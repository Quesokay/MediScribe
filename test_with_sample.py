"""Test the extractor with sample transcription file"""
from medical_extractor_simple import MedicalExtractor
from database_saver import MedicalRecordDB
import json

print("="*60)
print("Testing with sample_transcription.txt")
print("="*60)

# Extract from file
extractor = MedicalExtractor()
result = extractor.extract_from_file("sample_transcription.txt")

print("\nExtracted Data:")
print(json.dumps(result, indent=2))

# Save to database
print("\n" + "="*60)
print("Saving to database...")
print("="*60)

db = MedicalRecordDB()
record_id = db.add_record(result)

print(f"\n✓ Record saved with ID: {record_id}")
print(f"✓ Total records in database: {len(db.get_all_records())}")
