"""
MediScribe Agent for ADK
Connects to MediScribe MCP server
"""
import os
import sys
import json
import asyncio
from pathlib import Path
from typing import Any, Dict

# Ensure we can import from project root
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Import Google GenAI and ADK
from google import genai
from google.adk.agents import Agent
from google.adk.tools import FunctionTool


# MCP Client class
class MCPClient:
    """Client to communicate with MediScribe MCP server via stdio"""
    
    def __init__(self, python_path: str, server_script: str):
        self.python_path = python_path
        self.server_script = server_script
        self.process = None
        self.request_id = 0
        self._started = False
        
    async def start(self):
        """Start the MCP server process"""
        if self._started:
            return
            
        print(f"[ADK] Starting MCP server: {self.server_script}")
        self.process = await asyncio.create_subprocess_exec(
            self.python_path,
            self.server_script,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        # Start reading stderr in background
        asyncio.create_task(self._read_stderr())
        self._started = True
        
        # Wait for server to initialize
        await asyncio.sleep(3)
        print("[ADK] MCP server started and ready")
        
    async def _read_stderr(self):
        """Read and print stderr from MCP server"""
        try:
            async for line in self.process.stderr:
                print(f"[MCP] {line.decode().strip()}")
        except Exception as e:
            print(f"[MCP] Error reading stderr: {e}")
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call an MCP tool"""
        if not self._started:
            await self.start()
            
        self.request_id += 1
        
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }
        
        print(f"[MCP Client] Calling tool: {tool_name} with args: {arguments}")
        request_json = json.dumps(request) + "\n"
        self.process.stdin.write(request_json.encode())
        await self.process.stdin.drain()
        
        print(f"[MCP Client] Waiting for response...")
        response_line = await asyncio.wait_for(self.process.stdout.readline(), timeout=30)
        if not response_line:
            raise Exception("MCP server closed connection")
        
        print(f"[MCP Client] Got response: {response_line.decode()[:200]}...")
        response = json.loads(response_line.decode())
        
        if "result" in response:
            content = response["result"]["content"]
            if isinstance(content, list) and len(content) > 0:
                return json.loads(content[0]["text"])
            return content
        elif "error" in response:
            raise Exception(f"MCP Error: {response['error']}")
        
        return response
    
    async def stop(self):
        """Stop the MCP server"""
        if self.process and self._started:
            self.process.terminate()
            await self.process.wait()
            self._started = False


# Initialize MCP client
PROJECT_DIR = Path(__file__).parent.parent.parent
PYTHON_PATH = str(PROJECT_DIR / ".venv" / "Scripts" / "python.exe")
if not Path(PYTHON_PATH).exists():
    # Fallback to system python
    PYTHON_PATH = sys.executable

MCP_SERVER_PATH = str(PROJECT_DIR / "mcp_server.py")

# Global MCP client
_mcp_client = None


async def get_mcp_client() -> MCPClient:
    """Get or create MCP client"""
    global _mcp_client
    if _mcp_client is None:
        _mcp_client = MCPClient(PYTHON_PATH, MCP_SERVER_PATH)
        await _mcp_client.start()
    return _mcp_client


# Define ADK tools that wrap MCP functionality
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
        error_msg = {"error": str(e), "tool": "process_conversation"}
        return json.dumps(error_msg, indent=2)


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
        error_msg = {"error": str(e), "tool": "extract_medical_data"}
        return json.dumps(error_msg, indent=2)


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
        error_msg = {"error": str(e), "tool": "search_patient_records"}
        return json.dumps(error_msg, indent=2)


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
        import traceback
        error_msg = {
            "error": str(e),
            "error_type": type(e).__name__,
            "traceback": traceback.format_exc(),
            "tool": "get_all_records"
        }
        print(f"[ERROR] get_all_records failed: {error_msg}")
        return json.dumps(error_msg, indent=2)


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
        error_msg = {"error": str(e), "tool": "get_patient_record"}
        return json.dumps(error_msg, indent=2)


# Get API key from environment
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError(
        "GOOGLE_API_KEY environment variable not set. "
        "Set it with: set GOOGLE_API_KEY=your_api_key"
    )

# Create the agent - this is what ADK will load
root_agent = Agent(
    name="MediScribe",
    model="gemini-2.0-flash-exp",
    instruction="""You are MediScribe, an AI medical assistant for healthcare professionals.

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
        FunctionTool(process_conversation),
        FunctionTool(extract_medical_data),
        FunctionTool(search_patient_records),
        FunctionTool(get_all_records),
        FunctionTool(get_patient_record)
    ]
)

# Print confirmation
print(f"\n{'='*70}")
print("MediScribe Agent Loaded Successfully")
print(f"{'='*70}")
print(f"Model: {root_agent.model}")
print(f"Tools: {len(root_agent.tools)} available (via MCP)")
print(f"MCP Server: {MCP_SERVER_PATH}")
print(f"Python: {PYTHON_PATH}")
print(f"{'='*70}\n")


# Cleanup on exit
import atexit

@atexit.register
def cleanup():
    """Cleanup MCP client on exit"""
    global _mcp_client
    if _mcp_client and _mcp_client._started:
        try:
            asyncio.run(_mcp_client.stop())
            print("[ADK] MCP client stopped")
        except Exception as e:
            print(f"[ADK] Error stopping MCP client: {e}")
