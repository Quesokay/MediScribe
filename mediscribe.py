"""
MediScribe - Intelligent Medical Transcription Extraction System
Main entry point for the application
"""
from medical_extractor_simple import MedicalExtractor
from database_saver import MedicalRecordDB
import sys
from pathlib import Path


def print_banner():
    """Display MediScribe banner"""
    print("\n" + "="*70)
    print("  __  __          _ _ ____            _ _          ")
    print(" |  \\/  | ___  __| (_) ___|  ___ _ __(_) |__   ___ ")
    print(" | |\\/| |/ _ \\/ _` | \\___ \\ / __| '__| | '_ \\ / _ \\")
    print(" | |  | |  __/ (_| | |___) | (__| |  | | |_) |  __/")
    print(" |_|  |_|\\___|\\__,_|_|____/ \\___|_|  |_|_.__/ \\___|")
    print("\n Intelligent Medical Transcription Extraction System")
    print("="*70 + "\n")


def show_help():
    """Display help information"""
    print_banner()
    print("Usage:")
    print("  mediscribe.py <file_or_folder> [options]\n")
    print("Commands:")
    print("  mediscribe.py transcription.txt     Process single file")
    print("  mediscribe.py ./transcriptions      Process all files in folder")
    print("  mediscribe.py --view                View all records")
    print("  mediscribe.py --search <name>       Search by patient name")
    print("  mediscribe.py --help                Show this help\n")
    print("Examples:")
    print("  mediscribe.py doctor_notes.txt")
    print("  mediscribe.py ./medical_transcriptions")
    print("  mediscribe.py --search \"John Doe\"")
    print("  mediscribe.py --view\n")


def process_file(file_path: str):
    """Process a single transcription file"""
    print(f"📄 Processing: {file_path}\n")
    
    extractor = MedicalExtractor()
    result = extractor.extract_from_file(file_path)
    
    # Display key info
    print("✓ Extraction complete!")
    print(f"  Patient: {result.get('patient_name', 'Unknown')}")
    print(f"  Age: {result.get('age', 'N/A')}")
    print(f"  Gender: {result.get('gender', 'N/A')}")
    
    if result.get('diagnosis'):
        print(f"  Diagnosis: {', '.join([d['text'] for d in result['diagnosis']])}")
    
    # Save to database
    db = MedicalRecordDB()
    record_id = db.add_record(result)
    
    print(f"\n✓ Saved to database as {record_id}")


def process_folder(folder_path: str):
    """Process all transcription files in a folder"""
    folder = Path(folder_path)
    files = list(folder.glob("*.txt")) + list(folder.glob("*.json"))
    
    if not files:
        print(f"❌ No transcription files found in {folder_path}")
        return
    
    print(f"📁 Found {len(files)} file(s) to process\n")
    
    extractor = MedicalExtractor()
    db = MedicalRecordDB()
    
    successful = 0
    for file_path in files:
        try:
            print(f"  Processing: {file_path.name}...", end=" ")
            result = extractor.extract_from_file(str(file_path))
            record_id = db.add_record(result)
            print(f"✓ {record_id}")
            successful += 1
        except Exception as e:
            print(f"✗ Error: {e}")
    
    print(f"\n✓ Successfully processed {successful}/{len(files)} files")


def view_records():
    """View all records in database"""
    db = MedicalRecordDB()
    records = db.get_all_records()
    
    if not records:
        print("📭 No records in database")
        return
    
    print(f"📊 Total Records: {len(records)}\n")
    
    for record in records:
        print(f"{'='*70}")
        print(f"ID: {record['record_id']}")
        print(f"Patient: {record['patient_name']} ({record['age']}, {record['gender']})")
        print(f"Date: {record['timestamp'][:10]}")
        if record['diagnosis']:
            print(f"Diagnosis: {', '.join(record['diagnosis'])}")
        print()


def search_patient(name: str):
    """Search for patient records"""
    db = MedicalRecordDB()
    records = db.search_by_patient(name)
    
    if not records:
        print(f"📭 No records found for: {name}")
        return
    
    print(f"✓ Found {len(records)} record(s) for {name}\n")
    
    for record in records:
        print(f"{'='*70}")
        print(f"ID: {record['record_id']}")
        print(f"Date: {record['timestamp'][:10]}")
        if record['diagnosis']:
            print(f"Diagnosis: {', '.join(record['diagnosis'])}")
        if record['medications']:
            print(f"Medications: {', '.join(record['medications'])}")
        print()


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1]
    
    if command in ['--help', '-h', 'help']:
        show_help()
    elif command == '--view':
        print_banner()
        view_records()
    elif command == '--search':
        if len(sys.argv) < 3:
            print("❌ Please provide a patient name to search")
            return
        print_banner()
        search_patient(sys.argv[2])
    else:
        # Process file or folder
        path = Path(command)
        print_banner()
        
        if path.is_file():
            process_file(command)
        elif path.is_dir():
            process_folder(command)
        else:
            print(f"❌ File or folder not found: {command}")
            print("\nRun 'mediscribe.py --help' for usage information")


if __name__ == "__main__":
    main()
