"""
Real-Time ChatGPT Voice Mode Processor
Captures conversations from ChatGPT voice mode and processes them through MediScribe
"""
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict
from medical_extractor_simple import MedicalExtractor
from database_saver import MedicalRecordDB


class ChatGPTVoiceProcessor:
    """Process conversations from ChatGPT voice mode in real-time"""
    
    def __init__(self, use_translation: bool = True):
        """
        Initialize the processor
        
        Args:
            use_translation: Whether to enable multilingual translation
        """
        print("🚀 Initializing ChatGPT Voice Mode Processor...")
        print("="*70)
        
        # Initialize components
        self.extractor = MedicalExtractor()
        self.db = MedicalRecordDB()
        
        # Initialize translator if requested
        self.translator = None
        if use_translation:
            try:
                from translator import MultilingualTranslator
                self.translator = MultilingualTranslator(translation_method="nllb")
                print("✓ Multilingual translation enabled")
                print("  Supported: Shona, Ndebele, Zulu, Xhosa, Afrikaans")
            except Exception as e:
                print(f"⚠️  Translation not available: {e}")
                print("  Continuing with English-only mode")
        else:
            print("✓ English-only mode")
        
        print("✓ Medical data extractor ready")
        print("✓ Database connection ready")
        print("="*70)
        print()
    
    def process_conversation(self, conversation_text: str, auto_save: bool = True) -> Dict:
        """
        Process a conversation and extract medical data
        
        Args:
            conversation_text: The conversation transcript from ChatGPT voice mode
            auto_save: Whether to automatically save to database
            
        Returns:
            Extracted medical data
        """
        print("\n" + "="*70)
        print(f"📝 PROCESSING CONVERSATION")
        print(f"   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70)
        
        # Step 1: Language detection and translation
        original_language = "english"
        translated_text = conversation_text
        
        if self.translator:
            print("\n🔍 Detecting language...")
            original_language = self.translator.detect_language(conversation_text)
            print(f"   Detected: {original_language.title()}")
            
            if original_language != "english":
                print(f"\n🌐 Translating to English...")
                translated_text, _ = self.translator.translate(conversation_text, original_language)
                print("   ✓ Translation complete")
            else:
                print("   ✓ Already in English")
        
        # Step 2: Extract medical data
        print("\n🔬 Extracting medical data...")
        extracted_data = self.extractor.extract_from_text(translated_text)
        
        # Add metadata
        extracted_data["original_language"] = original_language
        extracted_data["processed_at"] = datetime.now().isoformat()
        extracted_data["source"] = "chatgpt_voice_mode"
        
        if original_language != "english":
            extracted_data["original_text"] = conversation_text
            extracted_data["translated_text"] = translated_text
        
        print("   ✓ Extraction complete")
        
        # Step 3: Save to database if requested
        if auto_save:
            print("\n💾 Saving to database...")
            record_id = self.db.add_record(extracted_data)
            extracted_data["record_id"] = record_id
            print(f"   ✓ Saved as: {record_id}")
        
        # Display summary
        self._display_summary(extracted_data)
        
        return extracted_data
    
    def _display_summary(self, data: Dict):
        """Display a summary of extracted data"""
        print("\n" + "="*70)
        print("📊 EXTRACTED DATA SUMMARY")
        print("="*70)
        
        if data.get("patient_name"):
            print(f"👤 Patient: {data['patient_name']}")
        else:
            print("👤 Patient: Not identified")
        
        if data.get("age"):
            print(f"📅 Age: {data['age']}")
        
        if data.get("gender"):
            print(f"⚧  Gender: {data['gender']}")
        
        if data.get("symptoms"):
            symptoms = [s['text'] for s in data['symptoms']]
            print(f"\n🤒 Symptoms ({len(symptoms)}):")
            for symptom in symptoms:
                print(f"   • {symptom}")
        
        if data.get("diagnosis"):
            diagnoses = [d['text'] for d in data['diagnosis']]
            print(f"\n🏥 Diagnosis ({len(diagnoses)}):")
            for diagnosis in diagnoses:
                print(f"   • {diagnosis}")
        
        if data.get("medications"):
            meds = [m['text'] for m in data['medications']]
            print(f"\n💊 Medications ({len(meds)}):")
            for med in meds:
                print(f"   • {med}")
        
        if data.get("vital_signs"):
            vitals = [v['text'] for v in data['vital_signs']]
            print(f"\n📈 Vital Signs ({len(vitals)}):")
            for vital in vitals:
                print(f"   • {vital}")
        
        print("="*70)
    
    def process_from_input(self, auto_save: bool = True):
        """
        Interactive mode: paste conversation and process
        
        Args:
            auto_save: Whether to save to database
        """
        print("\n" + "="*70)
        print("📋 PASTE CONVERSATION MODE")
        print("="*70)
        print("Instructions:")
        print("1. Copy your conversation from ChatGPT voice mode")
        print("2. Paste it below (press Enter, then Ctrl+Z and Enter on Windows)")
        print("3. The conversation will be processed automatically")
        print("="*70)
        print("\nPaste conversation here:")
        
        # Read multi-line input
        lines = []
        try:
            while True:
                line = input()
                lines.append(line)
        except EOFError:
            pass
        
        conversation_text = "\n".join(lines)
        
        if conversation_text.strip():
            return self.process_conversation(conversation_text, auto_save)
        else:
            print("\n❌ No conversation text provided")
            return None
    
    def process_from_file(self, file_path: str, auto_save: bool = True) -> Dict:
        """
        Process a conversation from a file
        
        Args:
            file_path: Path to conversation file
            auto_save: Whether to save to database
            
        Returns:
            Extracted medical data
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        print(f"\n📄 Reading file: {file_path}")
        
        with open(path, "r", encoding="utf-8") as f:
            conversation_text = f.read()
        
        return self.process_conversation(conversation_text, auto_save)
    
    def save_conversation_log(self, conversation_text: str, extracted_data: Dict, 
                            output_dir: str = "conversation_logs"):
        """
        Save conversation and extracted data to log files
        
        Args:
            conversation_text: Original conversation
            extracted_data: Extracted medical data
            output_dir: Directory to save logs
        """
        log_dir = Path(output_dir)
        log_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save original conversation
        conv_file = log_dir / f"conversation_{timestamp}.txt"
        with open(conv_file, "w", encoding="utf-8") as f:
            f.write(f"Timestamp: {datetime.now().isoformat()}\n")
            f.write(f"Source: ChatGPT Voice Mode\n")
            f.write("="*70 + "\n\n")
            f.write(conversation_text)
        
        # Save extracted data
        data_file = log_dir / f"extracted_{timestamp}.json"
        with open(data_file, "w", encoding="utf-8") as f:
            json.dump(extracted_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n📁 Logs saved:")
        print(f"   Conversation: {conv_file}")
        print(f"   Extracted data: {data_file}")
    
    def view_recent_records(self, limit: int = 5):
        """View recent medical records"""
        records = self.db.get_all_records(limit=limit)
        
        if not records:
            print("\n📭 No records in database")
            return
        
        print(f"\n📊 Recent Records (showing {len(records)}):")
        print("="*70)
        
        for record in records:
            print(f"\n🆔 {record['record_id']}")
            print(f"   Patient: {record.get('patient_name', 'Unknown')}")
            print(f"   Date: {record['timestamp'][:10]}")
            if record.get('diagnosis'):
                print(f"   Diagnosis: {', '.join(record['diagnosis'])}")
        
        print("="*70)


def main():
    """Main entry point with menu"""
    print("\n" + "="*70)
    print("  __  __          _ _ ____            _ _          ")
    print(" |  \\/  | ___  __| (_) ___|  ___ _ __(_) |__   ___ ")
    print(" | |\\/| |/ _ \\/ _` | \\___ \\ / __| '__| | '_ \\ / _ \\")
    print(" | |  | |  __/ (_| | |___) | (__| |  | | |_) |  __/")
    print(" |_|  |_|\\___|\\__,_|_|____/ \\___|_|  |_|_.__/ \\___|")
    print("\n ChatGPT Voice Mode - Real-Time Medical Data Extraction")
    print("="*70)
    
    # Initialize processor
    processor = ChatGPTVoiceProcessor(use_translation=True)
    
    # Menu
    while True:
        print("\n" + "="*70)
        print("MENU")
        print("="*70)
        print("1. Process conversation (paste mode)")
        print("2. Process from file")
        print("3. View recent records")
        print("4. Test with sample conversation")
        print("5. Exit")
        print("="*70)
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == "1":
            result = processor.process_from_input(auto_save=True)
            if result:
                save_log = input("\nSave conversation log? (y/n): ").strip().lower()
                if save_log == "y":
                    # Need to get original text - for now skip
                    print("✓ Data saved to database")
        
        elif choice == "2":
            file_path = input("\nEnter file path: ").strip()
            try:
                result = processor.process_from_file(file_path, auto_save=True)
            except Exception as e:
                print(f"\n❌ Error: {e}")
        
        elif choice == "3":
            limit = input("\nNumber of records to show (default 5): ").strip()
            limit = int(limit) if limit.isdigit() else 5
            processor.view_recent_records(limit)
        
        elif choice == "4":
            # Sample conversation
            sample = """
            Doctor: Good morning! What brings you in today?
            
            Patient: Hi doctor. I'm Sarah Johnson, I'm 28 years old. I've been feeling really sick 
            for the past few days. I have a terrible headache and I've been running a fever.
            
            Doctor: I see. Let me check your vitals. Your temperature is 101.5 Fahrenheit, 
            and your blood pressure is 125/80. How long have you had the headache?
            
            Patient: About 3 days now. It's constant and quite painful. I also have a dry cough 
            and my whole body aches.
            
            Doctor: Any other symptoms? Sore throat, difficulty breathing?
            
            Patient: Yes, my throat is a bit sore, but breathing is okay.
            
            Doctor: Based on your symptoms and examination, I believe you have a viral infection, 
            possibly the flu. I'm going to prescribe you Ibuprofen 400mg for the fever and pain, 
            take it three times daily with food. Also, I'll give you some cough syrup - 
            take 10ml every 6 hours as needed.
            
            Patient: Should I come back for a follow-up?
            
            Doctor: Yes, if your symptoms don't improve in 3-4 days, or if they get worse, 
            please come back immediately. Otherwise, you should start feeling better soon. 
            Make sure to rest and drink plenty of fluids.
            
            Patient: Thank you, doctor.
            
            Doctor: You're welcome. Take care and feel better soon!
            """
            
            print("\n📝 Processing sample conversation...")
            result = processor.process_conversation(sample, auto_save=True)
        
        elif choice == "5":
            print("\n👋 Goodbye!")
            break
        
        else:
            print("\n❌ Invalid option. Please select 1-5.")


if __name__ == "__main__":
    main()
