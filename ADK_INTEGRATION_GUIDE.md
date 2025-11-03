# MediScribe + Google ADK Integration Guide

## Overview

This integration connects your MediScribe MCP server with Google's Agent Development Kit (ADK), enabling you to use the ADK web UI for live voice interaction with Gemini 2.5 Flash for medical transcription, translation, and data extraction.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    ADK Web UI (Port 4200)                   │
│              Voice Input → Gemini 2.5 Flash                 │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/WebSocket
                         ↓
┌─────────────────────────────────────────────────────────────┐
│              ADK API Server (Port 8000)                     │
│                  MediScribe Agent                           │
└────────────────────────┬────────────────────────────────────┘
                         │ Function Calls
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                  MediScribe Tools                           │
│  • process_conversation (auto-translate + extract)          │
│  • extract_medical_data                                     │
│  • search_patient_records                                   │
│  • get_all_records                                          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────┐
│              Medical Records Database                       │
│                medical_records.json                         │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start

### Option 1: One-Click Startup (Recommended)

Simply run:
```bash
START_ADK_MEDISCRIBE.bat
```

This will:
1. Start the ADK API server on http://localhost:8000
2. Start the ADK Web UI on http://localhost:4200
3. Open two terminal windows (keep both running)

Then open your browser to: **http://localhost:4200**

### Option 2: Manual Startup

**Terminal 1 - Start API Server:**
```bash
start_adk_server.bat
```

**Terminal 2 - Start Web UI:**
```bash
start_adk_web.bat
```

## Using the Voice Interface

1. **Open the Web UI**: Navigate to http://localhost:4200

2. **Start Voice Conversation**: 
   - Click the microphone icon
   - Speak your medical conversation
   - Supports: English, Shona, Ndebele, Zulu, Xhosa, Afrikaans

3. **Process the Conversation**:
   - The agent will automatically:
     - Detect the language
     - Translate to English (if needed)
     - Extract structured medical data
     - Save to database (optional)

4. **View Results**:
   - Patient information
   - Symptoms
   - Diagnosis
   - Medications
   - Vital signs
   - Treatment plans

## Available Tools

The MediScribe agent has these tools available:

### 1. process_conversation
Main tool for voice conversations. Auto-detects language and translates.
```python
process_conversation(
    conversation="Patient says: I have a headache...",
    save_to_db=True
)
```

### 2. extract_medical_data
Extract data from English text only.
```python
extract_medical_data(
    transcription="Patient presents with...",
    save_to_db=False
)
```

### 3. search_patient_records
Search database by patient name.
```python
search_patient_records(patient_name="John Doe")
```

### 4. get_all_records
Retrieve all records.
```python
get_all_records(limit=50)
```

### 5. get_patient_record
Get specific record by ID.
```python
get_patient_record(record_id="REC-20241030120000")
```

## Configuration

### Google API Key
Your API key is configured in `start_adk_server.bat`:
```
GOOGLE_API_KEY=AIzaSyCZXSOHSVMKt92YQxLvSZl0z8Esk1jypjI
```

To change it, edit `start_adk_server.bat` or set environment variable:
```bash
set GOOGLE_API_KEY=your_new_key
```

### Agent Configuration
Edit `adk_agent_config.py` to customize:
- Model selection (default: gemini-2.0-flash-exp)
- System instructions
- Available tools
- Database path

### Web UI Configuration
Edit `adk-web/set-backend.js` to change backend URL if needed.

## Supported Languages

- **English** (default)
- **Shona** (Zimbabwe)
- **Ndebele** (Zimbabwe/South Africa)
- **Zulu** (South Africa)
- **Xhosa** (South Africa)
- **Afrikaans** (South Africa)

Translation is automatic using NLLB-200 model.

## Example Workflows

### Workflow 1: Voice Consultation
1. Start voice recording in ADK Web UI
2. Conduct medical consultation in any supported language
3. Stop recording
4. Agent automatically processes and extracts data
5. Review structured output
6. Data saved to database

### Workflow 2: Search Patient History
1. In chat, ask: "Search for patient John Doe"
2. Agent uses search_patient_records tool
3. View all records for that patient
4. Ask for specific record details

### Workflow 3: Multilingual Consultation
1. Patient speaks in Shona
2. Voice transcribed by Gemini
3. Agent detects Shona language
4. Translates to English
5. Extracts medical data
6. Saves with both original and translated text

## Troubleshooting

### API Server Won't Start
- Check if port 8000 is already in use
- Verify Google API key is set correctly
- Ensure virtual environment is activated
- Check: `adk --version`

### Web UI Won't Connect
- Ensure API server is running first
- Check CORS settings in API server
- Verify backend URL in web UI config
- Clear browser cache

### Translation Not Working
- Check if NLLB model is downloaded
- Run: `python download_nllb_model.py`
- Verify translator.py is working
- Check console output for errors

### Voice Input Not Working
- Check browser microphone permissions
- Use Chrome or Edge (best support)
- Ensure HTTPS or localhost
- Check browser console for errors

## Files Created

- `adk_agent_config.py` - Agent configuration with tools
- `start_adk_server.bat` - Start API server
- `start_adk_web.bat` - Start web UI
- `START_ADK_MEDISCRIBE.bat` - One-click startup
- `ADK_INTEGRATION_GUIDE.md` - This guide

## Advanced Usage

### Custom Agent Behavior
Edit the system instruction in `adk_agent_config.py`:
```python
system_instruction="""Your custom instructions here..."""
```

### Add More Tools
Define new tools in `adk_agent_config.py`:
```python
@tool
def my_custom_tool(param: str) -> dict:
    """Tool description"""
    # Your logic here
    return {"result": "data"}
```

### Change Model
Edit `adk_agent_config.py`:
```python
model="gemini-2.0-flash-exp"  # or gemini-1.5-pro, etc.
```

## API Endpoints

When running, the API server exposes:
- `http://localhost:8000/agents` - List agents
- `http://localhost:8000/chat` - Chat endpoint
- `http://localhost:8000/tools` - List tools
- `http://localhost:8000/health` - Health check

## Database

Records are saved to: `medical_records.json`

View records:
```bash
python view_database.py
```

Search records:
```bash
python show_records.py
```

## Next Steps

1. ✅ Start the services with `START_ADK_MEDISCRIBE.bat`
2. ✅ Open http://localhost:4200
3. ✅ Test voice input with a sample conversation
4. ✅ Try different languages
5. ✅ Search and retrieve records

## Support

For issues:
1. Check console output in both terminal windows
2. Review this guide's troubleshooting section
3. Check ADK documentation: https://google.github.io/adk-docs/
4. Verify all dependencies are installed

## Benefits of ADK Integration

- **Live Voice Input**: Real-time transcription with Gemini
- **Web Interface**: Easy-to-use UI for medical professionals
- **Multi-Model Support**: Can switch between Gemini models
- **Debugging Tools**: Built-in debugging and monitoring
- **Extensible**: Easy to add new tools and capabilities
- **Production Ready**: Can deploy to cloud with minimal changes

---

**Ready to use!** Run `START_ADK_MEDISCRIBE.bat` and start processing medical conversations with voice!
