# Corrected Architecture: ADK Web UI → MCP Server

## The Right Way

You're correct - the ADK Web UI should connect to your MCP server. Here's the proper architecture:

```
┌─────────────────────────────────────────────────────────────┐
│              ADK Web UI (Port 4200)                         │
│         Browser-based Voice Interface                       │
│                                                             │
│  • Voice Input (Gemini Speech-to-Text)                     │
│  • Chat Interface                                           │
│  • Visual Feedback                                          │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/WebSocket
                         ↓
┌─────────────────────────────────────────────────────────────┐
│         ADK API Server (Port 8000)                          │
│         Acts as MCP Client                                  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  MediScribe Agent (Gemini 2.5 Flash)                │  │
│  │                                                      │  │
│  │  Wraps MCP tools as ADK tools:                      │  │
│  │  • process_conversation → MCP call                  │  │
│  │  • extract_medical_data → MCP call                  │  │
│  │  • search_patient_records → MCP call                │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │ JSON-RPC over stdio
                         ↓
┌─────────────────────────────────────────────────────────────┐
│         Your MediScribe MCP Server                          │
│         (mcp_server.py)                                     │
│                                                             │
│  • process_conversation (auto-translate)                   │
│  • extract_medical_data                                    │
│  • translate_and_extract                                   │
│  • search_patient_records                                  │
│  • get_all_records                                         │
│  • get_patient_record                                      │
│  • save_to_database                                        │
│  • process_file                                            │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────┐
│              MediScribe Components                          │
│                                                             │
│  • Medical Extractor (spaCy + LLM)                         │
│  • Multilingual Translator (NLLB-200)                      │
│  • Database Saver (medical_records.json)                   │
│  • Language Detector                                        │
└─────────────────────────────────────────────────────────────┘
```

## Key Points

1. **ADK Web UI** - Provides the browser interface with voice input
2. **ADK API Server** - Acts as an MCP client, wrapping your MCP tools
3. **Your MCP Server** - Unchanged! Still does all the medical processing
4. **Communication** - ADK server talks to MCP server via JSON-RPC stdio

## What Changed

I created `adk_mcp_server.py` which:
- Starts your existing `mcp_server.py` as a subprocess
- Wraps each MCP tool as an ADK tool
- Handles JSON-RPC communication
- Provides the agent interface for ADK Web UI

## How It Works

1. **User speaks** in ADK Web UI
2. **Gemini transcribes** the speech to text
3. **ADK agent** receives the text
4. **Agent calls tool** (e.g., `process_conversation`)
5. **ADK tool wrapper** sends JSON-RPC request to MCP server
6. **MCP server** processes (detects language, translates, extracts)
7. **MCP server** returns JSON response
8. **ADK tool wrapper** formats response
9. **Agent** presents results in Web UI
10. **User** sees structured medical data

## Benefits

✅ **Reuses your MCP server** - No duplication of logic
✅ **ADK Web UI** - Professional interface with voice
✅ **MCP stays intact** - Your server works as-is
✅ **Clean separation** - UI layer, agent layer, processing layer
✅ **Easy to maintain** - Changes to MCP server automatically available

## Files

- `adk_mcp_server.py` - ADK server that connects to your MCP server
- `mcp_server.py` - Your existing MCP server (unchanged)
- `start_adk_server.bat` - Updated to use `adk_mcp_server.py`
- `start_adk_web.bat` - Starts the web UI (unchanged)

## Usage

Same as before:
```bash
# Terminal 1
start_adk_server.bat

# Terminal 2
start_adk_web.bat
```

Then open: http://localhost:4200

The difference is now the ADK server properly acts as an MCP client to your existing MCP server!
