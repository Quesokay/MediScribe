# Start Using MediScribe with Claude Desktop

## ✅ Configuration Complete!

Your Claude Desktop is already configured! The config file is at:
`C:\Users\moyov\AppData\Roaming\Claude\claude_desktop_config.json`

---

## 🚀 How to Use (3 Steps)

### Step 1: Start the MCP Server

Open a **new terminal** (not the one that had the error) and run:

```powershell
python mcp_server.py
```

You should see:

```
🚀 Initializing MediScribe MCP Server...
✓ Medical extractor ready
✓ Database ready
✓ Multilingual translation ready (NLLB-200)

======================================================================
MediScribe MCP Server Ready!
======================================================================
Waiting for ChatGPT/Claude to connect and send conversations...
======================================================================
```

**Keep this terminal open!** Don't type anything in it - just let it run.

---

### Step 2: Restart Claude Desktop

1. **Quit Claude Desktop completely** (right-click taskbar icon → Quit)
2. **Wait 5 seconds**
3. **Open Claude Desktop again**

---

### Step 3: Verify Connection

In Claude Desktop, look for the **🔧 tools icon** (usually near the input box).

Click it and you should see **7 MediScribe tools**:

- process_conversation
- extract_medical_data
- translate_and_extract
- search_patient_records
- get_patient_record
- get_all_records
- save_to_database

✅ **If you see these, you're connected!**

---

## 🎬 First Test

In Claude, type:

```
Process this medical conversation:

Doctor: Good morning! What's your name?
Patient: I'm John Doe, 45 years old, male.
Doctor: What brings you in today?
Patient: I have a fever and headache for 3 days.
Doctor: Let me check. Temperature is 101.5F.
Doctor: I'll prescribe Ibuprofen 400mg three times daily.
```

Claude will automatically:

1. Call the `process_conversation` tool
2. Send it to MediScribe
3. Show you the extracted data

In your MCP server terminal, you'll see:

```
======================================================================
📝 Processing conversation from ChatGPT/Claude
   Time: 2025-10-24 10:30:00
   Length: 280 characters
======================================================================
🔍 Detecting language...
   Detected: English
🔬 Extracting medical data...
   ✓ Extraction complete
💾 Saving to database...
   ✓ Saved as: REC-20251024103000
======================================================================
```

---

## 🌍 Test Multilingual (Shona)

Try this:

```
Process this Shona medical conversation:

Chiremba: Mangwanani. Zita renyu ndiani?
Murwere: Ndini Tendai Moyo, ndine makore 42.
Chiremba: Muri kunzwa sei?
Murwere: Ndine fivha uye kurwara musoro.
Chiremba: Tembiricha yenyu iri pa 38.5 degrees.
```

MediScribe will:

- Detect: Shona
- Translate to English
- Extract medical data
- Save to database

---

## 💬 Daily Usage

Just talk to Claude naturally:

```
"Process this medical conversation"
"Search for patient John Doe"
"Show me all recent records"
"Process this Ndebele conversation: [paste]"
```

Claude handles everything automatically!

---

## 🐛 Troubleshooting

### No tools icon in Claude?

1. Make sure MCP server is running: `python mcp_server.py`
2. Restart Claude Desktop completely
3. Wait 10 seconds after restart
4. Check Claude Desktop is latest version

### Server shows error?

- **Don't type anything in the server terminal!** Just let it run
- If you see "Invalid JSON" error, restart the server
- The server only accepts JSON-RPC from Claude, not keyboard input

### Translation not working?

First run downloads ~2.5GB model. Be patient!

---

## 📊 View Your Data

### In Terminal:

```powershell
python show_records.py
```

### In Claude:

```
"Show me all patient records"
"Search for John Doe"
```

---

## 🎉 That's It!

1. Keep `python mcp_server.py` running
2. Use Claude normally
3. Ask it to process conversations
4. Everything else is automatic!

---

## ⚠️ Important Notes

- **Don't type in the MCP server terminal** - it only accepts JSON-RPC from Claude
- **Keep the server running** - Claude needs it to process conversations
- **Restart Claude after config changes** - Required for MCP to reconnect

---

**You're all set! Start processing medical conversations with Claude!** 🎉
