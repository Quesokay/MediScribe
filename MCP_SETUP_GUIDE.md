# MediScribe MCP Setup - Complete Guide

## 🎯 What You're Setting Up

A system where ChatGPT automatically processes medical conversations:
1. You talk in ChatGPT voice mode
2. ChatGPT sends the transcript to MediScribe
3. MediScribe translates (if needed) and extracts medical data
4. Results appear in ChatGPT
5. Data saved to database

**No copy/paste required!**

---

## 📋 Prerequisites

### 1. Python 3.8 or higher
```bash
python --version
```

### 2. Install Dependencies
```bash
# Run the setup script
setup_chatgpt_mode.bat

# Or manually
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 3. ChatGPT Plus Account
- Required for MCP support
- Voice mode available

---

## 🚀 Setup Steps

### Step 1: Find Your Project Path

1. Open your project folder in File Explorer
2. Click the address bar and copy the full path
3. Example: `C:\Users\YourName\Documents\mediscribe`

**Important**: You'll need this path for configuration!

---

### Step 2: Update MCP Configuration

1. Open `mcp_config.json` in your project folder
2. Find this line:
   ```json
   "args": ["C:/full/path/to/your/mcp_server.py"],
   ```
3. Replace with your actual path:
   ```json
   "args": ["C:/Users/YourName/Documents/mediscribe/mcp_server.py"],
   ```
4. Save the file

**Note**: Use forward slashes `/` not backslashes `\`

---

### Step 3: Start MediScribe MCP Server

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
Waiting for ChatGPT to connect and send conversations...
======================================================================
```

**Keep this window open!** The server must stay running.

---

### Step 4: Configure ChatGPT

1. Open ChatGPT (web or desktop app)
2. Go to **Settings** → **Beta Features** → **Model Context Protocol**
3. Click **Add Server**
4. Copy the contents of your `mcp_config.json` file
5. Paste into ChatGPT MCP configuration
6. Click **Save**

**Alternative**: If ChatGPT has a file upload option, upload `mcp_config.json` directly.

---

### Step 5: Verify Connection

In ChatGPT, type:
```
"What MCP tools do you have available?"
```

ChatGPT should respond with something like:
```
"I have access to the following MediScribe tools:
- process_conversation: Process medical conversations with auto-translation
- extract_medical_data: Extract medical data from English text
- search_patient_records: Search for patient records
- get_patient_record: Get a specific record
- get_all_records: List all records
- save_to_database: Save extracted data"
```

✅ **If you see this, you're connected!**

---

## 🎬 First Test

### Test 1: Simple English Conversation

1. In ChatGPT, type:
   ```
   "I'm going to give you a medical conversation to process.
   
   Doctor: Good morning! What's your name?
   Patient: I'm John Doe, 45 years old, male.
   Doctor: What brings you in today?
   Patient: I have a fever and headache for 3 days.
   Doctor: Let me check. Temperature is 101.5F.
   Doctor: I'll prescribe Ibuprofen 400mg three times daily.
   
   Please process this conversation."
   ```

2. ChatGPT will automatically:
   - Call the `process_conversation` tool
   - Send the text to MediScribe
   - Show you the extracted data

3. You should see in your MCP server window:
   ```
   ======================================================================
   📝 Processing conversation from ChatGPT
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
   ```

4. ChatGPT will show you:
   ```
   "I've processed the conversation. Here's the extracted data:
   
   Patient: John Doe, 45 years old, male
   Symptoms: fever, headache (3 days)
   Vital Signs: temperature 101.5F
   Medications: Ibuprofen 400mg three times daily
   
   Saved to database as: REC-20251024103000"
   ```

✅ **If this works, your setup is complete!**

---

### Test 2: Multilingual (Shona)

1. In ChatGPT, type:
   ```
   "Process this Shona medical conversation:
   
   Chiremba: Mangwanani. Zita renyu ndiani?
   Murwere: Ndini Tendai Moyo, ndine makore 42.
   Chiremba: Muri kunzwa sei?
   Murwere: Ndine fivha uye kurwara musoro.
   Chiremba: Tembiricha yenyu iri pa 38.5 degrees.
   Chiremba: Ndichakupai Paracetamol 500mg."
   ```

