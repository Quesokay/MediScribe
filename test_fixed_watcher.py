"""
Test the fixed watcher to ensure it doesn't process its own output files
"""
import time
from pathlib import Path

# Create a test transcript
test_file = Path("Vibe_Transcripts/test_fixed.txt")
test_content = """
Patient Michael Brown, 28 year old male.
Presents with sore throat and fever for 3 days.
Temperature 100.2 Fahrenheit, blood pressure 118/75.

Diagnosis: Strep throat.
Prescribed Amoxicillin 500mg three times daily for 10 days.

Treatment plan: Rest, drink plenty of fluids, complete full course of antibiotics.
Follow up if symptoms don't improve in 48 hours.
"""

print("Creating test transcript...")
with open(test_file, "w") as f:
    f.write(test_content.strip())

print(f"✓ Created: {test_file}")
print("\nIf vibe_watcher.py is running, it should:")
print("  1. Detect test_fixed.txt")
print("  2. Process it")
print("  3. Create test_fixed_mediscribe.json")
print("  4. NOT process the JSON file (this was the bug)")
print("\nCheck the Vibe_Transcripts folder in a few seconds...")
print("You should see exactly 2 new files:")
print("  - test_fixed.txt (original)")
print("  - test_fixed_mediscribe.json (extracted data)")
print("\nIf you see test_fixed_mediscribe_mediscribe.json, the bug is still there!")
