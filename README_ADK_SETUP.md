# MediScribe + ADK Web UI Setup

## Overview

Your MediScribe MCP server is now integrated with Google's ADK Web UI, providing a professional browser-based interface with live voice interaction powered by Gemini 2.5 Flash.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│         Browser (http://localhost:4200)                 │
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐  │
│  │ Voice Input  │  │ Chat Window  │  │  Database   │  │
│  │  (Gemini)    │  │   (Agent)    │  │   Viewer    │  │
│  └──────────────┘  └──────────────┘  └─────────────┘  │
│                                                         │
│              ADK Web UI (Angular)                       │
└────────────────────────┬────────────────────────────────┘
                         │ HTTP/WebSocket
                         ↓
┌─────────────────────────────────────────────────────────┐
│      ADK API Server (http://localhost:8000)             │
│                                                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │  MediScribe Agent (Gemini 2.0 Flash)             │ │
│  │                                                   │ │
│  │  Tools (wrapped from MCP):                       │ │
│  │  • process_conversation                          │ │
│  │  • extract_medical_data                          │ │
│  │  • search_patient_records                        │ │
│  │  • get_all_records                               │ │
│  │  • get_patient_record                            │ │
│  └───────────────────────────────────────────────────┘ │
│                                                         │
│         adk_mcp_server.py (MCP Client)                  │
└────────────────────────┬────────────────────────────────┘
                         │ JSON-RPC stdio
                         ↓
┌─────────────────────────────────────────────────────────┐
│         MediScribe MCP Server (subprocess)              │
│                                                         │
│  mcp_server.py - Your existing MCP server               │
│                                                         │
│  • Medical data extraction                              │
│  • Language detection & translation                     │
│  • Database operations                                  │
│  • All your existing MCP tools                          │
└────────────────────────┬────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────┐
│              medical_records.json                       │
└─────────────────────────────────────────────────────────┘
```

## Quick Start

### 1. Test MCP Connection (Optional)
```bash
python test_mcp_connection.py
```

### 2. Start Everything
```bash
START_ADK_MEDISCRIBE.bat
```

This opens two terminals:
- **Terminal 1**: ADK API Server (backend)
- **Terminal 2**: ADK Web UI (frontend)

### 3. Open Browser
Navigate to: **http://localhost:4200**

## Using Voice Input

1. **Click the microphone icon** in the web UI
2. **Speak your medical conversation** (any supported language)
3. **Click stop** when done
4. **Watch the magic happen**:
   - Gemini transcribes your speech
   - Agent processes the text
   - MCP server detects language
   - Translates if needed
   - Extracts medical data
   - Saves to database
   - Displays results

## Supported Languages

- 🇬🇧 English
- 🇿🇼 Shona (Zimbabwe)
- 🇿🇦 Ndebele (Zimbabwe/South Africa)
- 🇿🇦 Zulu (South Africa)
- 🇿🇦 Xhosa (South Africa)
- 🇿🇦 Afrikaans (South Africa)

## Example Conversations

### English
> "Patient Sarah Johnson, age 32, complains of persistent cough for 2 weeks. Temperature 38.5°C. Diagnosed with bronchitis. Prescribed amoxicillin 500mg twice daily for 7 days."

### Shona
> "Murwere anonzi Tendai Moyo, ane makore 28, anorwadziwa nemusoro kwevhiki. BP 130/85. Takamupa paracetamol."

### Zulu
> "Isiguli uThabo Dlamini, uneminyaka engu-40, unesifo senhliziyo. Umfutho wegazi 150/95. Siphakamise i-enalapril."

## Features

### 🎤 Voice Interaction
- Real-time speech-to-text
- Natural conversation flow
- Hands-free operation

### 🌍 Multilingual
- Auto language detection
- Seamless translation
- Preserves original text

### 🏥 Medical Extraction
- Patient demographics
- Symptoms & complaints
- Vital signs
- Diagnosis
- Medications & dosages
- Treatment plans
- Follow-up instructions

### 💾 Database
- Automatic saving
- Search by patient name
- Retrieve specific records
- View all records
- Export capabilities

### 🤖 AI Agent
- Conversational interface
- Context awareness
- Professional medical persona
- Helpful suggestions

## Files

### Core Files
- `adk_mcp_server.py` - ADK server with MCP client
- `mcp_server.py` - Your MCP server (unchanged)
- `medical_records.json` - Database

### Startup Scripts
- `START_ADK_MEDISCRIBE.bat` - One-click start
- `start_adk_server.bat` - Start API server
- `start_adk_web.bat` - Start web UI

### Testing
- `test_mcp_connection.py` - Test MCP integration
- `test_adk_setup.py` - Test ADK setup

### Documentation
- `README_ADK_SETUP.md` - This file
- `FINAL_SETUP.md` - Complete setup guide
- `CORRECTED_ARCHITECTURE.md` - Architecture details
- `ADK_INTEGRATION_GUIDE.md` - Full integration guide
- `QUICK_START_ADK.md` - Quick start guide

## Configuration

### Google API Key
Set in `start_adk_server.bat`:
```batch
set GOOGLE_API_KEY=AIzaSyCZXSOHSVMKt92YQxLvSZl0z8Esk1jypjI
```

### Model Selection
Edit `adk_mcp_server.py`:
```python
model="gemini-2.0-flash-exp"  # Fast and efficient
# or
model="gemini-1.5-pro"  # More capable
```

### Ports
- API Server: 8000 (change in `start_adk_server.bat`)
- Web UI: 4200 (change in `start_adk_web.bat`)

## Troubleshooting

### MCP Server Not Starting
Check Terminal 1 for MCP logs:
```
[MCP] Initializing MediScribe MCP Server...
[MCP] Medical extractor ready
[MCP] Database ready
[MCP] MediScribe MCP Server Ready!
```

If missing, check:
- Virtual environment activated
- All dependencies installed
- `mcp_server.py` exists

### Web UI Can't Connect
- Ensure API server started first
- Check CORS settings
- Verify backend URL: http://localhost:8000
- Clear browser cache

### Voice Not Working
- Allow microphone permissions
- Use Chrome or Edge (best support)
- Check Gemini API access
- Verify API key is valid

### Tools Not Responding
- Check JSON-RPC communication in logs
- Verify MCP server is running
- Test with `test_mcp_connection.py`

## Advanced Usage

### Custom Agent Behavior
Edit system instruction in `adk_mcp_server.py`:
```python
system_instruction="""Your custom instructions..."""
```

### Add New MCP Tools
1. Add tool to `mcp_server.py`
2. Wrap it in `adk_mcp_server.py`:
```python
@tool
async def my_new_tool(param: str) -> str:
    client = await get_mcp_client()
    result = await client.call_tool("my_new_tool", {"param": param})
    return json.dumps(result, indent=2)
```

### Multiple MCP Servers
Modify `adk_mcp_server.py` to connect to multiple MCP servers:
```python
mcp_client_1 = MCPClient(python_path, "server1.py")
mcp_client_2 = MCPClient(python_path, "server2.py")
```

## API Endpoints

When running, these endpoints are available:

- `GET http://localhost:8000/` - API info
- `GET http://localhost:8000/agents` - List agents
- `POST http://localhost:8000/chat` - Chat with agent
- `GET http://localhost:8000/tools` - List tools
- `GET http://localhost:8000/health` - Health check
- `GET http://localhost:8000/docs` - API docs (Swagger)

## Database Operations

### View Records
```bash
python view_database.py
```

### Search Records
```bash
python show_records.py
```

### Check Database
```bash
python check_db.py
```

## Next Steps

1. ✅ Test MCP connection: `python test_mcp_connection.py`
2. ✅ Start services: `START_ADK_MEDISCRIBE.bat`
3. ✅ Open browser: http://localhost:4200
4. ✅ Test voice input with sample conversation
5. ✅ Try different languages
6. ✅ Search patient records
7. ✅ Customize agent behavior
8. ✅ Add custom tools

## Resources

- **ADK Docs**: https://google.github.io/adk-docs/
- **ADK Web**: https://github.com/google/adk-web
- **ADK Samples**: https://github.com/google/adk-samples
- **Gemini API**: https://ai.google.dev/
- **MCP Protocol**: https://modelcontextprotocol.io/

## Support

For issues:
1. Check terminal output for errors
2. Review troubleshooting section
3. Test MCP connection
4. Verify all dependencies
5. Check ADK documentation

---

**Ready to use!** 🎉

Run `START_ADK_MEDISCRIBE.bat` and open http://localhost:4200 to start using your voice-enabled medical transcription system!
