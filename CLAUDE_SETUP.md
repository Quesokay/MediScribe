# MediScribe Setup for Claude Desktop

## 🎯 Quick Setup (5 Minutes)

You're using Claude Desktop - perfect! This is the official MCP client and works great with MediScribe.

---

## Step 1: Install Dependencies

```bash
# Run the setup script
setup_chatgpt_mode.bat

# Or manually
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

---

## Step 2: Start MediScribe MCP Server

Open a terminal and run:

```bash
python mcp_server.py
```

You should see:

```
🚀 Initializing MediScribe MCP Server...
✓ Medical extractor ready
✓ Database ready
✓ Multilingual translation ready (NLLB-200)
  Supported: Shona, Ndebele, Zulu, Xhosa, Afrikaans → English

======================================================================
MediScribe MCP Server Ready!
======================================================================
Waiting for ChatGPT/Claude to connect and send conversations...
======================================================================
```

**Keep this terminal window open!** The server must stay running.

---

## Step 3: Configure Claude Desktop

### Windows:

1. Open File Explorer
2. Type in address bar: `%APPDATA%\Claude`
3. Create or edit `claude_desktop_config.json`
4. Add this content:

```json
{
  "mcpServers": {
    "mediscribe": {
      "command": "python",
      "args": ["C:/Clone_wars/MediScribe/mcp_server.py"]
    }
  }
}
```

**Note**: The path `C:/Clone_wars/MediScribe/mcp_server.py` is already set to your project location!

### Mac:

1. Open Terminal
2. Run: `code ~/Library/Application\ Support/Claude/claude_desktop_config.json`
3. Add the same JSON content (update path to your Mac location)

---

## Step 4: Restart Claude Desktop

1. Quit Claude Desktop completely
2. Reopen Claude Desktop
3. Wait a few seconds for it to connect to MediScribe

---

## Step 5: Verify Connection

In Claude Desktop, look for the **🔧 tools icon** (usually in the bottom right or input area).

Click it and you should see **7 MediScribe tools**:

- process_conversation
- extract_medical_data
- translate_and_extract
- search_patient_records
- get_patient_record
- get_all_records
- save_to_database

✅ **If you see these tools, you're connected!**

---

## 🎬 First Test

In Claude, type:

```
I'm going to give you a medical conversation to process.

Doctor: Good morning! What's your name?
Patient: I'm John Doe, 45 years old, male.
Doctor: What brings you in today?
Patient: I have a fever and headache for 3 days.
Doctor: Let me check. Temperature is 101.5F.
Doctor: I'll prescribe Ibuprofen 400mg three times daily.

Please process this conversation using the process_conversation tool.
```

Claude will:

1. Automatically call the `process_conversation` tool
2. Send the conversation to MediScribe
3. MediScribe extracts the medical data
4. Claude shows you the structured results

You should see in your MCP server terminal:

```
======================================================================
📝 Processing conversation from ChatGPT/Claude
   Time: 2025-10-24 10:30:00
   Length: 280 characters
======================================================================
🔍 Detecting language...
   Detected: English
   ✓ Already in English
🔬 Extracting medical data...
   ✓ Extraction complete
💾 Saving to database...
   ✓ Saved as: REC-20251024103000

📊 Summary:
   Patient: John Doe
   Symptoms: 2 found
   Medications: 1 found
======================================================================
```

And Claude will respond with:

```
I've processed the medical conversation. Here's the extracted data:

**Patient Information:**
- Name: John Doe
- Age: 45 years old
- Gender: Male

**Symptoms:**
- Fever (3 days)
- Headache (3 days)

**Vital Signs:**
- Temperature: 101.5°F

**Medications:**
- Ibuprofen 400mg, three times daily

**Record Details:**
- Record ID: REC-20251024103000
- Saved to database: Yes
```

✅ **If this works, you're all set!**

---

## 🌍 Test Multilingual (Shona)

Try this in Claude:

```
Process this Shona medical conversation:

Chiremba: Mangwanani. Zita renyu ndiani?
Murwere: Ndini Tendai Moyo, ndine makore 42.
Chiremba: Muri kunzwa sei?
Murwere: Ndine fivha uye kurwara musoro.
Chiremba: Tembiricha yenyu iri pa 38.5 degrees.
Chiremba: Ndichakupai Paracetamol 500mg.
```

MediScribe will:

- Detect language: Shona
- Translate to English
- Extract medical data
- Save to database

Claude will show you the results in English!

---

## 💬 How to Use Daily

### With Voice Mode:

1. Enable voice in Claude Desktop
2. Have your medical conversation
3. Say: "Process this conversation"
4. Done! Claude automatically calls MediScribe

### With Text:

Just type or paste a conversation and say:

```
"Process this medical conversation"
```

### Search Records:

```
"Search for patient records for John Doe"
"Get all recent medical records"
"Show me the record REC-20251024103000"
```

---

## 🐛 Troubleshooting

### Claude doesn't show the tools icon

**Solutions:**

1. Make sure MCP server is running: `python mcp_server.py`
2. Check `claude_desktop_config.json` path is correct
3. Restart Claude Desktop completely
4. Check Claude Desktop is updated to latest version

### Server won't start

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### Translation not working

```bash
pip install transformers torch
```

First run downloads ~2.5GB NLLB model (one-time, be patient)

### Path issues

Make sure to use **forward slashes** `/` not backslashes `\`:

```json
✅ "C:/Clone_wars/MediScribe/mcp_server.py"
❌ "C:\\Clone_wars\\MediScribe\\mcp_server.py"
```

### Server logs not showing

Check your terminal where you ran `python mcp_server.py` - all logs appear there.

---

## 📊 What Gets Extracted

From any conversation, MediScribe extracts:

- ✅ Patient name, age, gender
- ✅ Symptoms
- ✅ Diagnosis
- ✅ Medications and dosages
- ✅ Vital signs (temperature, BP, heart rate)
- ✅ Allergies
- ✅ Treatment plan
- ✅ Follow-up instructions

All saved to searchable database!

---

## 🎯 Example Prompts for Claude

```
"Process this medical conversation"

"Extract patient data from our discussion"

"Search for all records for Sarah Johnson"

"Get the last 10 patient records"

"Process this Shona conversation: [paste]"

"Translate and extract data from this Ndebele consultation"
```

---

## 📁 View Your Data

### In Terminal:

```bash
# View all records
python show_records.py

# Search for patient
python mediscribe.py --search "John Doe"

# View specific record
python mediscribe.py --view
```

### In Claude:

```
"Show me all patient records"
"Search for John Doe's records"
"Get record REC-20251024103000"
```

---

## 🎉 You're Ready!

Keep the MCP server running, use Claude normally, and ask it to process your medical conversations. Everything else is automatic!

### Quick Reference:

1. **Start server**: `python mcp_server.py` (keep running)
2. **Use Claude**: Just talk and ask to process
3. **View data**: `python show_records.py` or ask Claude

---

## 📚 More Documentation

- **[MCP_COMPLIANCE.md](MCP_COMPLIANCE.md)** - How we follow MCP standards
- **[CHATGPT_MCP_WORKFLOW.md](CHATGPT_MCP_WORKFLOW.md)** - Detailed workflow
- **[USAGE_GUIDE.md](USAGE_GUIDE.md)** - Complete usage guide
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture

---

**Happy processing with Claude!** 🎉
