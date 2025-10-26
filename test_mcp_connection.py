"""
Test MCP Server Connection
Quick diagnostic to see if the server can start properly
"""
import sys
import asyncio

async def test_server():
    print("="*70)
    print("MCP Server Connection Test")
    print("="*70)
    print()
    
    # Test 1: Check imports
    print("Test 1: Checking imports...")
    try:
        from mcp.server import Server
        from mcp.types import Tool, TextContent
        import mcp.server.stdio
        print("✓ MCP imports successful")
    except Exception as e:
        print(f"✗ MCP import failed: {e}")
        return
    
    # Test 2: Check medical components
    print("\nTest 2: Checking medical components...")
    try:
        from medical_extractor_simple import MedicalExtractor
        from database_saver import MedicalRecordDB
        print("✓ Medical components loaded")
    except Exception as e:
        print(f"✗ Medical components failed: {e}")
        return
    
    # Test 3: Check translator
    print("\nTest 3: Checking translator...")
    try:
        from translator import MultilingualTranslator
        print("✓ Translator available")
    except Exception as e:
        print(f"⚠️  Translator not available: {e}")
    
    # Test 4: Create server
    print("\nTest 4: Creating MCP server...")
    try:
        app = Server("mediscribe")
        print("✓ Server created successfully")
    except Exception as e:
        print(f"✗ Server creation failed: {e}")
        return
    
    # Test 5: Check tools
    print("\nTest 5: Checking tools...")
    try:
        # Import the actual server to get tools
        import mcp_server
        print("✓ Server module loaded")
    except Exception as e:
        print(f"✗ Server module failed: {e}")
        return
    
    print("\n" + "="*70)
    print("✓ All tests passed!")
    print("="*70)
    print()
    print("If Claude still doesn't see tools, try:")
    print("1. Completely quit Claude Desktop (check Task Manager)")
    print("2. Wait 10 seconds")
    print("3. Start Claude Desktop again")
    print("4. Wait for it to fully load")
    print("5. Look for the tools icon")
    print()

if __name__ == "__main__":
    asyncio.run(test_server())
