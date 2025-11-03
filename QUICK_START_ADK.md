# Quick Start: MediScribe + Google ADK

## What You're Getting

A complete voice-enabled medical transcription system using:
- **Google ADK Web UI** - Beautiful web interface with voice input
- **Gemini 2.5 Flash** - Fast, accurate text processing
- **MediScribe Tools** - Auto-translation + medical data extraction
- **Your API Key** - Already configured!

## Start in 3 Steps

### 1. Start the API Server
Open a terminal and run:
```bash
start_adk_server.bat
```

Wait until you see: `Application startup complete`

### 2. Start the Web UI
Open ANOTHER terminal and run:
```bash
start_adk_web.bat
```

Wait until you see: `Compiled successfully`

### 3. Open Your Browser
Navigate to: **http://localhost:4200**

## Using Voice Interaction

1. Click the **microphone icon** in the web UI
2. Speak your medical conversation (any supported language)
3. Click stop when done
4. The agent will automatically:
   - Transcribe your speech
   - Detect the language
   - Translate if needed
   - Extract medical data
   - Save to database

## Supported Languages

- English
- Shona (Zimbabwe)
- Ndebele (Zimbabwe/South Africa)
- Zulu (South Africa)
- Xhosa (South Africa)
- Afrikaans (South Africa)

## Example Conversation

Try saying:
> "Patient John Doe, age 45, presents with severe headache for 3 days. Blood pressure 140/90. Diagnosed with migraine. Prescribed ibuprofen 400mg three times daily."

The system will extract:
- Patient: John Doe, 45 years old
- Symptoms: Severe headache (3 days)
- Vital Signs: BP 140/90
- Diagnosis: Migraine
- Medications: Ibuprofen 400mg TID

## Troubleshooting

**Port already in use?**
- Kill any existing processes on ports 4200 or 8000
- Or change ports in the batch files

**Can't connect?**
- Make sure API server started first
- Check both terminals for errors
- Verify your API key is set

**Voice not working?**
- Allow microphone permissions in browser
- Use Chrome or Edge (best support)
- Check browser console for errors

## What's Happening Behind the Scenes

```
Your Voice → Gemini Transcription → ADK Agent → MediScribe Tools → Database
```

1. **Voice Input**: Browser captures audio, sends to Gemini
2. **Transcription**: Gemini converts speech to text
3. **Agent Processing**: ADK agent receives text, calls MediScribe tools
4. **Data Extraction**: Tools detect language, translate, extract medical data
5. **Storage**: Structured data saved to medical_records.json

## Next Steps

- View records: `python view_database.py`
- Search patients: Use the agent chat to search by name
- Customize agent: Edit `adk_agent_config.py`
- Change model: Switch to gemini-1.5-pro or other models

## Files You Can Customize

- `adk_agent_config.py` - Agent behavior and tools
- `start_adk_server.bat` - Server configuration
- `adk-web/` - Web UI customization

---

**Ready?** Run `start_adk_server.bat` and `start_adk_web.bat` in separate terminals!
