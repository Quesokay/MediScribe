"""
Vibe-MediScribe Integration Service
Watches a directory for new Vibe transcripts and automatically processes them
"""
import time
import json
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from medical_extractor_simple import MedicalExtractor
from database_saver import MedicalRecordDB


class VibeTranscriptHandler(FileSystemEventHandler):
    """Handles new transcript files from Vibe"""
    
    def __init__(self, config: dict):
        self.config = config
        self.extractor = MedicalExtractor()
        self.db = MedicalRecordDB()
        self.processed_files = set()
        
        # Load previously processed files
        self._load_processed_files()
        
        print("✓ Vibe-MediScribe Integration Active")
        print(f"✓ Watching: {config['watch_directory']}")
        print(f"✓ File types: {', '.join(config['file_extensions'])}")
        print(f"✓ Auto-process: {'ON' if config['auto_process'] else 'OFF'}\n")
    
    def _load_processed_files(self):
        """Load list of already processed files"""
        processed_log = Path("processed_files.json")
        if processed_log.exists():
            with open(processed_log, "r") as f:
                self.processed_files = set(json.load(f))
    
    def _save_processed_files(self):
        """Save list of processed files"""
        with open("processed_files.json", "w") as f:
            json.dump(list(self.processed_files), f, indent=2)
    
    def on_created(self, event):
        """Called when a new file is created"""
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        
        # Check if file extension matches
        if file_path.suffix not in self.config['file_extensions']:
            return
        
        # Check if already processed
        if str(file_path) in self.processed_files:
            return
        
        # Wait a bit to ensure file is fully written
        time.sleep(1)
        
        self.process_transcript(file_path)
    
    def on_modified(self, event):
        """Called when a file is modified (Vibe might save incrementally)"""
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        
        # Only process if configured and not already processed
        if (file_path.suffix in self.config['file_extensions'] and 
            str(file_path) not in self.processed_files and
            self.config.get('process_on_modify', False)):
            
            time.sleep(1)
            self.process_transcript(file_path)
    
    def process_transcript(self, file_path: Path):
        """Process a transcript file with MediScribe"""
        try:
            print(f"\n{'='*70}")
            print(f"📄 New transcript detected: {file_path.name}")
            print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"{'='*70}\n")
            
            # Extract medical information
            print("🔍 Extracting medical information...")
            result = self.extractor.extract_from_file(str(file_path))
            
            # Display key findings
            print("\n✓ Extraction complete!")
            if result.get('patient_name'):
                print(f"  👤 Patient: {result['patient_name']}")
            if result.get('age'):
                print(f"  📅 Age: {result['age']}")
            if result.get('gender'):
                print(f"  ⚧ Gender: {result['gender']}")
            if result.get('diagnosis'):
                diagnoses = [d['text'] for d in result['diagnosis']]
                print(f"  🏥 Diagnosis: {', '.join(diagnoses)}")
            if result.get('medications'):
                meds = [m['text'] for m in result['medications']]
                print(f"  💊 Medications: {', '.join(meds)}")
            
            # Save to database
            print("\n💾 Saving to database...")
            record_id = self.db.add_record(result)
            
            # Save extracted JSON if configured
            if self.config.get('save_extracted_json', True):
                json_path = file_path.parent / f"{file_path.stem}_mediscribe.json"
                self.extractor.save_to_json(result, str(json_path))
                print(f"✓ Saved extracted data: {json_path.name}")
            
            # Mark as processed
            self.processed_files.add(str(file_path))
            self._save_processed_files()
            
            print(f"\n✅ Successfully processed and saved as {record_id}")
            print(f"{'='*70}\n")
            
            # Play notification sound if configured
            if self.config.get('notification_sound', False):
                self._play_notification()
            
        except Exception as e:
            print(f"\n❌ Error processing {file_path.name}: {e}")
            print(f"{'='*70}\n")
    
    def _play_notification(self):
        """Play a notification sound (optional)"""
        try:
            import winsound
            winsound.MessageBeep(winsound.MB_ICONASTERISK)
        except:
            pass  # Silently fail if not on Windows or winsound not available


def load_config(config_path: str = "vibe_config.json") -> dict:
    """Load configuration from JSON file"""
    config_file = Path(config_path)
    
    if not config_file.exists():
        # Create default config
        default_config = {
            "watch_directory": str(Path.home() / "Documents" / "Vibe Transcripts"),
            "file_extensions": [".txt", ".srt", ".vtt", ".json"],
            "auto_process": True,
            "process_on_modify": False,
            "save_extracted_json": True,
            "notification_sound": True,
            "database_path": "medical_records.json"
        }
        
        with open(config_file, "w") as f:
            json.dump(default_config, f, indent=2)
        
        print(f"✓ Created default config: {config_path}")
        print(f"✓ Edit this file to customize settings\n")
        
        return default_config
    
    with open(config_file, "r") as f:
        return json.load(f)


def main():
    """Main entry point"""
    print("\n" + "="*70)
    print("  🎙️  VIBE-MEDISCRIBE INTEGRATION SERVICE")
    print("="*70)
    print("  Automatically processes Vibe transcripts with MediScribe")
    print("  Press Ctrl+C to stop\n")
    
    # Load configuration
    config = load_config()
    
    # Ensure watch directory exists
    watch_dir = Path(config['watch_directory'])
    if not watch_dir.exists():
        print(f"⚠️  Watch directory doesn't exist: {watch_dir}")
        print(f"Creating directory...")
        watch_dir.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created: {watch_dir}\n")
    
    # Set up file watcher
    event_handler = VibeTranscriptHandler(config)
    observer = Observer()
    observer.schedule(event_handler, str(watch_dir), recursive=False)
    observer.start()
    
    try:
        print("👀 Monitoring for new transcripts...")
        print("💡 Tip: Configure Vibe to save transcripts to the watch directory\n")
        
        while True:
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping Vibe-MediScribe Integration...")
        observer.stop()
        observer.join()
        print("✓ Service stopped\n")


if __name__ == "__main__":
    main()
