# MediScribe

**Intelligent Medical Transcription Extraction System**

Transform audio transcriptions into structured medical records automatically.

---

## Overview

MediScribe extracts structured medical information from audio transcriptions (via Vibe or other tools), organizing patient data, symptoms, diagnoses, medications, and treatment plans into a searchable database.

### 🎙️ **NEW: Seamless Vibe Integration!**

MediScribe now integrates directly with [Vibe](https://github.com/thewh1teagle/vibe) for automatic background processing:

1. **Transcribe** in Vibe (review & verify the transcript)
2. **Save** the transcript (Vibe saves to your configured folder)
3. **Done!** MediScribe automatically extracts and saves patient data

👉 **[START HERE](START_HERE.md)** | **[5-Min Setup](VIBE_QUICK_SETUP.md)** | **[Complete Guide](VIBE_INTEGRATION.md)**

## Features

✓ **Fast Processing** - Extract data in 1-2 seconds  
✓ **CPU-Friendly** - No GPU required  
✓ **Privacy-First** - All processing happens locally  
✓ **Structured Output** - Clean, organized medical records  
✓ **Batch Processing** - Handle multiple transcriptions at once  
✓ **Searchable Database** - Find patient records instantly  

## Quick Start

### Installation

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### Basic Usage

**Option 1: Automatic Integration with Vibe**
```bash
# Start the integration service (runs in background)
python vibe_watcher.py

# Or use the Windows batch file
start_vibe_integration.bat

# Then use Vibe normally - MediScribe processes automatically!
```

**Option 2: Manual Processing**
```bash
# Process a single transcription
python batch_process.py doctor_notes.txt

# View all records
python view_database.py

# Test the system
python medical_extractor_simple.py
```

## What MediScribe Extracts

- **Patient Information**: Name, age, gender
- **Symptoms**: Cough, fever, pain, nausea, etc.
- **Diagnosis**: Medical conditions identified
- **Medications**: Prescribed drugs and dosages
- **Vital Signs**: Temperature, blood pressure, heart rate
- **Allergies**: Known allergies
- **Treatment Plans**: Care instructions
- **Follow-up**: Next appointment details

## Workflow

### Manual Mode
```
Doctor speaks → Vibe transcribes → Export as .txt
                                        ↓
                    MediScribe extracts structured data
                                        ↓
                    Save to searchable database
                                        ↓
                    Query/export records anytime
```

### Automatic Mode (Vibe Integration)
```
Doctor speaks → Vibe transcribes → Review in Vibe → Save transcript
                                                            ↓
                                    MediScribe auto-detects & processes
                                                            ↓
                                    Saves to database (background)
                                                            ↓
                                    Ready to query instantly
```

## Example

**Input** (transcription.txt):
```
Patient John Doe, 45 year old male, presents with fever and cough.
Temperature 101.5F, BP 130/85.
Diagnosis: Pneumonia
Prescribed Amoxicillin 500mg three times daily.
```

**Output** (structured data):
```json
{
  "patient_name": "John Doe",
  "age": "45",
  "gender": "male",
  "symptoms": ["fever", "cough"],
  "vital_signs": ["101.5F", "130/85"],
  "diagnosis": ["Pneumonia"],
  "medications": ["Amoxicillin"],
  "dosages": ["500mg", "three times daily"]
}
```

## Core Files

- `medical_extractor_simple.py` - Main extraction engine
- `batch_process.py` - Process single or multiple files
- `view_database.py` - View and search records
- `database_saver.py` - Database management
- `vibe_watcher.py` - **NEW!** Automatic Vibe integration service
- `vibe_config.json` - Configuration for Vibe integration

## Documentation

- **QUICK_START.md** - Get started guide
- **README_SIMPLE.md** - Detailed documentation
- **SUCCESS.md** - Complete feature overview
- **VIBE_INTEGRATION.md** - **NEW!** Complete Vibe integration guide

## Performance

- **Speed**: 1-2 seconds per transcription
- **CPU**: Any modern processor
- **RAM**: ~500MB
- **Model Size**: 12MB

## Privacy & Compliance

- ✓ Runs entirely on your local machine
- ✓ No data sent to external servers
- ✓ HIPAA-compliant architecture
- ✓ Encrypted storage ready

## Customization

Easily customize for your needs:
- Add custom medical terms
- Adjust extraction patterns
- Integrate with EHR systems
- Export to various formats

## Roadmap

- [x] **Vibe integration** - Automatic background processing
- [ ] Web interface for doctors
- [ ] Real-time transcription integration
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] EHR system integration
- [ ] Mobile app

## License

MIT License - Free for personal and commercial use

## Support

For questions or issues, check the documentation files or customize the code to fit your specific needs.

---

**MediScribe** - Making medical documentation effortless.
