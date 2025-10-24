# MediScribe Architecture - ChatGPT Voice Mode Integration

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     ChatGPT Voice Mode                          │
│                  (User speaks naturally)                        │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ Voice → Text Transcript
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│                  User Copies Transcript                         │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ Paste into MediScribe
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│              MediScribe Processing Pipeline                     │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  1. Language Detection                                   │  │
│  │     - Auto-detect: English, Shona, Ndebele, etc.       │  │
│  └──────────────────────┬───────────────────────────────────┘  │
│                         │                                       │
│                         ↓                                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  2. Translation (if needed)                             │  │
│  │     - NLLB-200 Model (Meta)                            │  │
│  │     - Offline, no API keys                             │  │
│  │     - African languages → English                      │  │
│  └──────────────────────┬───────────────────────────────────┘  │
│                         │                                       │
│                         ↓                                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  3. Medical Entity Extraction                           │  │
│  │     - spaCy NLP                                         │  │
│  │     - Extract: patient info, symptoms, diagnosis,      │  │
│  │       medications, vital signs, treatment plan         │  │
│  └──────────────────────┬───────────────────────────────────┘  │
│                         │                                       │
│                         ↓                                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  4. Database Storage                                    │  │
│  │     - SQLite database                                   │  │
│  │     - Structured JSON records                           │  │
│  │     - Searchable by patient name                        │  │
│  └──────────────────────┬───────────────────────────────────┘  │
└─────────────────────────┼───────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Structured Output                            │
│  - Patient demographics                                         │
│  - Clinical findings                                            │
│  - Treatment plan                                               │
│  - Record ID for retrieval                                      │
└─────────────────────────────────────────────────────────────────┘
```

## 🔄 Data Flow

### 1. Input Stage
```
ChatGPT Voice → Text Transcript → User Clipboard → MediScribe
```

### 2. Processing Stage
```
Raw Text → Language Detection → Translation → Entity Extraction → Structured Data
```

### 3. Storage Stage
```
Structured Data → Validation → Database → Record ID
```

### 4. Retrieval Stage
```
Query → Database Search → Record Retrieval → JSON Output
```

## 🧩 Component Breakdown

### Core Components

#### 1. **realtime_chatgpt_processor.py**
- Main entry point for ChatGPT voice mode integration
- Handles user interaction
- Orchestrates the processing pipeline
- Provides interactive menu

**Key Classes**:
- `ChatGPTVoiceProcessor`: Main processor class
  - `process_conversation()`: Process a conversation
  - `process_from_input()`: Interactive paste mode
  - `process_from_file()`: File-based processing
  - `view_recent_records()`: Database queries

#### 2. **mcp_server.py**
- Model Context Protocol server
- Exposes tools for AI assistants
- Handles tool calls from ChatGPT

**Available Tools**:
- `extract_medical_data`: Extract from English text
- `translate_and_extract`: Multilingual processing
- `search_patient_records`: Database search
- `get_patient_record`: Retrieve by ID
- `get_all_records`: List all records
- `save_to_database`: Store extracted data

#### 3. **translator.py**
- Multilingual translation engine
- Uses NLLB-200 model

**Key Classes**:
- `MultilingualTranslator`: Translation handler
  - `detect_language()`: Auto-detect language
  - `translate()`: Translate to English
  - `translate_nllb()`: NLLB translation
  - `translate_google()`: Google Translate fallback

**Supported Languages**:
- English (eng_Latn)
- Shona (sna_Latn)
- Ndebele (nde_Latn)
- Zulu (zul_Latn)
- Xhosa (xho_Latn)
- Afrikaans (afr_Latn)

#### 4. **medical_extractor_simple.py**
- Medical entity extraction
- Uses spaCy NLP

**Key Classes**:
- `MedicalExtractor`: Entity extractor
  - `extract_from_text()`: Extract from text
  - `extract_from_file()`: Extract from file

**Extracted Entities**:
- Patient name, age, gender
- Symptoms
- Diagnosis
- Medications & dosages
- Vital signs
- Allergies
- Treatment plan
- Follow-up instructions

#### 5. **database_saver.py**
- SQLite database operations
- Record management

**Key Classes**:
- `MedicalRecordDB`: Database handler
  - `add_record()`: Save new record
  - `get_record()`: Retrieve by ID
  - `search_by_patient()`: Search by name
  - `get_all_records()`: List all records

## 🔌 Integration Points

### ChatGPT Integration

```
┌──────────────┐
│   ChatGPT    │
│  Voice Mode  │
└──────┬───────┘
       │
       │ User copies transcript
       ↓
┌──────────────┐
│  MediScribe  │
│  Processor   │
└──────┬───────┘
       │
       │ Structured data
       ↓
┌──────────────┐
│   Database   │
└──────────────┘
```

### MCP Integration

```
┌──────────────┐
│   ChatGPT    │
│  (MCP Client)│
└──────┬───────┘
       │
       │ MCP Protocol
       ↓
