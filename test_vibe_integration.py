"""
Test script for Vibe-MediScribe integration
Creates a sample transcript in the watch directory to test the integration
"""
import json
from pathlib import Path
from datetime import datetime


def create_test_transcript():
    """Create a test transcript file"""
    
    # Load config to get watch directory
    config_path = Path("vibe_config.json")
    if config_path.exists():
        with open(config_path, "r") as f:
            config = json.load(f)
        watch_dir = Path(config['watch_directory'])
    else:
        watch_dir = Path.home() / "Documents" / "Vibe Transcripts"
    
    # Ensure directory exists
    watch_dir.mkdir(parents=True, exist_ok=True)
    
    # Sample medical transcription
    sample_text = """
Patient Sarah Johnson, 32 year old female, presents with severe headache and nausea 
for the past 2 days. Temperature is 99.8 Fahrenheit, blood pressure 125/80. 
Patient reports sensitivity to light and occasional dizziness. No known allergies.

Diagnosis: Migraine headache. Ordered blood work to rule out other causes.

Prescribed Sumatriptan 50mg as needed for migraine attacks, maximum 2 doses per day.
Also recommended over-the-counter ibuprofen 400mg for pain management.

Treatment plan: Rest in dark, quiet room. Stay hydrated. Avoid triggers like 
bright lights and loud noises. Keep a headache diary to identify patterns.

Follow up in two weeks or sooner if symptoms worsen or new symptoms develop.
"""
    
    # Create test file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    test_file = watch_dir / f"test_transcript_{timestamp}.txt"
    
    with open(test_file, "w", encoding="utf-8") as f:
        f.write(sample_text.strip())
    
    print("="*70)
    print("TEST TRANSCRIPT CREATED")
    print("="*70)
    print(f"✓ File: {test_file}")
    print(f"✓ Location: {watch_dir}")
    print("\nIf vibe_watcher.py is running, it should detect and process this file.")
    print("\nTo verify:")
    print("  1. Check the console output of vibe_watcher.py")
    print("  2. Run: python view_database.py")
    print(f"  3. Look for: {test_file.stem}_mediscribe.json")
    print("="*70)


if __name__ == "__main__":
    create_test_transcript()
