"""
Test MCP connection from ADK server
"""
import asyncio
import json
from pathlib import Path
from adk_mcp_server import MCPClient, PYTHON_PATH, MCP_SERVER_PATH

async def test_mcp():
    """Test MCP client connection"""
    print("="*70)
    print("Testing MCP Connection")
    print("="*70)
    
    # Create MCP client
    print(f"\n1. Creating MCP client...")
    print(f"   Python: {PYTHON_PATH}")
    print(f"   Server: {MCP_SERVER_PATH}")
    
    client = MCPClient(PYTHON_PATH, MCP_SERVER_PATH)
    
    # Start MCP server
    print(f"\n2. Starting MCP server...")
    await client.start()
    await asyncio.sleep(3)  # Wait for server to initialize
    print("   ✓ MCP server started")
    
    # Test process_conversation
    print(f"\n3. Testing process_conversation tool...")
    test_conversation = """
    Patient John Doe, age 45, presents with severe headache for 3 days.
    Blood pressure is 140/90. Temperature 37.2°C.
    Diagnosed with migraine. Prescribed ibuprofen 400mg three times daily.
    """
    
    try:
        result = await client.call_tool("process_conversation", {
            "conversation": test_conversation,
            "save_to_db": True
        })
        print("   ✓ Tool call successful")
        print(f"\n   Result:")
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"   ✗ Tool call failed: {e}")
    
    # Test search
    print(f"\n4. Testing search_patient_records tool...")
    try:
        result = await client.call_tool("search_patient_records", {
            "patient_name": "John Doe"
        })
        print("   ✓ Search successful")
        print(f"\n   Found {result.get('records_found', 0)} records")
    except Exception as e:
        print(f"   ✗ Search failed: {e}")
    
    # Stop MCP server
    print(f"\n5. Stopping MCP server...")
    await client.stop()
    print("   ✓ MCP server stopped")
    
    print("\n" + "="*70)
    print("MCP Connection Test Complete!")
    print("="*70)
    print("\nIf all tests passed, your setup is ready!")
    print("Run: START_ADK_MEDISCRIBE.bat")
    print("Then open: http://localhost:4200")
    print("="*70)

if __name__ == "__main__":
    asyncio.run(test_mcp())
