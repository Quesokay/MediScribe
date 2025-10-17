"""Quick view of all records"""
from database_saver import MedicalRecordDB
import json

db = MedicalRecordDB()
records = db.get_all_records()

print(f"\n📊 Total Records: {len(records)}\n")
print(json.dumps(records, indent=2))
