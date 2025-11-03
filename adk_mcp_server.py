"""
ADK API Server with MCP Client Integration
This server connects ADK Web UI to your MediScribe MCP server
"""
import os
import sys
import json
import asyncio
import subprocess
from pathlib import Path
from typing import Any, Dict, Optional

from adk.agents import Agent
from adk.tools import tool
from google import genai

# MCP Client using subprocess
class MCPClient:
    """Client to communicate with MediScribe MCP server via stdio"""
    
    def __init__(self, python_path: str, server_script: str):
        self.python_path = python_path
        self.server_script = server_script
        self.process = None
        self.request_id = 0
        
    async def start(self):
        """Start the MCP server process"""
        print(f"Starting MCP server: {self.server_script}")
        self.process = await asyncio.create_subprocess_exec(
            self.python_path,
            self.server_script,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        # Start reading stderr in background
        asyncio.create_task(self._read_stderr())
        print("MCP server started")
        
    async def _read_stderr(self):
        """Read and print stderr from MCP server"""
        async for line in self.process.stderr:
            print(f"[MCP] {line.decode().strip()}")
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call an MCP tool"""
        self.request_id += 1
        
        # MCP request format
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }
        
        # Send request
        request_json = json.dumps(request) + "\n"
        self.process.stdin.write(request_json.encode())
        await self.process.stdin.drain()
        
        # Read response
        response_line = await self.process.stdout.readline()
        response = json.loads(response_line.decode())
        
        if "result" in response:
            # Extract text content from MCP response
            content = response["result"]["content"]
            if isinstance(content, list) and len(content) > 0:
                return json.loads(content[0]["text"])
            return content
        elif "error" in response:
            raise Exception(f"MCP Error: {response['error']}")
        
        return response
    
    async def stop(self):
        """Stop the MCP server"""
        if self.process:
            self.process.terminate()
            await self.process.wait()


# Initialize MCP client
PROJECT_DIR = Path(__file__).parent
PYTHON_PATH = str(PROJECT_DIR / ".venv" / "Scripts" / "python.exe")
MCP_SERVER_PATH = str(PROJECT_DIR / "mcp_server.py")

# Global MCP client instance
mcp_client = None


async def get_mcp_client() -> MCPClient:
    """Get or create MCP client"""
    global mcp_client
    if mcp_client is None:
        mcp_client = MCPClient(PYTHON_PATH, MCP_SERVER_PATH)
        await mcp_client.start()
    return mcp_client


# Define ADK tools that wrap MCP functionality
@tool
async def process_conversation(conversation: str, save_to_db: bool = True) -> str:
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
        client = await get_mcp_client()
        result = await client.call_tool("process_conversation", {
            "conversation": conversation,
            "save_to_db": save_to_db
        })
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


@tool
async def extract_medical_data(transcription: str, save_to_db: bool = False) -> str:
    """
    Extract structured medical information from English transcription.
    
    Args:
        transcription: Medical transcription text in English
        save_to_db: Whether to save extracted data to database
    
    Returns:
        JSON string with extracted medical data
    """
    try:
        client = await get_mcp_client()
        result = await client.call_tool("extract_medical_data", {
            "transcription": transcription,
            "save_to_db": save_to_db
        })
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


@tool
async def search_patient_records(patient_name: str) -> str:
    """
    Search medical records database by patient name.
    
    Args:
        patient_name: Patient name to search for
    
    Returns:
        JSON string with matching records
    """
    try:
        client = await get_mcp_client()
        result = await client.call_tool("search_patient_records", {
            "patient_name": patient_name
        })
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


@tool
async def get_all_records(limit: int = 50) -> str:
    """
    Retrieve all medical records from the database.
    
    Args:
        limit: Maximum number of records to return
    
    Returns:
        JSON string with all records
    """
    try:
        client = await get_mcp_client()
        result = await client.call_tool("get_all_records", {
            "limit": limit
        })
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


@tool
async def get_patient_record(record_id: str) -> str:
    """
    Retrieve a specific medical record by ID.
    
    Args:
        record_id: Record ID (format: REC-YYYYMMDDHHMMSS)
    
    Returns:
        JSON string with record data or error
    """
    try:
        client = await get_mcp_client()
        result = await client.call_tool("get_patient_record", {
            "record_id": record_id
        })
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


# Create the agent
def create_agent(api_key: str = None) -> Agent:
    """Create and return the MediScribe agent with MCP integration"""
    
    if not api_key:
        api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not set. Use: set GOOGLE_API_KEY=your_key")
    
    # Configure Gemini client
    client = genai.Client(api_key=api_key)
    
    # Create agent
    agent = Agent(
        name="MediScribe",
        model="gemini-2.0-flash-exp",
        client=client,
        system_instruction="""You are MediScribe, an AI medical assistant for healthcare professionals.

Your capabilities:
- Process voice conversations in multiple languages (English, Shona, Ndebele, Zulu, Xhosa, Afrikaans)
- Auto-detect language and translate to English if needed
- Extract structured medical data: patient info, symptoms, diagnosis, medications, vital signs
- Save records to database and retrieve them later

When processing a conversation:
1. Use process_conversation() for any medical conversation (handles translation automatically)
2. Present extracted data clearly with key medical information highlighted
3. Offer to save to database or search for related records

Be professional, accurate, and helpful. Always confirm important medical details.""",
        tools=[
            process_conversation,
            extract_medical_data,
            search_patient_records,
            get_all_records,
            get_patient_record
        ]
    )
    
    print(f"\n{'='*70}")
    print("MediScribe Agent Created (with MCP Integration)")
    print(f"{'='*70}")
    print(f"Model: {agent.model}")
    print(f"Tools: {len(agent.tools)} available (via MCP)")
    print(f"MCP Server: {MCP_SERVER_PATH}")
    print(f"{'='*70}\n")
    
    return agent


# Export for ADK API server
root_agent = create_agent()


# Cleanup on exit
import atexit

@atexit.register
def cleanup():
    """Cleanup MCP client on exit"""
    global mcp_client
    if mcp_client:
        asyncio.run(mcp_client.stop())
