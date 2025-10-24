"""
Real-Time Conversation Processor for Medical Data Extraction
Captures conversations from ChatGPT voice mode, translates if needed, and extracts medical data
"""
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict
import pyperclip  # For clipboard monitoring
from medical_extractor_simple import MedicalExtractor
from database_saver import MedicalRecordDB


class RealtimeConversationProcessor:
    """Process real-time conversations and extract medical data"""
    
    def __init__(self, use_nllb: bool = True):
        """
        Initialize the processor
        
        Args:
            use_nllb: Whether to use NLLB for translation (requires model download)
        """
        print("🚀 Initializing Real-Time Conversation Processor...")
        
        # Initialize components
        self.extractor = MedicalExtractor()
        self.db = MedicalRecordDB()
        self.use_nllb = use_nllb
        
        # Initialize translator
        if use_nllb:
            try:
                from translator import NLLBTranslator
                self.translator = NLLBTranslator()
                print("✓ NLLB translator loaded")
            except Exception as e:
                print(f"⚠️  NLLB not available: {e}")
                print("   Falling back to simple translator...")
                from translator_simple import SimpleTranslator
                self.translator = SimpleTranslator()
        else:
            from translator_simple import SimpleTranslator
            self.translator = SimpleTranslator()
            print("✓ Simple translator loaded")
        
        # Conversation buffer
        self.conversation_buffer = []
        self.last_clipboard = ""
        
        print("✓ Processor ready!\n")
    
    def process_conversation(self, conversation_text: str, auto_save: bool = True) -> Dict:
        """
        Process a conversation and extract medical data
        
        Args:
            conversation_text: The conversation transcript
            auto_save: Whether to automatically save to database
            
        Returns:
            Extracted medical data
        """
        print("\n" + "="*70)
        print(f"📝 Processing conversation at {datetime.now().strftime('%H:%M:%S')}")
        print("="*70)
        
        # Step 1: Detect language
        detected_lang = self.translator.detect_language(conversation_text)
        print(f"🔍 Detected language: {detected_lang}")
        
        # Step 2: Translate if needed
        if detected_lang != "english":
            print(f"🌐 Translating to English...")
            translated_text, _ = self.translator.translate(conversation_text)
            print("✓ Translation complete")
        else:
            translated_text = conversation_text
            print("✓ Already in English")
        
        # Step 3: Extract medical data
        print("🔬 Extracting medical data...")
        extracted_data = self.extractor.extract_from_text(translated_text)
        
        # Add metadata
        extracted_data["original_language"] = detected_lang
        extracted_data["processed_at"] = datetime.now().isoformat()
        
        print("✓ Extraction complete")
        
        # Step 4: Save to database if requested
        if auto_save:
            record_id = self.db.add_record(extracted_data)
            extracted_data["record_id"] = record_id
            print(f"💾 Saved to database: {record_id}")
        
        # Display summary
        self._display_summary(extracted_data)
        
        return extracted_data
    
    def _display_summary(self, data: Dict):
        """Display a summary of extracted data"""
        print("\n" + "-"*70)
        print("📊 EXTRACTED DATA SUMMARY")
        print("-"*70)
        
        if data.get("patient_name"):
            print(f"👤 Patient: {data['patient_name']}")
        if data.get("age"):
            print(f"📅 Age: {data['age']}")
        if data.get("gender"):
            print(f"⚧  Gender: {data['gender']}")
        
        if data.get("symptoms"):
            print(f"🤒 Symptoms: {', '.join([s['text'] for s in data['symptoms']])}")
        
        if data.get("diagnosis"):
            print(f"🏥 Diagnosis: {', '.join([d['text'] for d in data['diagnosis']])}")
        
        if data.get("medications"):
            print(f"💊 Medications: {', '.join([m['text'] for m in data['medications']])}")
        
        if data.get("vital_signs"):
            print(f"📈 Vital Signs: {', '.join([v['text'] for v in data['vital_signs']])}")
        
        print("-"*70)
    
    def monitor_clipboard(self, check_interval: int = 2):
        """
        Monitor clipboard for new conversations
        Useful when copying from ChatGPT voice mode
        
        Args:
            check_interval: Seconds between clipboard checks
        """
        print("\n" + "="*70)
        print("👀 CLIPBOARD MONITORING MODE")
        print("="*70)
        print("Instructions:")
        print("1. Have a conversation in ChatGPT voice mode")
        print("2. Copy the conversation text (Ctrl+C)")
        print("3. This script will automatically process it")
        print("4. Press Ctrl+C to stop monitoring")
        print("="*70 + "\n")
        
        try:
            while True:
                try:
                    clipboard_content = pyperclip.paste()
                    
                    # Check if clipboard has new content
                    if clipboard_content and clipboard_content != self.last_clipboard:
                        # Check if it looks like a medical conversation
                        if self._is_medical_conversation(clipboard_content):
                            print(f"\n🔔 New conversation detected!")
                            self.process_conversation(clipboard_content)
                            self.last_clipboard = clipboard_content
                        else:
                            # Update last clipboard but don't process
                            self.last_clipboard = clipboard_content
                    
                    time.sleep(check_interval)
                    
                except Exception as e:
                    print(f"⚠️  Error reading clipboard: {e}")
                    time.sleep(check_interval)
                    
        except KeyboardInterrupt:
            print("\n\n✓ Monitoring stopped")
    
    def _is_medical_conversation(self, text: str) -> bool:
        """Check if text looks like a medical conversation"""
        text_lower = text.lower()
        
        # Medical keywords
        medical_keywords = [
            "patient", "doctor", "symptom", "diagnosis", "medication",
            "fever", "pain", "cough", "treatment", "prescription",
            "blood pressure", "temperature", "heart rate",
            # Multilingual
            "murwere", "chiremba", "isiguli", "udokotela"
        ]
        
        # Check if text contains medical keywords and is long enough
        has_keywords = any(keyword in text_lower for keyword in medical_keywords)
        is_long_enough = len(text.split()) > 20
        
        return has_keywords and is_long_enough
    
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
        
        with open(path, "r", encoding="utf-8") as f:
            conversation_text = f.read()
        
        return self.process_conversation(conversation_text, auto_save)
    
    def save_conversation_log(self, conversation_text: str, output_dir: str = "conversation_logs"):
        """Save conversation to a log file"""
        log_dir = Path(output_dir)
        log_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_dir / f"conversation_{timestamp}.txt"
        
        with open(log_file, "w", encoding="utf-8") as f:
            f.write(f"Timestamp: {datetime.now().isoformat()}\n")
            f.write("="*70 + "\n\n")
            f.write(conversation_text)
        
        print(f"📄 Conversation saved to: {log_file}")
        return str(log_file)


