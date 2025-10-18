import json

with open('medical_records.json', 'r') as f:
    data = json.load(f)

print(f"\n✅ Database has {len(data)} record(s)\n")

if data:
    latest = data[-1]
    print("Latest Record:")
    print(f"  ID: {latest['record_id']}")
    print(f"  Patient: {latest['patient_name']}")
    print(f"  Age: {latest['age']}")
    print(f"  Gender: {latest['gender']}")
    print(f"  Diagnosis: {', '.join(latest['diagnosis'])}")
    print(f"  Medications: {', '.join(latest['medications'])}")
    print()
