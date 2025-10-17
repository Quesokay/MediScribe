# Quick Start Guide

## ✅ You're All Set!

The lightweight version is working on your CPU. Here's what to do next:

## Test It Now

```bash
# Test with built-in example
python medical_extractor_simple.py

# Test with sample file
python test_with_sample.py
```

## Use with Your Vibe Transcriptions

### Step 1: Transcribe with Vibe
- Record doctor's audio notes in Vibe
- Export as `.txt` or `.json` file

### Step 2: Process the Transcription

```python
from medical_extractor_simple import MedicalExtractor

extractor = MedicalExtractor()
result = extractor.extract_from_file("your_vibe_file.txt")

# See what was extracted
import json
print(json.dumps(result, indent=2))
```

### Step 3: Save to Database

```python
from database_saver import MedicalRecordDB

db = MedicalRecordDB()
record_id = db.add_record(result)
print(f"Saved as {record_id}")
```

## Complete Workflow Example

```python
from medical_extractor_simple import MedicalExtractor
from database_saver import MedicalRecordDB

# Initialize
extractor = MedicalExtractor()
db = MedicalRecordDB()

# Process Vibe transcription
result = extractor.extract_from_file("doctor_notes.txt")

# Save to database
record_id = db.add_record(result)

# Later: Search for patient records
patient_records = db.search_by_patient("John Doe")
for record in patient_records:
    print(f"Visit on {record['timestamp']}")
    print(f"Diagnosis: {record['diagnosis']}")
```

## What You Get

The extractor automatically finds:
- ✓ Patient name, age, gender
- ✓ Symptoms (fever, cough, pain, etc.)
- ✓ Diagnosis
- ✓ Medications and dosages
- ✓ Vital signs (BP, temp, heart rate)
- ✓ Allergies
- ✓ Treatment plan
- ✓ Follow-up instructions

## Performance

- **Speed**: 1-2 seconds per transcription
- **No GPU needed**: Runs on any CPU
- **Memory**: ~500MB RAM
- **Privacy**: Everything stays on your machine

## Tips for Best Results

1. **Structured notes work best**: "Patient John Doe, 45 year old male..."
2. **Use medical terms**: "Temperature 101.5F" vs "really hot"
3. **Clear sections**: "Diagnosis:", "Prescribed:", "Treatment plan:"
4. **Consistent format**: Same structure for each transcription

## Customize for Your Needs

### Add More Symptoms

Edit `medical_extractor_simple.py` line 73:

```python
symptom_keywords = [
    'cough', 'fever', 'pain', 'headache',
    'your_custom_symptom',  # Add here
]
```

### Add More Medical Terms

Add patterns in `_add_medical_patterns()` method.

## Need Help?

- Check `README_SIMPLE.md` for full documentation
- See `sample_transcription.txt` for example format
- Run `test_with_sample.py` to see it in action

## Next: Build Your App

Now you can:
1. Create a simple UI for doctors
2. Integrate with your EHR system
3. Add more medical term recognition
4. Export to PDF/DOCX for records
5. Add user authentication
6. Deploy to a server for team use

The foundation is ready - build what you need on top!
