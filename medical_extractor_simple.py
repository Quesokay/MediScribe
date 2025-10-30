"""
Medical Transcription Information Extractor - Lightweight Version
Uses spaCy's built-in NER + custom rules (no LLM required)
Fast and works on CPU
"""
import spacy
from spacy.matcher import Matcher
from spacy.tokens import Span
import re
import json
from pathlib import Path
from typing import Dict, List


class MedicalExtractor:
    def __init__(self):
        """Initialize with spaCy's standard model + custom medical patterns"""
        import sys
        print("Loading spaCy model...", file=sys.stderr)
        self.nlp = spacy.load("en_core_web_sm")
        
        # Add custom entity ruler for medical terms
        self._add_medical_patterns()
        
    def _add_medical_patterns(self):
        """Add patterns for medical entity recognition"""
        # Create matcher for patterns
        self.matcher = Matcher(self.nlp.vocab)
        
        # Vital signs patterns
        vital_patterns = [
            [{"LIKE_NUM": True}, {"LOWER": {"IN": ["fahrenheit", "f", "celsius", "c"]}}],
            [{"LOWER": "temperature"}, {"IS_PUNCT": True, "OP": "?"}, {"LIKE_NUM": True}],
            [{"LOWER": "bp"}, {"IS_PUNCT": True, "OP": "?"}, {"LIKE_NUM": True}],
            [{"LOWER": {"IN": ["blood", "pressure"]}}, {"IS_PUNCT": True, "OP": "?"}, {"LIKE_NUM": True}],
            [{"LIKE_NUM": True}, {"ORTH": "/"}, {"LIKE_NUM": True}],  # BP format
            [{"LOWER": {"IN": ["heart", "pulse"]}}, {"LOWER": "rate"}],
        ]
        self.matcher.add("VITAL_SIGNS", vital_patterns)
        
        # Medication dosage patterns
        dosage_patterns = [
            [{"LIKE_NUM": True}, {"LOWER": {"IN": ["mg", "mcg", "g", "ml"]}}],
            [{"LOWER": {"IN": ["twice", "three", "once"]}}, {"LOWER": {"IN": ["daily", "day"]}}],
            [{"LIKE_NUM": True}, {"LOWER": "times"}, {"LOWER": {"IN": ["daily", "day", "per"]}}],
        ]
        self.matcher.add("DOSAGE", dosage_patterns)
        
    def extract_from_text(self, transcription: str) -> Dict:
        """Extract structured medical information from transcription text"""
        doc = self.nlp(transcription)
        
        # Apply custom matchers
        matches = self.matcher(doc)
        
        # Initialize result structure
        extracted_data = {
            "patient_name": None,
            "age": None,
            "gender": None,
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
        
        # Extract patient name - try multiple patterns
        # Pattern 1: "I am [Name]" or "My name is [Name]"
        name_pattern1 = re.search(r'(?:I am|my name is|I\'m)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', transcription, re.IGNORECASE)
        if name_pattern1:
            extracted_data["patient_name"] = name_pattern1.group(1).strip()
        
        # Pattern 2: "Patient: [Name]" at start of line
        name_pattern2 = re.search(r'Patient:\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', transcription)
        if name_pattern2 and not extracted_data["patient_name"]:
            extracted_data["patient_name"] = name_pattern2.group(1).strip()
        
        # Pattern 3: Use spaCy NER as fallback
        if not extracted_data["patient_name"]:
            for ent in doc.ents:
                if ent.label_ == "PERSON":
                    # Skip if it's "Doctor" or "Patient"
                    if ent.text.lower() not in ['doctor', 'patient', 'dr']:
                        extracted_data["patient_name"] = ent.text
                        break
        
        # Extract age - multiple patterns
        age_match = re.search(r'(\d+)\s*year\s*old', transcription, re.IGNORECASE)
        if not age_match:
            age_match = re.search(r'I am (\d+)|I\'m (\d+)|age[:\s]+(\d+)', transcription, re.IGNORECASE)
        if age_match:
            extracted_data["age"] = age_match.group(1) or age_match.group(2) or age_match.group(3)
        
        # Extract gender
        gender_match = re.search(r'\b(male|female|man|woman)\b', transcription, re.IGNORECASE)
        if gender_match:
            gender = gender_match.group(1).lower()
            if gender in ['male', 'man']:
                extracted_data["gender"] = "male"
            elif gender in ['female', 'woman']:
                extracted_data["gender"] = "female"
        
        # Extract symptoms (look for common symptom keywords)
        symptom_keywords = ['cough', 'fever', 'pain', 'headache', 'nausea', 'vomiting', 
                           'dizziness', 'fatigue', 'weakness', 'breathing', 'chest tightness',
                           'sore throat', 'runny nose', 'congestion', 'ache', 'hurt', 'sick']
        
        # Also look for "I have [symptom]" or "feeling [symptom]" patterns
        symptom_pattern = re.findall(r'(?:I have|I\'m feeling|feeling|experiencing|suffering from)\s+(?:a\s+)?([a-z\s]+?)(?:\.|,|and|$)', transcription, re.IGNORECASE)
        for symptom in symptom_pattern:
            symptom = symptom.strip()
            if symptom and len(symptom) < 50:  # Reasonable length
                extracted_data["symptoms"].append({
                    "text": symptom,
                    "context": symptom
                })
        
        # Keyword-based extraction
        for keyword in symptom_keywords:
            if keyword in transcription.lower():
                # Find the sentence containing the symptom
                for sent in doc.sents:
                    if keyword in sent.text.lower():
                        extracted_data["symptoms"].append({
                            "text": keyword,
                            "context": sent.text.strip()
                        })
                        break
        
        # Extract diagnosis (look after "diagnosis:" or "suspected")
        diagnosis_match = re.search(r'diagnosis[:\s]+([^.]+)', transcription, re.IGNORECASE)
        if diagnosis_match:
            extracted_data["diagnosis"].append({
                "text": diagnosis_match.group(1).strip()
            })
        
        # Extract medications (look for "prescribed" or common drug patterns)
        med_match = re.findall(r'prescribed\s+(\w+)', transcription, re.IGNORECASE)
        for med in med_match:
            extracted_data["medications"].append({"text": med})
        
        # Extract allergies
        allergy_match = re.search(r'allerg(?:y|ies)[:\s]+([^.]+)', transcription, re.IGNORECASE)
        if allergy_match:
            allergy_text = allergy_match.group(1).strip()
            if 'no known' not in allergy_text.lower():
                extracted_data["allergies"].append({"text": allergy_text})
        
        # Extract vital signs using matcher
        for match_id, start, end in matches:
            span = doc[start:end]
            label = self.nlp.vocab.strings[match_id]
            
            if label == "VITAL_SIGNS":
                extracted_data["vital_signs"].append({
                    "text": span.text,
                    "start": span.start_char,
                    "end": span.end_char
                })
            elif label == "DOSAGE":
                extracted_data["dosages"].append({
                    "text": span.text,
                    "start": span.start_char,
                    "end": span.end_char
                })
        
        # Extract treatment plan
        treatment_match = re.search(r'treatment\s+plan[:\s]+([^.]+(?:\.[^.]+)?)', transcription, re.IGNORECASE)
        if treatment_match:
            extracted_data["treatment_plan"].append({
                "text": treatment_match.group(1).strip()
            })
        
        # Extract follow-up
        followup_match = re.search(r'follow[\s-]up[:\s]+([^.]+)', transcription, re.IGNORECASE)
        if followup_match:
            extracted_data["follow_up"].append({
                "text": followup_match.group(1).strip()
            })
        
        # Remove duplicates
        for key in ["symptoms", "vital_signs", "dosages"]:
            seen = set()
            unique = []
            for item in extracted_data[key]:
                text = item.get("text", "").lower()
                if text and text not in seen:
                    seen.add(text)
                    unique.append(item)
            extracted_data[key] = unique
        
        return extracted_data
    
    def extract_from_file(self, file_path: str) -> Dict:
        """Extract information from a transcription file"""
        path = Path(file_path)
        
        if path.suffix == ".json":
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                transcription = data.get("text") or data.get("transcription") or str(data)
        else:
            with open(path, "r", encoding="utf-8") as f:
                transcription = f.read()
        
        return self.extract_from_text(transcription)
    
    def save_to_json(self, extracted_data: Dict, output_path: str):
        """Save extracted data to JSON file"""
        import sys
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(extracted_data, f, indent=2, ensure_ascii=False)
        print(f"Saved extracted data to {output_path}", file=sys.stderr)


def main():
    """Example usage"""
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
    
    print("="*60)
    print("MEDICAL TRANSCRIPTION EXTRACTOR - Lightweight Version")
    print("="*60)
    print("No LLM required - Fast CPU processing")
    print("Uses spaCy + custom medical patterns\n")
    
    extractor = MedicalExtractor()
    
    print("Processing transcription...\n")
    result = extractor.extract_from_text(sample_transcription)
    
    print("="*60)
    print("EXTRACTED MEDICAL INFORMATION")
    print("="*60)
    print(json.dumps(result, indent=2))
    
    # Save to file
    extractor.save_to_json(result, "extracted_medical_data.json")
    print("\nProcessing complete!")


if __name__ == "__main__":
    main()
