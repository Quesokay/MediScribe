# MediScribe - Quick Start Guide

## 🚀 Get Started in 3 Minutes

### Step 1: Install Dependencies

```bash
# Windows
setup_chatgpt_mode.bat

# Or manually
pip install spacy transformers torch mcp
python -m spacy download en_core_web_sm
```

### Step 2: Choose Your Mode

#### A. Interactive Mode (Easiest)
```bash
python realtime_chatgpt_processor.py
```
- Select option 4 to test with sample conversation
- Select option 1 to paste your own conversation

#### B. MCP Server Mode (For ChatGPT Integration)
```bash
python mcp_server.py
```
- Keep running in background
- Configure in ChatGPT settings
- Use natural language to call tools

### Step 3: Try It Out

**Sample Conversation to Test**:
```
Doctor: Good morning! What's your name and age?
Patient: I'm John Smith, 45 years old, male.
Doctor: What brings you in today?
Patient: I have a severe headache and fever for 3 days.
Doctor: Let me check. Temperature is 101.5F, BP is 130/85.
Patient: I also have a dry cough.
Doctor: I'll prescribe Ibuprofen 400mg three times daily.
```

Copy this, paste into the processor, and see the magic! ✨

---

## 📱 Using with ChatGPT Voice Mode

### The Workflow

1. **Have a conversation** in ChatGPT voice mode
   - Talk naturally about medical topics
   - Can be in English, Shona, Ndebele, Zulu, Xhosa, or Afrikaans

2. **Copy the transcript** from ChatGPT
   - ChatGPT provides text of voice conversations

3. **Process with MediScribe**
   ```bash
   python realtime_chatgpt_processor.py
   ```
   - Select option 1 (paste mode)
   - Paste conversation
   - Press Enter, Ctrl+Z, Enter

4. **Get structured data**
   - Patient information
   - Symptoms
   - Diagnosis
   - Medications
   - Vital signs
   - All saved to database!

---

## 🎯 What You Get

### Input (Conversation)
```
Doctor: Hi, what's your name?
Patient: I'm Sarah, 28 years old. I have a headache and fever.
Doctor: Temperature is 101.5F. I'll prescribe Ibuprofen 400mg.
```

### Output (Structured Data)
```json
{
  "patient_name": "Sarah",
  "age": "28",
  "symptoms": ["headache", "fever"],
  "vital_signs": ["temperature 101.5F"],
  "medications": ["Ibuprofen 400mg"],
  "record_id": "REC-20251024103000"
}
```

---

## 🌍 Multilingual Example

### Shona Conversation
```
Chiremba: Zita renyu ndiani?
Murwere: Ndini John, ndine makore 45. Ndine fivha.
Chiremba: Tembiricha yenyu iri pa 38.5 degrees.
```

### Automatic Translation + Extraction
```json
{
  "patient_name": "John",
  "age": "45",
  "symptoms": ["fever"],
  "vital_signs": ["temperature 38.5 degrees"],
  "original_language": "shona"
}
```

---

## 🔧 MCP Integration (Advanced)

### 1. Start MCP Server
```bash
python mcp_server.py
```

### 2. Configure ChatGPT
Add to ChatGPT MCP settings:
```json
{
  "mediscribe": {
    "command": "python",
    "args": ["C:/full/path/to/mcp_server.py"]
  }
}
```

### 3. Use in ChatGPT
```
You: "Extract medical data from: Patient John Doe, 45, has fever. 
     Temperature 101F. Prescribed Amoxicillin."

ChatGPT: [Uses extract_medical_data tool]
         Here's the extracted data: ...
```

---

## 📊 View Your Data

### See All Records
```bash
python show_records.py
```

### Search for Patient
```bash
python mediscribe.py --search "John Doe"
```

### Get Specific Record
```bash
python mediscribe.py --view
```

---

## 🧪 Test Everything

```bash
python test_chatgpt_processor.py
```

This runs:
- ✅ English conversation test
- ✅ Multilingual translation test
- ✅ Group consultation test

---

## 💡 Tips for Best Results

### 1. Clear Structure
```
Doctor: [question]
Patient: [response]
```

### 2. Include Key Info
- Patient name and age
- Specific symptoms
- Vital signs with units (101.5F, 130/85)
- Medication names and dosages

### 3. Use Medical Terms
- ✅ "Temperature 101.5F"
- ❌ "Really hot"
- ✅ "Ibuprofen 400mg"
- ❌ "Pain pill"

---

## 🐛 Troubleshooting

### "Module not found"
```bash
pip install spacy transformers torch mcp
```

### "spaCy model not found"
```bash
python -m spacy download en_core_web_sm
```

### "Translation not working"
```bash
pip install transformers torch
```
First run downloads ~2.5GB model (one-time)

### "No data extracted"
- Make sure conversation has medical keywords
- Needs at least 20 words
- Try the test conversation first

---

## 📚 Learn More

- **Full Guide**: `USAGE_GUIDE.md`
- **ChatGPT Integration**: `README_CHATGPT_INTEGRATION.md`
- **Main README**: `README.md`

---

## 🎉 You're Ready!

Start with:
```bash
python realtime_chatgpt_processor.py
```

Select option 4 for a demo, then try your own conversations!

---

## ⚠️ Important

- This is a research/demo tool
- Not for production medical use
- Always verify extracted data
- Handle patient data per regulations
