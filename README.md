# Medical Transcription Extractor

Extract structured medical information from audio transcriptions using spacy-llm.

## Features

- Extract patient information (name, age, gender)
- Identify symptoms, diagnoses, medications
- Capture vital signs and allergies
- Extract treatment plans and follow-up instructions
- Save structured data to database

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

**Note:** First run will download Dolly-3B model (~6GB). Requirements:
- **CPU only** - No GPU needed!
- ~10GB free disk space
- 8GB+ RAM recommended

### 2. Model Options for CPU

**Default: Dolly-3B (CPU-optimized)**
- Uses `config.cfg`
- Runs on CPU (no GPU required)
- ~6GB model size
- Reasonable speed on modern CPUs
- No API keys needed
- HIPAA compliant (data never leaves your system)

**Alternative CPU-friendly models:**

Edit `config.cfg` to try:

```ini
# Smaller and faster (less accurate)
[components.llm.model]
@llm_models = "spacy.StableLM.v1"
name = "stabilityai/stablelm-base-alpha-3b"
```

```ini
# Better accuracy (slower on CPU)
[components.llm.model]
@llm_models = "spacy.OpenLLaMA.v1"
name = "openlm-research/open_llama_3b"
```

## Usage

### Basic Example

```python
from medical_extractor import MedicalExtractor

# Initialize
extractor = MedicalExtractor("config.cfg")

# Extract from text
transcription = "Patient John Doe, 45 year old male..."
result = extractor.extract_from_text(transcription)

print(result)
```

### Process Vibe Transcription Files

```python
# From text file
result = extractor.extract_from_file("transcription.txt")

# From JSON file (if Vibe exports JSON)
result = extractor.extract_from_file("transcription.json")
```

### Save to Database

```python
from database_saver import MedicalRecordDB

db = MedicalRecordDB()
record_id = db.add_record(result)

# Search records
records = db.search_by_patient("John Doe")
```

## Run Examples

```bash
# Test extraction
python medical_extractor.py

# Test database integration
python database_saver.py
```

## Integration with Vibe

1. Use Vibe to transcribe audio
2. Export transcription as text or JSON
3. Process with this tool:

```python
extractor = MedicalExtractor()
result = extractor.extract_from_file("vibe_output.txt")

db = MedicalRecordDB()
db.add_record(result)
```

## Customization

### Add More Fields

Edit `config.cfg` to add custom labels:

```ini
[components.llm.task]
labels = ["PATIENT_NAME", "YOUR_CUSTOM_FIELD", ...]

[components.llm.task.label_definitions]
YOUR_CUSTOM_FIELD = "Description of what to extract"
```

### Use Different Models

All models run locally on CPU:
- **Dolly-3B** (default) - Good balance for CPU
- **StableLM-3B** - Faster, lighter
- **OpenLLaMA-3B** - Better accuracy, slower

⚠️ **Note:** Processing will be slower on CPU (30-60 seconds per transcription). For production with many transcriptions, consider:
- Using a cloud VM with GPU
- Batch processing overnight
- Upgrading to a machine with GPU

## Privacy & Compliance

⚠️ **Important for Medical Data:**

- Use local models for HIPAA compliance
- Never send PHI to public APIs without proper agreements
- Encrypt database storage
- Implement access controls
- Audit all data access

## Next Steps

- [ ] Add real database (PostgreSQL, MongoDB)
- [ ] Implement user authentication
- [ ] Add data validation and error handling
- [ ] Create web interface for doctors
- [ ] Add export to EHR systems
- [ ] Implement audit logging
