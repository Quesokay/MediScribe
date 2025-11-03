"""
Test ADK setup and agent configuration
"""
import os
import sys

print("="*70)
print("Testing MediScribe ADK Setup")
print("="*70)

# Test 1: Check imports
print("\n1. Checking imports...")
try:
    from google import genai
    print("   ✓ google-genai installed")
except ImportError as e:
    print(f"   ✗ google-genai not installed: {e}")
    sys.exit(1)

try:
    from adk.agents import Agent
    from adk.tools import tool
    print("   ✓ google-adk installed")
except ImportError as e:
    print(f"   ✗ google-adk not installed: {e}")
    print("   Run: pip install google-adk")
    sys.exit(1)

# Test 2: Check API key
print("\n2. Checking API key...")
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    print(f"   ✓ API key set ({api_key[:20]}...)")
else:
    print("   ✗ GOOGLE_API_KEY not set")
    print("   Set it with: set GOOGLE_API_KEY=your_key")
    sys.exit(1)

# Test 3: Check MediScribe components
print("\n3. Checking MediScribe components...")
try:
    from medical_extractor_simple import MedicalExtractor
    print("   ✓ Medical extractor available")
except ImportError as e:
    print(f"   ✗ Medical extractor not found: {e}")

try:
    from database_saver import MedicalRecordDB
    print("   ✓ Database saver available")
except ImportError as e:
    print(f"   ✗ Database saver not found: {e}")

try:
    from translator import MultilingualTranslator
    print("   ✓ Translator available")
except ImportError as e:
    print(f"   ⚠ Translator not available (English only mode): {e}")

# Test 4: Create a simple agent
print("\n4. Testing agent creation...")
try:
    client = genai.Client(api_key=api_key)
    
    @tool
    def test_tool(message: str) -> str:
        """A simple test tool"""
        return f"Received: {message}"
    
    agent = Agent(
        name="TestAgent",
        model="gemini-2.0-flash-exp",
        client=client,
        system_instruction="You are a test agent.",
        tools=[test_tool]
    )
    print(f"   ✓ Agent created successfully")
    print(f"   Model: {agent.model}")
    print(f"   Tools: {len(agent.tools)}")
except Exception as e:
    print(f"   ✗ Failed to create agent: {e}")
    sys.exit(1)

# Test 5: Check ADK web directory
print("\n5. Checking ADK web UI...")
from pathlib import Path
adk_web_dir = Path("adk-web")
if adk_web_dir.exists():
    print(f"   ✓ ADK web directory found")
    if (adk_web_dir / "node_modules").exists():
        print(f"   ✓ Node modules installed")
    else:
        print(f"   ⚠ Node modules not installed - run: cd adk-web && npm install")
else:
    print(f"   ✗ ADK web directory not found")

print("\n" + "="*70)
print("Setup Test Complete!")
print("="*70)
print("\nNext steps:")
print("1. Run: START_ADK_MEDISCRIBE.bat")
print("2. Open: http://localhost:4200")
print("3. Start using voice interaction!")
print("="*70)
