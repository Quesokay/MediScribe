"""
Medical Transcription Information Extractor
Extracts structured medical information from audio transcriptions
"""
import spacy
from spacy.util import load_config
from pathlib import Path
import json
from typing import Dict, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class MedicalExtractor:
    def __init__(self, config_path: str = "config.cfg"):
        """Initialize the medical extractor with spacy-llm pipeline"""
        # Load config and create pipeline
        config = load_config(config_path)
        self.nlp = spacy.util.load_model_from_config(config, auto_fill=True)
    
    def extract_from_text(self, transcription: str) -> Dict:
        """
        Extract structured medical information from transcription text
        
        Args:
            transcription: Raw text from audio transcription
            
        Returns:
            Dictionary with extracted medical fields
        """
        doc = self.nlp(transcription)
        
        # Organize entities by label
        extracted_data = {
            "patient_name": [],
            "age": [],
            "gender": [],
            "symptoms": [],
            "diagnosis": [],
            "medications": [],
            "dosages": [],
            "vital_signs": [],
            "allergies": [],
            "treatment_plan": [],
            "follow_up": [],
            "raw_transcription": transcription
        }
        
        # Map entity labels to fields
        label_mapping = {
            "PATIENT_NAME": "patient_name",
            "AGE": "age",
            "GENDER": "gender",
            "SYMPTOM": "symptoms",
            "DIAGNOSIS": "diagnosis",
            "MEDICATION": "medications",
            "DOSAGE": "dosages",
            "VITAL_SIGNS": "vital_signs",
            "ALLERGY": "allergies",
            "TREATMENT_PLAN": "treatment_plan",
            "FOLLOW_UP": "follow_up"
        }
        
        for ent in doc.ents:
            field = label_mapping.get(ent.label_)
            if field:
                extracted_data[field].append({
                    "text": ent.text,
                    "start": ent.start_char,
                    "end": ent.end_char
                })
        
        # Clean up single-value fields
        for field in ["patient_name", "age", "gender"]:
            if extracted_data[field]:
                extracted_data[field] = extracted_data[field][0]["text"]
            else:
                extracted_data[field] = None
        
        return extracted_data
    
    def extract_from_file(self, file_path: str) -> Dict:
        """Extract information from a transcription file"""
        path = Path(file_path)
        
        if path.suffix == ".json":
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Assume JSON has a 'text' or 'transcription' field
                transcription = data.get("text") or data.get("transcription") or str(data)
        else:
            # Plain text file
            with open(path, "r", encoding="utf-8") as f:
                transcription = f.read()
        
        return self.extract_from_text(transcription)
    
    def save_to_json(self, extracted_data: Dict, output_path: str):
        """Save extracted data to JSON file"""
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(extracted_data, f, indent=2, ensure_ascii=False)
        print(f"Saved extracted data to {output_path}")


def main():
    """Example usage"""
    # Sample medical transcription
    sample_transcription = """
    Patient John Doe, 45 year old male, presents with persistent cough and fever 
    for the past 5 days. Temperature is 101.5 Fahrenheit, blood pressure 130/85. 
    Patient reports difficulty breathing and chest tightness. No known allergies.
    
    Diagnosis: Suspected pneumonia. Ordered chest X-ray to confirm.
    
    Prescribed Amoxicillin 500mg three times daily for 7 days. Also recommended 
    over-the-counter fever reducer as needed.
    
    Treatment plan: Rest, increase fluid intake, monitor temperature. 
    Follow up in one week or sooner if symptoms worsen.
    """
    
    print("Initializing Medical Extractor...")
    print("Using local Dolly-3B model (CPU-friendly)")
    print("Note: First run will download the model (~6GB)\n")
    
    extractor = MedicalExtractor()
    
    print("Processing transcription...")
    result = extractor.extract_from_text(sample_transcription)
    
    print("\n" + "="*60)
    print("EXTRACTED MEDICAL INFORMATION")
    print("="*60)
    print(json.dumps(result, indent=2))
    
    # Save to file
    extractor.save_to_json(result, "extracted_medical_data.json")


if __name__ == "__main__":
    main()
