# MediScribe - ChatGPT Voice Mode Integration

Real-time medical conversation processing using ChatGPT voice mode with multilingual support.

## 🎯 Overview

This system allows you to:
1. Have medical conversations using ChatGPT voice mode
2. Copy the conversation transcript
3. Process it through MediScribe to extract structured medical data
4. Automatically translate from Shona, Ndebele, Zulu, Xhosa, or Afrikaans
5. Save to database via MCP (Model Context Protocol)

## 🚀 Quick Start

### Option 1: Interactive Mode (Recommended)

```bash
python realtime_chatgpt_processor.py
```

Then select from the menu:
- **Option 1**: Paste conversation directly
- **Option 2**: Process from file
- **Option 3**: View recent records
- **Option 4**: Test with sample conversation

### Option 2: MCP Server (For AI Integration)

Start the MCP server:
```bash
python mcp_server.py
```

Or use the batch file:
```bash
start_mcp_server.bat
```

## 📋 Workflow with ChatGPT Voice Mode

### Step 1: Have Your Conversation
1. Open ChatGPT and enable voice mode
2. Have a medical conversation (doctor-patient, consultation, etc.)
3. The conversation can be in English or any supported language

### Step 2: Copy the Transcript
1. After the conversation, copy the text from ChatGPT
2. ChatGPT voice mode provides a text transcript of the conversation

### Step 3: Process with MediScribe
1. Run the processor: `python realtime_chatgpt_processor.py`
2. Select option 1 (paste mode)
3. Paste your conversation
4. Press Enter, then Ctrl+Z and Enter (Windows) to finish

### Step 4: Review Extracted Data
The system will:
- Detect the language automatically
- Translate to English if needed (using NLLB model)
- Extract medical entities using spaCy
- Save to database
- Display a summary

## 🌍 Multilingual Support

### Supported Languages
- **English** (default)
- **Shona** (Zimbabwe)
- **Ndebele** (Zimbabwe/South Africa)
- **Zulu** (South Africa)
- **Xhosa** (South Africa)
- **Afrikaans** (South Africa)

### Translation Engine
Uses **NLLB-200** (No Language Left Behind) by Meta:
- Offline translation (no API keys needed)
- High quality for African languages
- First run downloads ~2.5GB model

### Enable Translation
```python
processor = ChatGPTVoiceProcessor(use_translation=True)
```

## 🔧 MCP Integration

### What is MCP?
Model Context Protocol allows AI assistants like ChatGPT to call your tools directly.

### Available MCP Tools

1. **extract_medical_data**
   - Extract structured data from transcription
   - Input: conversation text
   - Output: patient info, symptoms, diagnosis, medications, etc.

2. **translate_and_extract**
   - Translate non-English text and extract data
   - Auto-detects language
   - Supports all African languages listed above

3. **search_patient_records**
   - Search database by patient name
   - Returns all matching records

4. **get_patient_record**
   - Get specific record by ID
   - Format: REC-YYYYMMDDHHMMSS

5. **get_all_records**
   - List all records in database
   - Optional limit parameter

6. **save_to_database**
   - Save extracted data to database
   - Returns record ID

### Configure MCP in ChatGPT

Copy `mcp_config.json` to your ChatGPT MCP configuration:

```json
{
  "mcpServers": {
    "mediscribe": {
      "command": "python",
      "args": ["C:/path/to/your/mcp_server.py"],
      "env": {},
      "disabled": false
    }
  }
}
```

### Using MCP Tools in ChatGPT

Once configured, you can ask ChatGPT:

```
"Extract medical data from this conversation: [paste conversation]"

"Search for patient records for John Doe"

"Get all recent medical records"

"Translate this Shona conversation and extract medical data: [paste]"
```

## 📊 Extracted Data Structure