def main():
    """Example usage and testing"""
    print("="*70)
    print("REAL-TIME CONVERSATION PROCESSOR")
    print("="*70)
    print("Process medical conversations from ChatGPT voice mode")
    print()
    
    # Initialize processor
    processor = RealtimeConversationProcessor(use_nllb=False)
    
    # Example conversation
    sample_conversation = """
    Doctor: Good morning. What brings you in today?
    
    Patient: Hi doctor. I've been feeling really unwell for the past few days.
    I have a terrible headache and I've been running a fever.
    
    Doctor: I see. Let me check your temperature. It's 101.5 Fahrenheit.
    And your blood pressure is 130/85. How long have you had the headache?
    
    Patient: About 3 days now. It's constant and quite painful.
    
    Doctor: Any other symptoms? Cough, sore throat, body aches?
    
    Patient: Yes, I have a dry cough and my whole body aches.
    
    Doctor: Okay. Based on your symptoms and examination, I believe you have
    a viral infection, possibly the flu. I'm going to prescribe you
    Ibuprofen 400mg for the fever and pain, take it three times daily.
    Also, get plenty of rest and drink lots of fluids.
    
    Patient: Should I come back for a follow-up?
    
    Doctor: Yes, if your symptoms don't improve in 3-4 days, or if they get worse,
    please come back. Otherwise, you should start feeling better soon.
    
    Patient: Thank you, doctor.
    
    Doctor: You're welcome. Take care and feel better soon.
    """
    
    print("\n📝 Processing sample conversation...\n")
    result = processor.process_conversation(sample_conversation, auto_save=True)
    
    print("\n" + "="*70)
    print("✓ Processing complete!")
    print("="*70)
    print("\nTo use with ChatGPT voice mode:")
    print("1. Run: python realtime_conversation_processor.py --monitor")
    print("2. Have your conversation in ChatGPT voice mode")
    print("3. Copy the conversation text")
    print("4. It will be automatically processed and saved!")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--monitor":
        # Start clipboard monitoring mode
        processor = RealtimeConversationProcessor(use_nllb=False)
        processor.monitor_clipboard()
    else:
        # Run demo
        main()
