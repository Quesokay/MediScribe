"""
Test client for MediScribe MCP Server
Demonstrates how to use the MCP server programmatically
"""
import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_extraction():
    """Test basic medical data extraction"""
    print("="*70)
    print("TEST 1: Extract Medical Data")
    print("="*70)
    
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Test extraction
            transcription = """
            Patient John Doe, 45 year old male, presents with persistent cough 
            and fever for 5 days. Temperature 101.5F, BP 130/85.
            Diagnosis: Suspected pneumonia.
            Prescribed Amoxicillin 500mg three times daily.
            """
            
            result = await session.call_tool(
                "extract_medical_data",
                {
                    "transcription": transcription,
                    "save_to_db": False
                }
            )
            
            print("\nInput:")
            print(transcription)
            print("\nExtracted Data:")
            print(json.dumps(json.loads(result.content[0].text), indent=2))


async def test_translation():
    """Test multilingual translation and extraction"""
    print("\n" + "="*70)
    print("TEST 2: Translate and Extract (Shona)")
    print("="*70)
    
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Test Shona translation
            shona_text = """
            Murwere: John Doe, makore 45, murume.
            Ndiri kunzwa kurwara uye ndine fivha.
            Tembiricha: 38.5 degrees.
            Mushonga: Paracetamol 500mg.
            """
            
            result = await session.call_tool(
                "translate_and_extract",
                {
                    "transcription": shona_text,
                    "save_to_db": False
                }
            )
            
            print("\nInput (Shona):")
            print(shona_text)
            print("\nResult:")
            print(json.dumps(json.loads(result.content[0].text), indent=2))


async def test_database_operations():
    """Test database save and search"""
    print("\n" + "="*70)
    print("TEST 3: Database Operations")
    print("="*70)
    
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Extract and save
            transcription = "Patient Jane Smith, 28 year old female, headache and nausea."
            
            print("\n1. Extracting and saving to database...")
            result = await session.call_tool(
                "extract_medical_data",
                {
                    "transcription": transcription,
                    "save_to_db": True
                }
            )
            
            data = json.loads(result.content[0].text)
            print(f"✓ Saved with Record ID: {data['record_id']}")
            
            # Search by patient name
            print("\n2. Searching for patient records...")
            search_result = await session.call_tool(
                "search_patient_records",
                {"patient_name": "Jane Smith"}
            )
            
            search_data = json.loads(search_result.content[0].text)
            print(f"✓ Found {search_data['records_found']} record(s)")
            
            # Get all records
            print("\n3. Getting all records...")
            all_result = await session.call_tool(
                "get_all_records",
                {"limit": 10}
            )
            
            all_data = json.loads(all_result.content[0].text)
            print(f"✓ Total records in database: {all_data['total_records']}")


async def test_list_tools():
    """List all available tools"""
    print("\n" + "="*70)
    print("TEST 4: List Available Tools")
    print("="*70)
    
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # List tools
            tools = await session.list_tools()
            
            print(f"\nAvailable Tools ({len(tools.tools)}):")
            for tool in tools.tools:
                print(f"\n  • {tool.name}")
                print(f"    {tool.description}")


async def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("MEDISCRIBE MCP SERVER TEST SUITE")
    print("="*70)
    print("Testing MCP server functionality...\n")
    
    try:
        await test_list_tools()
        await test_extraction()
        await test_translation()
        await test_database_operations()
        
        print("\n" + "="*70)
        print("✓ ALL TESTS COMPLETED SUCCESSFULLY")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
