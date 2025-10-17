"""
Batch process multiple Vibe transcription files
"""
from medical_extractor_simple import MedicalExtractor
from database_saver import MedicalRecordDB
from pathlib import Path
import json

def batch_process_folder(folder_path: str, pattern: str = "*.txt"):
    """
    Process all transcription files in a folder
    
    Args:
        folder_path: Path to folder containing transcription files
        pattern: File pattern to match (e.g., "*.txt", "*.json")
    """
    folder = Path(folder_path)
    files = list(folder.glob(pattern))
    
    if not files:
        print(f"No files found matching '{pattern}' in {folder_path}")
        return
    
    print(f"Found {len(files)} files to process\n")
    
    # Initialize
    extractor = MedicalExtractor()
    db = MedicalRecordDB()
    
    successful = 0
    failed = 0
    
    for file_path in files:
        try:
            print(f"Processing: {file_path.name}...", end=" ")
            
            # Extract data
            result = extractor.extract_from_file(str(file_path))
            
            # Save to database
            record_id = db.add_record(result)
            
            print(f"✓ Saved as {record_id}")
            successful += 1
            
        except Exception as e:
            print(f"✗ Error: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print("BATCH PROCESSING COMPLETE")
    print("="*60)
    print(f"✓ Successful: {successful}")
    print(f"✗ Failed: {failed}")
    print(f"Total records in database: {len(db.get_all_records())}")


def process_single_file(file_path: str, save_json: bool = True):
    """
    Process a single file and optionally save as JSON
    
    Args:
        file_path: Path to transcription file
        save_json: Whether to save extracted data as JSON
    """
    print(f"Processing: {file_path}\n")
    
    extractor = MedicalExtractor()
    result = extractor.extract_from_file(file_path)
    
    # Display results
    print("="*60)
    print("EXTRACTED DATA")
    print("="*60)
    print(json.dumps(result, indent=2))
    
    # Save to database
    db = MedicalRecordDB()
    record_id = db.add_record(result)
    print(f"\n✓ Saved to database as {record_id}")
    
    # Optionally save as JSON
    if save_json:
        output_path = Path(file_path).stem + "_extracted.json"
        extractor.save_to_json(result, output_path)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Single file:  python batch_process.py <file_path>")
        print("  Batch folder: python batch_process.py <folder_path> [pattern]")
        print("\nExamples:")
        print("  python batch_process.py transcription.txt")
        print("  python batch_process.py ./transcriptions")
        print("  python batch_process.py ./transcriptions *.json")
        sys.exit(1)
    
    path = Path(sys.argv[1])
    
    if path.is_file():
        # Process single file
        process_single_file(str(path))
    elif path.is_dir():
        # Process folder
        pattern = sys.argv[2] if len(sys.argv) > 2 else "*.txt"
        batch_process_folder(str(path), pattern)
    else:
        print(f"Error: {path} is not a valid file or directory")