┌──────────────┐
│ MCP Server   │
│ (MediScribe) │
└──────┬───────┘
       │
       │ Tool calls
       ↓
┌──────────────┐
│  Processing  │
│   Pipeline   │
└──────────────┘
```

## 📊 Data Models

### Conversation Record

```json
{
  "record_id": "REC-20251024103000",
  "timestamp": "2025-10-24T10:30:00",
  "source": "chatgpt_voice_mode",
  "original_language": "english",
  "patient_name": "John Doe",
  "age": "45",
  "gender": "male",
  "symptoms": [
    {
      "text": "headache",
      "start": 120,
      "end": 128
    }
  ],
  "diagnosis": [
    {
      "text": "viral infection",
      "start": 300,
      "end": 315
    }
  ],
  "medications": [
    {
      "text": "Ibuprofen 400mg three times daily",
      "start": 400,
      "end": 433
    }
  ],
  "vital_signs": [
    {
      "text": "temperature 101.5F",
      "start": 200,
      "end": 218
    }
  ],
  "treatment_plan": [
    {
      "text": "rest and increase fluid intake",
      "start": 500,
      "end": 530
    }
  ],
  "follow_up": [
    {
      "text": "follow up in one week",
      "start": 600,
      "end": 621
    }
  ]
}
```

### Database Schema

```sql
CREATE TABLE medical_records (
    record_id TEXT PRIMARY KEY,
    timestamp TEXT NOT NULL,
    patient_name TEXT,
    age TEXT,
    gender TEXT,
    symptoms TEXT,  -- JSON array
    diagnosis TEXT,  -- JSON array
    medications TEXT,  -- JSON array
    vital_signs TEXT,  -- JSON array
    allergies TEXT,  -- JSON array
    treatment_plan TEXT,  -- JSON array
    follow_up TEXT,  -- JSON array
    raw_transcription TEXT,
    original_language TEXT,
    translated_text TEXT,
    source TEXT
);
```

## 🔐 Security & Privacy

### Data Handling
- All processing happens locally (except ChatGPT conversation)
- Translation uses offline NLLB model
- No external API calls for extraction
- Database stored locally

### Privacy Considerations
- Patient data never leaves local system (after ChatGPT)
- No cloud storage
- No external API calls (except optional Google Translate)
- User controls all data

### Compliance Notes
- Not HIPAA compliant out-of-the-box
- Requires additional security measures for production
- Intended for research/demonstration only

## 🚀 Performance

### Processing Speed
- Language detection: < 1 second
- Translation (NLLB): 2-5 seconds
- Entity extraction: 1-2 seconds
- Database save: < 1 second
- **Total**: 4-9 seconds per conversation

### Resource Usage
- **Memory**: 2-4 GB (NLLB model loaded)
- **Disk**: ~3 GB (models + database)
- **CPU**: Moderate (can run on CPU, no GPU required)

### Scalability
- Single conversation: 4-9 seconds
- Batch processing: Parallel processing possible
- Database: SQLite handles thousands of records efficiently

## 🔧 Configuration

### Environment Variables
```bash
# Optional: Google Translate API key
GOOGLE_TRANSLATE_API_KEY=your_key_here

# Optional: Custom database path
DB_PATH=path/to/database.db
```

### Model Configuration
```python
# Translation model
MODEL_NAME = "facebook/nllb-200-distilled-600M"

# spaCy model
SPACY_MODEL = "en_core_web_sm"
```

## 🧪 Testing Strategy

### Unit Tests
- Language detection accuracy
- Translation quality
- Entity extraction precision
- Database operations

### Integration Tests
- End-to-end conversation processing
- MCP tool calls
- Multilingual workflows

### Test Files
- `test_chatgpt_processor.py`: Main test suite
- Sample conversations in multiple languages
- Edge cases and error handling

## 📈 Future Enhancements

### Planned Features
1. **Real-time streaming**: Process as conversation happens
2. **Voice input**: Direct audio processing
3. **Advanced NER**: Custom medical entity models
4. **Multi-modal**: Support images (X-rays, charts)
5. **Export formats**: PDF, HL7 FHIR, CSV
6. **Analytics**: Conversation insights and trends

### Potential Integrations
- EHR systems (Epic, Cerner)
- Telemedicine platforms
- Medical training systems
- Research databases

## 🎯 Design Principles

1. **Modularity**: Each component is independent
2. **Extensibility**: Easy to add new languages/entities
3. **Privacy-first**: Local processing by default
4. **User-friendly**: Simple CLI and MCP interfaces
5. **Robust**: Error handling and validation
6. **Documented**: Comprehensive guides and examples

## 📚 Technology Stack

- **Python 3.8+**: Core language
- **spaCy**: NLP and entity extraction
- **Transformers**: NLLB translation model
- **PyTorch**: Deep learning backend
- **SQLite**: Database
- **MCP**: Model Context Protocol
- **asyncio**: Async operations for MCP server
