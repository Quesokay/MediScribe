"""
MediScribe ADK Agent
Google ADK agent that integrates with MediScribe MCP server for voice-based medical transcription
Uses Gemini 2.5 Flash for text processing with live voice interaction
"""
import os
import sys
import json
import asyncio
from pathlib import Path
from typing import Any, Dict, List

# Google ADK imports
from google import genai
from google.genai import types
from adk.agents import Agent
from adk.tools import Tool, ToolContext

# MCP client imports
import subprocess
import threading
import queue


class MCPClient:
    """Client to communicate with MediScribe MCP server"""
    
    def __init__(self, python_path: str, server_script: str):
        self.python_path = python_path
        self.server_script = server_script
        self.process = None
        self.output_queue = queue.Queue()
        self.error_queue = queue.Queue()
        
    def start(self):
        """Start the MCP server process"""
        print(f"Starting MCP server: {self.server_script}")
        self.process = subprocess.Popen(
            [self.python_path, self.server_script],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        # Start threads to read output
        threading.Thread(target=self._read_output, daemon=True).start()
        threading.Thread(target=self._read_errors, daemon=True).start()
        print("MCP server started")
        
    def _read_output(self):
        """Read stdout from MCP server"""
        for line in iter(self.process.stdout.readline, ''):
            if line:
                self.output_queue.put(line.strip())
                
    def _read_errors(self):
        """Read stderr from MCP server"""
        for line in iter(self.process.stderr.readline, ''):
            if line:
                self.error_queue.put(line.strip())
                print(f"[MCP Server] {line.strip()}")
    
    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call an MCP tool"""
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }
        
        # Send request
        request_json = json.dumps(request) + "\n"
        self.process.stdin.write(request_json)
        self.process.stdin.flush()
        
        # Read response
        response_line = self.output_queue.get(timeout=30)
        response = json.loads(response_line)
        
        if "result" in response:
            # Extract text content from MCP response
            content = response["result"]["content"]
            if isinstance(content, list) and len(content) > 0:
                return json.loads(content[0]["text"])
            return content
        elif "error" in response:
            raise Exception(f"MCP Error: {response['error']}")
        
        return response
    
    def stop(self):
        """Stop the MCP server"""
        if self.process:
            self.process.terminate()
            self.process.wait()


# Initialize MCP client
PROJECT_DIR = Path(__file__).parent
PYTHON_PATH = str(PROJECT_DIR / ".venv" / "Scripts" / "python.exe")
MCP_SERVER_PATH = str(PROJECT_DIR / "mcp_server.py")

mcp_client = MCPClient(PYTHON_PATH, MCP_SERVER_PATH)


# Define ADK tools that wrap MCP functionality
async def process_conversation_tool(context: ToolContext, conversation: str, save_to_db: bool = True) -> str:
    """
    Process a medical conversation with auto-translation and data extraction.
    Supports English, Shona, Ndebele, Zulu, Xhosa, and Afrikaans.
    
    Args:
        conversation: The conversation transcript from voice interaction
        save_to_db: Whether to save extracted data to database (default: True)
    
    Returns:
        JSON string with extracted medical data
    """
    try:
        result = mcp_client.call_tool("process_conversation", {
            "conversation": conversation,
            "save_to_db": save_to_db
        })
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


async def extract_medical_data_tool(context: ToolContext, transcription: str, save_to_db: bool = False) -> str:
    """
    Extract structured medical information from English transcription.
    
    Args:
        transcription: Medical transcription text in English
        save_to_db: Whether to save extracted data to database
    
    Returns:
        JSON string with extracted medical data
    """
    try:
        result = mcp_client.call_tool("extract_medical_data", {
            "transcription": transcription,
            "save_to_db": save_to_db
        })
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


async def search_patient_records_tool(context: ToolContext, patient_name: str) -> str:
    """
    Search medical records database by patient name.
    
    Args:
        patient_name: Patient name to search for
    
    Returns:
        JSON string with matching records
    """
    try:
        result = mcp_client.call_tool("search_patient_records", {
            "patient_name": patient_name
        })
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


async def get_all_records_tool(context: ToolContext, limit: int = 50) -> str:
    """
    Retrieve all medical records from the database.
    
    Args:
        limit: Maximum number of records to return
    
    Returns:
        JSON string with all records
    """
    try:
        result = mcp_client.call_tool("get_all_records", {
            "limit": limit
        })
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


# Create the MediScribe agent
def create_mediscribe_agent(api_key: str) -> Agent:
    """Create and configure the MediScribe ADK agent"""
    
    # Configure Gemini client
    client = genai.Client(api_key=api_key)
    
    # Create agent with Gemini 2.5 Flash
    agent = Agent(
        name="MediScribe",
        model="gemini-2.0-flash-exp",
        client=client,
        system_instruction="""You are MediScribe, an AI medical assistant that helps healthcare professionals 
transcribe, translate, and extract structured data from medical conversations.

Your capabilities:
1. Process voice conversations in multiple languages (English, Shona, Ndebele, Zulu, Xhosa, Afrikaans)
2. Auto-detect language and translate to English if needed
3. Extract structured medical data: patient info, symptoms, diagnosis, medications, vital signs
4. Save records to database for later retrieval
5. Search and retrieve patient records

When a user provides a conversation transcript:
1. Use process_conversation_tool to handle it (this auto-detects language and translates)
2. Present the extracted data in a clear, organized format
3. Highlight key medical information
4. Ask if they want to save to database or search for related records

Be professional, accurate, and helpful. Always confirm important medical details.""",
        tools=[
            process_conversation_tool,
            extract_medical_data_tool,
            search_patient_records_tool,
            get_all_records_tool
        ]
    )
    
    return agent


def main():
    """Main entry point"""
    # Get API key from environment or argument
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY environment variable not set")
        print("Set it with: set GOOGLE_API_KEY=your_api_key")
        sys.exit(1)
    
    print("="*70)
    print("MediScribe ADK Agent")
    print("="*70)
    print("Starting MCP server...")
    
    # Start MCP server
    mcp_client.start()
    
    print("Creating agent...")
    agent = create_mediscribe_agent(api_key)
    
    print("Agent ready!")
    print("="*70)
    print("\nYou can now:")
    print("1. Start the ADK web UI to interact via voice")
    print("2. Use the agent programmatically")
    print("\nTo start web UI:")
    print("  cd adk-web")
    print("  npm run serve")
    print("\nThen in another terminal:")
    print("  adk api_server --allow_origins=http://localhost:4200")
    print("="*70)
    
    try:
        # Keep running
        input("\nPress Enter to stop...\n")
    finally:
        print("\nStopping MCP server...")
        mcp_client.stop()
        print("Goodbye!")


if __name__ == "__main__":
    main()
