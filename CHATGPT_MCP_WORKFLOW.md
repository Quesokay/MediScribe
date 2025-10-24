# ChatGPT MCP Workflow - Automatic Conversation Processing

## 🎯 The New Workflow

Instead of copying and pasting, ChatGPT automatically sends conversation transcripts to MediScribe!

```
┌─────────────────────────────────────────────────────────────────┐
│  1. User connects ChatGPT to MediScribe MCP server             │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│  2. User has medical conversation in ChatGPT voice mode         │
│     (Can be in English, Shona, Ndebele, Zulu, Xhosa, etc.)    │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│  3. User asks ChatGPT to process the conversation               │
│     "Process this medical conversation"                         │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│  4. ChatGPT calls MediScribe MCP tool automatically             │
│     Tool: process_conversation                                  │
│     Data: Full conversation transcript                          │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│  5. MediScribe processes:                                       │
│     • Auto-detects language                                     │
│     • Translates to English (if needed via NLLB)               │
│     • Extracts medical entities (via spaCy)                    │
│     • Saves to database                                         │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│  6. ChatGPT receives structured data and shows to user          │
│     • Patient information                                       │
│     • Symptoms                                                  │
│     • Diagnosis                                                 │
│     • Medications                                               │
│     • Record ID                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Setup (One-Time)

### Step 1: Start MediScribe MCP Server

```bash
python mcp_server.py
```

Keep this running in the background. You'll see:
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

### Step 2: Configure ChatGPT

1. Open ChatGPT settings
2. Go to MCP configuration
3. Add MediScribe server:

```json
{
  "mediscribe": {
    "command": "python",
    "args": ["C:/full/path/to/your/mcp_server.py"],
    "disabled": false
  }
}
```

**Important**: Replace `C:/full/path/to/your/mcp_server.py` with the actual path!

### Step 3: Verify Connection

In ChatGPT, ask:
```
"What MCP tools do you have available?"
```

You should see `process_conversation` and other MediScribe tools listed.

---

## 💬 Using the System

### Basic Workflow

1. **Have a conversation** in ChatGPT voice mode:
   ```
   You: "I need to document a patient consultation"
   
   [Enable voice mode and have the conversation]
   
   Doctor: Good morning, what brings you in today?
   Patient: Hi doctor, I'm John Doe, 45 years old. I have a fever and headache.
   Doctor: Let me check. Temperature is 101.5F. I'll prescribe Ibuprofen 400mg.
   ```

2. **Ask ChatGPT to process it**:
   ```
   You: "Process this medical conversation and extract the data"
   ```

3. **ChatGPT automatically**:
   - Calls the `process_conversation` tool
   - Sends the transcript to MediScribe
   - Receives structured data
   - Shows you the results

4. **You get the results**:
   ```
   ChatGPT: "I've processed the conversation. Here's what I extracted:
   
   Patient: John Doe, 45 years old
   Symptoms: fever, headache
   Vital Signs: temperature 101.5F
   Medications: Ibuprofen 400mg
   
   Saved to database as: REC-20251024103000"
   ```

---

## 🌍 Multilingual Example

### Shona Conversation

1. **Have conversation in Shona**:
   ```
   Chiremba: Mangwanani. Zita renyu ndiani?
   Murwere: Ndini Tendai Moyo, ndine makore 42. Ndine fivha.
   Chiremba: Tembiricha yenyu iri pa 38.5 degrees.
   ```

2. **Ask ChatGPT to process**:
   ```
   You: "Process this medical conversation"
   ```

3. **MediScribe automatically**:
   - Detects language: Shona
   - Translates to English via NLLB
   - Extracts medical data
   - Saves to database

4. **ChatGPT shows results**:
   ```
   ChatGPT: "I've processed the Shona conversation. Here's the extracted data:
   
   Original Language: Shona
   Patient: Tendai Moyo, 42 years old
   Symptoms: fever
   Vital Signs: temperature 38.5 degrees
   
   The conversation was automatically translated and saved."
   ```

---

## 🎯 Example Prompts for ChatGPT

### After a Voice Conversation

```
"Process this medical conversation and save it to the database"

"Extract medical data from our conversation"

"Analyze this patient consultation and structure the data"

"Save this medical conversation to MediScribe"
```

### Searching Records

```
"Search for patient records for John Doe"

"Get all recent medical records"

"Find the record with ID REC-20251024103000"

"Show me the last 10 patient records"
```

### Multilingual

```
"Process this Shona medical conversation"

"This conversation is in Ndebele, please process it"

"Extract data from this multilingual consultation"
```

---

## 🔧 Advanced Usage

### Custom Processing

```
You: "Process this conversation but don't save to database yet"

ChatGPT: [Calls process_conversation with save_to_db=false]
```

### Review Before Saving

```
You: "Extract the data first, let me review it, then save"

ChatGPT: [Shows extracted data]

You: "Looks good, now save it"

ChatGPT: [Calls save_to_database tool]
```

### Batch Processing

```
You: "I have 3 conversations to process. Here's the first one..."

