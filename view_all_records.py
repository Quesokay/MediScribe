"""
View all medical records in the database
"""
import json
from database_saver import MedicalRecordDB

# Initialize database
db = MedicalRecordDB()
records = db.get_all_records()

print("\n" + "="*70)
print(f"TOTAL RECORDS IN DATABASE: {len(records)}")
print("="*70)

if not records:
    print("\nNo records found in database.")
else:
    for i, record in enumerate(records, 1):
        print(f"\n[{i}] Record ID: {record['record_id']}")
        print(f"    Date: {record['timestamp'][:10]}")
        
        if record.get('patient_name'):
            print(f"    Patient: {record['patient_name']}")
        
        if record.get('age'):
            print(f"    Age: {record['age']}")
        
        if record.get('gender'):
            print(f"    Gender: {record['gender']}")
        
        if record.get('symptoms'):
            print(f"    Symptoms: {', '.join(record['symptoms'])}")
        
        if record.get('diagnosis'):
            print(f"    Diagnosis: {', '.join(record['diagnosis'])}")
        
        if record.get('medications'):
            print(f"    Medications: {', '.join(record['medications'])}")
        
        if record.get('vital_signs'):
            print(f"    Vital Signs: {', '.join(record['vital_signs'])}")

print("\n" + "="*70)
print(f"END OF RECORDS (Total: {len(records)})")
print("="*70)
