"""
Database integration for medical records
This is a simple example using JSON files as a database
Replace with actual database (PostgreSQL, MongoDB, etc.) in production
"""
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List


class MedicalRecordDB:
    def __init__(self, db_path: str = "medical_records.json"):
        """Initialize the database"""
        import sys
        self.db_path = Path(db_path)
        self.records = self._load_records()
        print(f"Database initialized: {self.db_path.absolute()}", file=sys.stderr)
        print(f"Loaded {len(self.records)} existing records", file=sys.stderr)
    
    def _load_records(self) -> List[Dict]:
        """Load existing records from file"""
        if self.db_path.exists():
            with open(self.db_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    
    def _save_records(self):
        """Save records to file"""
        import sys
        try:
            with open(self.db_path, "w", encoding="utf-8") as f:
                json.dump(self.records, f, indent=2, ensure_ascii=False)
            print(f"Database file updated: {self.db_path.absolute()}", file=sys.stderr)
        except Exception as e:
            print(f"ERROR saving database: {e}", file=sys.stderr)
    
    def add_record(self, extracted_data: Dict) -> str:
        """
        Add a new medical record
        
        Args:
            extracted_data: Dictionary with extracted medical information
            
        Returns:
            Record ID
        """
        record_id = f"REC-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        record = {
            "record_id": record_id,
            "timestamp": datetime.now().isoformat(),
            "patient_name": extracted_data.get("patient_name"),
            "age": extracted_data.get("age"),
            "gender": extracted_data.get("gender"),
            "symptoms": [s["text"] for s in extracted_data.get("symptoms", [])],
            "diagnosis": [d["text"] for d in extracted_data.get("diagnosis", [])],
            "medications": [m["text"] for m in extracted_data.get("medications", [])],
            "dosages": [d["text"] for d in extracted_data.get("dosages", [])],
            "vital_signs": [v["text"] for v in extracted_data.get("vital_signs", [])],
            "allergies": [a["text"] for a in extracted_data.get("allergies", [])],
            "treatment_plan": [t["text"] for t in extracted_data.get("treatment_plan", [])],
            "follow_up": [f["text"] for f in extracted_data.get("follow_up", [])],
            "raw_transcription": extracted_data.get("raw_transcription", "")
        }
        
        self.records.append(record)
        self._save_records()
        
        import sys
        print(f"Record saved with ID: {record_id}", file=sys.stderr)
        return record_id
    
    def get_record(self, record_id: str) -> Dict:
        """Retrieve a record by ID"""
        for record in self.records:
            if record["record_id"] == record_id:
                return record
        return None
    
    def search_by_patient(self, patient_name: str) -> List[Dict]:
        """Search records by patient name"""
        return [r for r in self.records if r.get("patient_name") == patient_name]
    
    def get_all_records(self, limit: int = None) -> List[Dict]:
        """Get all records, optionally limited to a specific number"""
        if limit:
            return self.records[:limit]
        return self.records


def main():
    """Example usage"""
    from medical_extractor import MedicalExtractor
    
    print("Processing sample transcription and saving to database...\n")
    
    # Extract information
    extractor = MedicalExtractor()
    extracted_data = extractor.extract_from_file("sample_transcription.txt")
    
    # Save to database
    db = MedicalRecordDB()
    record_id = db.add_record(extracted_data)
    
    print(f"\nTotal records in database: {len(db.get_all_records())}")
    
    # Retrieve and display
    print("\n" + "="*60)
    print("SAVED RECORD")
    print("="*60)
    record = db.get_record(record_id)
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