2. MediScribe will:
   - Detect language: Shona
   - Translate to English
   - Extract medical data
   - Save to database

3. ChatGPT will show the results in English

✅ **If translation works, multilingual support is active!**

---

## 🔧 Troubleshooting

### Issue 1: ChatGPT doesn't see MediScribe tools

**Symptoms**: ChatGPT says "I don't have access to those tools"

**Solutions**:
1. ✅ Make sure MCP server is running (`python mcp_server.py`)
2. ✅ Check the path in `mcp_config.json` is correct
3. ✅ Restart ChatGPT after adding the configuration
4. ✅ Check ChatGPT MCP settings are enabled

---

### Issue 2: MCP server won't start

**Symptoms**: Error when running `python mcp_server.py`

**Solutions**:
```bash
# Install missing packages
pip install mcp spacy transformers torch

# Download spaCy model
python -m spacy download en_core_web_sm

# Check Python version (need 3.8+)
python --version
```

---

### Issue 3: Translation not working

**Symptoms**: Server says "Translation not available"

**Solutions**:
```bash
# Install translation packages
pip install transformers torch

# First run downloads ~2.5GB model (one-time)
# Be patient, it takes a few minutes
```

---

### Issue 4: Path issues in mcp_config.json

**Symptoms**: ChatGPT can't find the server

**Solutions**:
1. Use **forward slashes** `/` not backslashes `\`
2. Use **full absolute path**, not relative
3. Example correct path:
   ```json
   "args": ["C:/Users/John/Documents/mediscribe/mcp_server.py"]
   ```
4. Example wrong paths:
   ```json
   "args": ["mcp_server.py"]  ❌ (relative path)
   "args": ["C:\\Users\\John\\..."]  ❌ (backslashes)
   ```

---

### Issue 5: Server crashes during processing

**Symptoms**: Server stops when processing conversation

**Solutions**:
1. Check server logs for error messages
2. Verify all dependencies installed:
   ```bash
   pip install -r requirements.txt
   ```
3. Try with a simpler conversation first
4. Check available RAM (need ~2-4GB for translation)

---

## 📊 Monitoring

### Server Logs
The MCP server shows real-time logs:
```
📝 Processing conversation from ChatGPT
🔍 Detecting language...
🌐 Translating...
🔬 Extracting medical data...
💾 Saving to database...
```

### Database Records
View saved records:
```bash
python show_records.py
```

Search for patient:
```bash
python mediscribe.py --search "John Doe"
```

---

## 🎯 Usage Tips

### 1. Natural Language with ChatGPT
```
✅ "Process this medical conversation"
✅ "Extract patient data from our discussion"
✅ "Save this consultation"

❌ Don't need technical commands
```

### 2. Voice Mode
1. Enable voice mode in ChatGPT
2. Have your medical conversation
3. Say "Process this conversation"
4. ChatGPT handles the rest!

### 3. Multiple Conversations
```
You: "I have 3 patient consultations to process"
[Provide first conversation]
You: "Process this one"
[Provide second conversation]
You: "Process this one too"
```

### 4. Review Before Saving
```
You: "Extract the data but don't save to database yet"
[ChatGPT shows extracted data]
You: "Looks good, now save it"
```

---

## 🎉 You're Ready!

Once setup is complete:

1. **Keep MCP server running** in the background
2. **Open ChatGPT** and start conversations
3. **Ask ChatGPT to process** medical conversations
4. **Data automatically extracted** and saved

No copy/paste, no manual processing - just natural conversation!

---

## 📚 Next Steps

- **[CHATGPT_MCP_WORKFLOW.md](CHATGPT_MCP_WORKFLOW.md)** - Detailed workflow guide
- **[USAGE_GUIDE.md](USAGE_GUIDE.md)** - Complete usage guide
- **[QUICK_START.md](QUICK_START.md)** - Quick reference

---

## 🆘 Still Having Issues?

1. Check all dependencies: `pip install -r requirements.txt`
2. Verify Python version: `python --version` (need 3.8+)
3. Run test suite: `python test_chatgpt_processor.py`
4. Check server logs for specific errors
5. Try the manual processor first: `python realtime_chatgpt_processor.py`

---

**Happy processing!** 🎉
