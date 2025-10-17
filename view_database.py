"""
View all medical records in the database
"""
from database_saver import MedicalRecordDB
import json
from datetime import datetime


def format_record(record):
    """Format a single record for display"""
    print("\n" + "="*70)
    print(f"📋 RECORD ID: {record['record_id']}")
    print("="*70)
    
    # Parse timestamp
    timestamp = datetime.fromisoformat(record['timestamp'])
    print(f"📅 Date: {timestamp.strftime('%B %d, %Y at %I:%M %p')}")
    
    print(f"\n👤 PATIENT INFORMATION")
    print(f"   Name: {record['patient_name'] or 'Not recorded'}")
    print(f"   Age: {record['age'] or 'Not recorded'}")
    print(f"   Gender: {record['gender'] or 'Not recorded'}")
    
    if record['symptoms']:
        print(f"\n🤒 SYMPTOMS")
        for symptom in record['symptoms']:
            print(f"   • {symptom}")
    
    if record['diagnosis']:
        print(f"\n🔬 DIAGNOSIS")
        for diag in record['diagnosis']:
            print(f"   • {diag}")
    
    if record['medications']:
        print(f"\n💊 MEDICATIONS")
        for med in record['medications']:
            print(f"   • {med}")
    
    if record['dosages']:
        print(f"\n📏 DOSAGES")
        for dose in record['dosages']:
            print(f"   • {dose}")
    
    if record['vital_signs']:
        print(f"\n❤️  VITAL SIGNS")
        for vital in record['vital_signs']:
            print(f"   • {vital}")
    
    if record['allergies']:
        print(f"\n⚠️  ALLERGIES")
        for allergy in record['allergies']:
            print(f"   • {allergy}")
    else:
        print(f"\n⚠️  ALLERGIES: None recorded")
    
    if record['treatment_plan']:
        print(f"\n📝 TREATMENT PLAN")
        for plan in record['treatment_plan']:
            print(f"   {plan}")
    
    if record['follow_up']:
        print(f"\n📆 FOLLOW-UP")
        for followup in record['follow_up']:
            print(f"   • {followup}")


def view_all_records():
    """Display all records in the database"""
    db = MedicalRecordDB()
    records = db.get_all_records()
    
    if not records:
        print("📭 Database is empty. No records found.")
        return
    
    print("\n" + "="*70)
    print(f"🏥 MEDICAL RECORDS DATABASE")
    print(f"   Total Records: {len(records)}")
    print("="*70)
    
    for record in records:
        format_record(record)
    
    print("\n" + "="*70)


def search_by_patient_name():
    """Interactive search by patient name"""
    db = MedicalRecordDB()
    
    print("\n🔍 Search by Patient Name")
    name = input("Enter patient name: ").strip()
    
    if not name:
        print("❌ No name entered")
        return
    
    records = db.search_by_patient(name)
    
    if not records:
        print(f"📭 No records found for patient: {name}")
        return
    
    print(f"\n✓ Found {len(records)} record(s) for {name}")
    
    for record in records:
        format_record(record)


def export_to_json():
    """Export database to a formatted JSON file"""
    db = MedicalRecordDB()
    records = db.get_all_records()
    
    output_file = "database_export.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Database exported to {output_file}")


def main():
    """Main menu"""
    while True:
        print("\n" + "="*70)
        print("🏥 MEDICAL RECORDS DATABASE VIEWER")
        print("="*70)
        print("1. View all records")
        print("2. Search by patient name")
        print("3. Export to JSON")
        print("4. Exit")
        print("="*70)
        
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == "1":
            view_all_records()
        elif choice == "2":
            search_by_patient_name()
        elif choice == "3":
            export_to_json()
        elif choice == "4":
            print("\n👋 Goodbye!")
            break
        else:
            print("❌ Invalid option. Please choose 1-4.")


if __name__ == "__main__":
    main()