[Repeat for each conversation]
```

---

## 📊 What Gets Processed

### Automatic Detection
- ✅ Language (English, Shona, Ndebele, Zulu, Xhosa, Afrikaans)
- ✅ Patient name, age, gender
- ✅ Symptoms
- ✅ Diagnosis
- ✅ Medications and dosages
- ✅ Vital signs (temperature, BP, heart rate)
- ✅ Allergies
- ✅ Treatment plan
- ✅ Follow-up instructions

### Automatic Actions
- ✅ Translation (if not English)
- ✅ Entity extraction
- ✅ Database storage
- ✅ Record ID generation

---

## 🎬 Complete Example Session

```
User: [Enables voice mode in ChatGPT]

User: "Let me document a patient visit"

[Voice conversation]
Doctor: Good morning! What's your name?
Patient: I'm Sarah Johnson, 28 years old, female.
Doctor: What brings you in?
Patient: I have a terrible headache and fever for 3 days.
Doctor: Let me check. Temperature is 101.5F, BP is 125/80.
Patient: I also have a dry cough.
Doctor: I'll prescribe Ibuprofen 400mg three times daily.

User: "Process this medical conversation"

ChatGPT: "I'll process that conversation using MediScribe."

[ChatGPT calls process_conversation tool]

ChatGPT: "I've successfully processed the conversation. Here's the extracted data:

**Patient Information:**
- Name: Sarah Johnson
- Age: 28 years old
- Gender: Female

**Symptoms:**
- Headache (3 days)
- Fever (3 days)
- Dry cough

**Vital Signs:**
- Temperature: 101.5°F
- Blood Pressure: 125/80

**Medications:**
- Ibuprofen 400mg, three times daily

**Record Details:**
- Record ID: REC-20251024103000
- Language: English
- Saved to database: Yes

The medical data has been structured and saved to your database."

User: "Great! Can you search for all records for Sarah Johnson?"

ChatGPT: [Calls search_patient_records tool]

ChatGPT: "I found 1 record for Sarah Johnson:

Record ID: REC-20251024103000
Date: 2025-10-24
Diagnosis: Not specified in this visit
Medications: Ibuprofen 400mg

Would you like to see more details?"
```

---

## 🔍 Monitoring the Server

While the MCP server is running, you'll see real-time logs:

```
======================================================================
📝 Processing conversation from ChatGPT
   Time: 2025-10-24 10:30:00
   Length: 450 characters
======================================================================
🔍 Detecting language...
   Detected: English
   ✓ Already in English
🔬 Extracting medical data...
   ✓ Extraction complete
💾 Saving to database...
   ✓ Saved as: REC-20251024103000

📊 Summary:
   Patient: Sarah Johnson
   Symptoms: 3 found
   Diagnosis: 0 found
   Medications: 1 found
======================================================================
```

---

## 🐛 Troubleshooting

### ChatGPT doesn't see MediScribe tools

**Solution**:
1. Make sure MCP server is running: `python mcp_server.py`
2. Check MCP configuration in ChatGPT settings
3. Verify the path in `mcp_config.json` is correct
4. Restart ChatGPT

### Translation not working

**Solution**:
```bash
pip install transformers torch
```
First run downloads ~2.5GB NLLB model (one-time)

### No data extracted

**Possible causes**:
1. Conversation too short (needs medical keywords)
2. Not a medical conversation
3. Language not supported

**Solution**: Try with a clear medical conversation first

### Server crashes

**Solution**:
1. Check Python version (3.8+)
2. Verify all dependencies: `pip install -r requirements.txt`
3. Check server logs for errors

---

## 💡 Tips for Best Results

### 1. Clear Medical Conversations
```
✅ Good:
"Patient John Doe, 45 years old, has fever and cough. 
Temperature 101.5F. Prescribed Amoxicillin 500mg."

❌ Too vague:
"Someone is sick and needs medicine."
```

### 2. Include Key Information
- Patient name and age
- Specific symptoms
- Vital signs with units
- Medication names and dosages

### 3. Natural Language with ChatGPT
```
✅ "Process this medical conversation"
✅ "Extract the patient data from our discussion"
✅ "Save this consultation to the database"

❌ Don't need to specify tool names or parameters
```

### 4. Review Before Saving
```
You: "Extract the data but don't save yet"
[Review the extracted data]
You: "Looks good, save it now"
```

---

## 🎉 Benefits of This Workflow

### No Copy/Paste Required
- ChatGPT handles everything automatically
- Just have the conversation and ask to process

### Automatic Language Detection
- Speak in any supported language
- MediScribe detects and translates automatically

### Real-Time Processing
- Immediate results
- Instant database storage

### Natural Interaction
- Use natural language with ChatGPT
- No need to remember tool names or parameters

### Complete Audit Trail
- Server logs all processing
- Database stores all records
- Easy to review and search

---

## 📚 Related Documentation

- **[QUICK_START.md](QUICK_START.md)** - Quick setup guide
- **[README_CHATGPT_INTEGRATION.md](README_CHATGPT_INTEGRATION.md)** - Detailed integration guide
- **[USAGE_GUIDE.md](USAGE_GUIDE.md)** - Complete usage guide
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture

---

## ⚠️ Important Notes

1. **Keep MCP server running**: The server must be running for ChatGPT to connect
2. **First translation is slow**: NLLB model loads on first use (~2.5GB)
3. **Review extracted data**: Always verify medical information
4. **Not for production**: This is a research/demonstration tool

---

**Ready to use!** Start the MCP server and connect ChatGPT to begin processing conversations automatically.
