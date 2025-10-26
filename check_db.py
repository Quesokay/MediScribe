from database_saver import MedicalRecordDB

db = MedicalRecordDB()
records = db.get_all_records()

print(f"\nDatabase file: medical_records.json")
print(f"Total records: {len(records)}\n")

for i, r in enumerate(records, 1):
    print(f"{i}. {r['record_id']} - {r.get('patient_name', 'No name')} - {r['timestamp'][:10]}")