```json
{
  "patient_name": "John Doe",
  "age": "45",
  "gender": "male",
  "symptoms": [
    {"text": "headache", "start": 120, "end": 128},
    {"text": "fever", "start": 145, "end": 150}
  ],
  "diagnosis": [
    {"text": "viral infection", "start": 300, "end": 315}
  ],
  "medications": [
    {"text": "Ibuprofen 400mg", "start": 400, "end": 415}
  ],
  "vital_signs": [
    {"text": "temperature 101.5F", "start": 200, "end": 218},
    {"text": "BP 130/85", "start": 220, "end": 229}
  ],
  "original_language": "english",
  "processed_at": "2025-10-24T10:30:00",
  "record_id": "REC-20251024103000"
}
```

## 🧪 Testing

### Test the Processor
```bash
python test_chatgpt_processor.py
```

This runs three test scenarios:
1. English medical conversation
2. Shona conversation with translation
3. Multi-person group consultation

### Test MCP Tools
```bash
# Start the server
python mcp_server.py

# In another terminal, test with MCP client
# Or use ChatGPT with MCP configured
```

## 💾 Database

All processed conversations are saved to SQLite database:
- **Location**: `medical_records.db`
- **View records**: `python show_records.py`
- **Search**: `python mediscribe.py --search "Patient Name"`

## 🔍 Example Conversations

### English Example
```
Doctor: Good morning! What brings you in today?
Patient: Hi doctor. I'm Sarah Johnson, 28 years old. I have a terrible headache.
Doctor: Let me check your vitals. Temperature is 101.5F, BP is 125/80.
Patient: I also have a dry cough and body aches.
Doctor: I believe you have the flu. I'll prescribe Ibuprofen 400mg three times daily.
```

### Shona Example
```
Chiremba: Mangwanani. Zita renyu ndiani?
Murwere: Ndini Tendai Moyo, ndine makore 42. Ndiri kunzwa kurwara musoro.
Chiremba: Tembiricha yenyu iri pa 39.2 degrees.
Murwere: Ndine chikosoro uye kurema mumuviri.
Chiremba: Ndichakupai Paracetamol 500mg katatu pazuva.
```

## 📁 Project Structure

```
mediscribe/
├── realtime_chatgpt_processor.py  # Main processor for ChatGPT voice mode
├── mcp_server.py                  # MCP server for AI integration
├── medical_extractor_simple.py    # spaCy-based data extraction
├── translator.py                  # NLLB multilingual translation
├── database_saver.py              # SQLite database operations
├── test_chatgpt_processor.py      # Test suite
├── mcp_config.json                # MCP configuration
└── start_mcp_server.bat           # Windows startup script
```

## 🛠️ Requirements

```bash
pip install spacy
pip install transformers torch  # For translation
pip install mcp  # For MCP server
python -m spacy download en_core_web_sm
```

## 🎯 Use Cases

1. **Real-time Clinical Documentation**
   - Doctor speaks with patient
   - Conversation captured via ChatGPT voice mode
   - Automatically extracted and saved

2. **Multilingual Clinics**
   - Patients speak in native language
   - Automatic translation to English
   - Standardized medical records

3. **Telemedicine**
   - Remote consultations via ChatGPT voice
   - Structured data extraction
   - Database integration

4. **Medical Training**
   - Record practice consultations
   - Extract key medical information
   - Review and analyze

## 🔐 Privacy & Security

- All processing happens locally (except ChatGPT conversation)
- Translation uses offline NLLB model (no external API)
- Database stored locally
- No data sent to external services (except initial ChatGPT conversation)

## 🚨 Important Notes

1. **Not for Production Medical Use**: This is a demonstration/research tool
2. **Verify Extracted Data**: Always review extracted information
3. **HIPAA Compliance**: Ensure compliance if using with real patient data
4. **ChatGPT Terms**: Review OpenAI's terms for medical use cases

## 📞 Support

For issues or questions:
1. Check the test suite: `python test_chatgpt_processor.py`
2. View logs in `conversation_logs/` directory
3. Check database: `python show_records.py`

## 🎉 Next Steps

1. Test with sample conversations
2. Configure MCP in ChatGPT
3. Try with real conversations (test data only)
4. Customize extraction rules in `medical_extractor_simple.py`
5. Add custom medical entities as needed
