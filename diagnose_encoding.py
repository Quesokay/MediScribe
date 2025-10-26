"""
Diagnose encoding issues
"""
import sys
import io
import json

print("="*70)
print("Encoding Diagnostic Tool")
print("="*70)
print()

# Check current encoding
print(f"1. Current stdout encoding: {sys.stdout.encoding}")
print(f"2. Current stderr encoding: {sys.stderr.encoding}")
print(f"3. Default encoding: {sys.getdefaultencoding()}")
print()

# Test UTF-8 setup
print("4. Setting up UTF-8 encoding...")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', line_buffering=True)
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace', line_buffering=True)
print(f"   New stdout encoding: {sys.stdout.encoding}")
print(f"   New stderr encoding: {sys.stderr.encoding}")
print()

# Test ASCII characters
print("5. Testing ASCII characters...")
print("   Hello World 123")
print("   Status: OK")
print()

# Test JSON with ensure_ascii
print("6. Testing JSON with ensure_ascii=True...")
test_data = {
    "patient_name": "John Doe",
    "temperature": "101.5F",
    "status": "OK"
}
json_output = json.dumps(test_data, indent=2, ensure_ascii=True)
print(json_output)
print("   Status: OK")
print()

# Test medical extractor
print("7. Testing medical extractor...")
try:
    from medical_extractor_simple import MedicalExtractor
    extractor = MedicalExtractor()
    print("   Medical extractor loaded: OK")
except Exception as e:
    print(f"   Error: {e}")
print()

# Test database
print("8. Testing database...")
try:
    from database_saver import MedicalRecordDB
    db = MedicalRecordDB()
    print("   Database loaded: OK")
except Exception as e:
    print(f"   Error: {e}")
print()

# Test extraction
print("9. Testing extraction...")
try:
    sample = "Patient John Doe, 45 year old male, has fever."
    result = extractor.extract_from_text(sample)
    json_result = json.dumps(result, indent=2, ensure_ascii=True)
    print("   Extraction: OK")
    print("   Sample output:")
    print(json_result[:200] + "...")
except Exception as e:
    print(f"   Error: {e}")
    import traceback
    traceback.print_exc()
print()

print("="*70)
print("Diagnostic Complete!")
print("="*70)
print()
print("If all tests passed, the MCP server should work.")
print("If any test failed, that's where the problem is.")
