# Medical Transcription Extractor - Lightweight Version

✓ **CPU-friendly** - No GPU required  
✓ **Fast** - Processes transcriptions in seconds  
✓ **No LLM** - Uses spaCy + custom medical patterns  
✓ **Privacy-first** - Everything runs locally  

## Quick Start

### 1. Install

```bash
pip install spacy python-dotenv
python -m spacy download en_core_web_sm
```

### 2. Run

```bash
# Test with built-in example
python medical_extractor_simple.py

# Test with sample file
python test_with_sample.py
```

## Usage

### Extract from Text

```python
from medical_extractor_simple import MedicalExtractor

extractor = MedicalExtractor()
transcription = "Patient John Doe, 45 year old male..."
result = extractor.extract_from_text(transcription)
print(result)
```

### Extract from Vibe Transcription File

```python
# From text file
result = extractor.extract_from_file("vibe_transcription.txt")

# From JSON file
result = extractor.extract_from_file("vibe_transcription.json")
```

### Save to Database

```python
from database_saver import MedicalRecordDB

db = MedicalRecordDB()
record_id = db.add_record(result)

# Search records
records = db.search_by_patient("John Doe")
```

## What It Extracts

- **Patient Info**: Name, age, gender
- **Symptoms**: Cough, fever, pain, nausea, etc.
- **Diagnosis**: Medical conditions identified
- **Medications**: Prescribed drugs
- **Dosages**: Medication amounts and frequency
- **Vital Signs**: Temperature, blood pressure, heart rate
- **Allergies**: Known allergies
- **Treatment Plan**: Care instructions
- **Follow-up**: Next appointment details

## Integration with Vibe

1. Use Vibe to transcribe doctor's audio notes
2. Export as text or JSON
3. Process with this tool:

```python
extractor = MedicalExtractor()
result = extractor.extract_from_file("vibe_output.txt")

db = MedicalRecordDB()
db.add_record(result)
```

## Performance

- **Speed**: ~1-2 seconds per transcription
- **RAM**: ~500MB
- **CPU**: Any modern processor
- **Accuracy**: Good for structured medical notes

## Customization

### Add More Symptoms

Edit `medical_extractor_simple.py`:

```python
symptom_keywords = ['cough', 'fever', 'your_symptom', ...]
```

### Add More Patterns

Add custom patterns to `_add_medical_patterns()`:

```python
custom_patterns = [
    [{"LOWER": "your"}, {"LOWER": "pattern"}],
]
self.matcher.add("YOUR_LABEL", custom_patterns)
```

## Comparison: Simple vs LLM Version

| Feature | Simple (This) | LLM Version |
|---------|--------------|-------------|
| Speed | ⚡ Fast (1-2s) | 🐌 Slow (30-60s) |
| CPU Usage | ✓ Low | ❌ High |
| GPU Required | ✗ No | ✓ Yes (for speed) |
| Accuracy | Good | Better |
| Setup | Easy | Complex |
| Model Size | 12MB | 6-13GB |

## When to Use Each

**Use Simple Version (this) when:**
- You have CPU-only hardware
- You need fast processing
- Your transcriptions are well-structured
- You're prototyping

**Use LLM Version when:**
- You have GPU available
- You need highest accuracy
- Transcriptions are unstructured/messy
- You're in production with complex cases

## Next Steps

- [ ] Add more medical term patterns
- [ ] Improve medication name recognition
- [ ] Add ICD-10 code mapping
- [ ] Create web interface
- [ ] Add real database (PostgreSQL)
- [ ] Implement user authentication
- [ ] Add audit logging for HIPAA compliance

## Files

- `medical_extractor_simple.py` - Main extractor (use this!)
- `database_saver.py` - Database integration
- `sample_transcription.txt` - Example transcription
- `test_with_sample.py` - Test script
- `medical_extractor.py` - LLM version (requires GPU)
