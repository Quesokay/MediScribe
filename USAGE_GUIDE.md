# MediScribe - Complete Usage Guide

## 🎯 Three Ways to Use MediScribe

### 1. ChatGPT Voice Mode (Real-time) ⭐ RECOMMENDED

**Best for**: Live conversations, real-time processing

```bash
python realtime_chatgpt_processor.py
```

**Workflow**:
1. Have a conversation in ChatGPT voice mode
2. Copy the transcript from ChatGPT
3. Paste into MediScribe
4. Get structured medical data instantly

**Features**:
- ✅ Real-time processing
- ✅ Multilingual support (auto-detect)
- ✅ Automatic database saving
- ✅ Interactive menu

---

### 2. MCP Server (AI Integration)

**Best for**: Integrating with ChatGPT or other AI assistants

```bash
python mcp_server.py
```

**Setup**:
1. Start the MCP server
2. Configure in ChatGPT settings (copy `mcp_config.json`)
3. Use natural language to call tools

**Example ChatGPT Commands**:
```
"Extract medical data from this conversation: [paste text]"
"Search for patient John Doe"
"Get all medical records from the database"
"Translate this Shona conversation and extract data"
```

**Available Tools**:
- `extract_medical_data` - Extract from English text
- `translate_and_extract` - Translate + extract
- `search_patient_records` - Search by name
- `get_patient_record` - Get by ID
- `get_all_records` - List all records
- `save_to_database` - Save extracted data

---

### 3. File Processing (Batch)

**Best for**: Processing multiple saved transcripts

```bash
# Single file
python mediscribe.py transcript.txt

# Entire folder
python mediscribe.py ./transcriptions/

# View all records
python mediscribe.py --view

# Search patient
python mediscribe.py --search "John Doe"
```

---

## 🌍 Multilingual Processing

### Supported Languages

| Language | Code | Region |
|----------|------|--------|
| English | en | Default |
| Shona | sn | Zimbabwe |
| Ndebele | nd | Zimbabwe/South Africa |
| Zulu | zu | South Africa |
| Xhosa | xh | South Africa |
| Afrikaans | af | South Africa |

### How Translation Works

1. **Auto-detection**: System detects language automatically
2. **NLLB Translation**: Uses Meta's NLLB-200 model (offline)
3. **Extraction**: spaCy extracts medical entities from English text
4. **Storage**: Saves both original and translated text

### Example: Shona Conversation

**Input (Shona)**:
```
Chiremba: Mangwanani. Zita renyu ndiani?
Murwere: Ndini John Doe, ndine makore 45. Ndiri kunzwa kurwara musoro.
Chiremba: Tembiricha yenyu iri pa 38.5 degrees.
```

**Output (Extracted)**:
```json
{
  "patient_name": "John Doe",
  "age": "45",
  "symptoms": [{"text": "headache"}],
  "vital_signs": [{"text": "temperature 38.5 degrees"}],
  "original_language": "shona"
}
```

---

## 📊 Understanding Extracted Data

### What Gets Extracted

1. **Patient Information**
   - Name
   - Age
   - Gender

2. **Clinical Data**
   - Symptoms (complaints, pain, discomfort)
   - Diagnosis (conditions, diseases)
   - Vital signs (temperature, BP, heart rate)
   - Medications (drugs, dosages)
   - Allergies

3. **Care Plan**
   - Treatment plan
   - Follow-up instructions

### Data Format

```json
{
  "patient_name": "Sarah Johnson",
  "age": "28",
  "gender": "female",
  "symptoms": [
    {"text": "headache", "start": 120, "end": 128},
    {"text": "fever", "start": 145, "end": 150}
  ],
  "diagnosis": [
    {"text": "viral infection", "start": 300, "end": 315}
  ],
  "medications": [
    {"text": "Ibuprofen 400mg three times daily", "start": 400, "end": 433}
  ],
  "vital_signs": [
    {"text": "temperature 101.5F", "start": 200, "end": 218},
    {"text": "blood pressure 125/80", "start": 220, "end": 241}
  ],
  "treatment_plan": [
    {"text": "rest and increase fluid intake", "start": 500, "end": 530}
  ],
  "follow_up": [
    {"text": "follow up in one week", "start": 600, "end": 621}
  ],
  "record_id": "REC-20251024103000",
  "timestamp": "2025-10-24T10:30:00",
  "original_language": "english"
}
```

---

## 🎬 Step-by-Step Tutorials

### Tutorial 1: First Conversation

**Goal**: Process your first medical conversation

1. **Start the processor**:
   ```bash
   python realtime_chatgpt_processor.py
   ```

2. **Select option 4** (test with sample)
   - This runs a demo conversation
   - Shows you what to expect

3. **Try your own conversation**:
   - Select option 1 (paste mode)
   - Copy this sample:
   ```
   Doctor: Good morning! What's your name?
   Patient: I'm Jane Smith, 30 years old, female.
   Doctor: What brings you in today?
   Patient: I have a bad cough and sore throat.
   Doctor: Let me check. Temperature is 99.5F. I'll prescribe cough syrup.
   ```
   - Paste and press Enter, then Ctrl+Z, then Enter

4. **View the results**:
   - See extracted data on screen
   - Check database: `python show_records.py`

---

### Tutorial 2: Multilingual Conversation

**Goal**: Process a conversation in Shona

1. **Enable translation**:
   ```bash
   python realtime_chatgpt_processor.py
   ```

2. **Prepare Shona conversation**:
   ```
   Chiremba: Mangwanani. Zita renyu ndiani?
   Murwere: Ndini Tendai Moyo, ndine makore 35, murume.
   Chiremba: Muri kunzwa sei?
   Murwere: Ndine fivha uye kurwara musoro.
   Chiremba: Tembiricha yenyu iri pa 38.8 degrees.
   Chiremba: Ndichakupai Paracetamol 500mg.
   ```

3. **Process**:
   - Select option 1
   - Paste the Shona text
   - System auto-detects language
   - Translates to English
   - Extracts medical data

4. **Review**:
   - Original Shona text saved
   - English translation saved
   - Medical data extracted from English

---

### Tutorial 3: MCP Integration with ChatGPT

**Goal**: Use MediScribe tools directly in ChatGPT

1. **Start MCP server**:
   ```bash
   python mcp_server.py
   ```
   Keep this running in the background

2. **Configure ChatGPT**:
   - Open ChatGPT settings
   - Go to MCP configuration
   - Add MediScribe server:
   ```json
   {
     "mediscribe": {
       "command": "python",
       "args": ["C:/full/path/to/mcp_server.py"]
     }
   }
   ```

3. **Test in ChatGPT**:
   ```
   You: "Use the extract_medical_data tool on this text:
   Patient John Doe, 45 years old, has fever and cough.
   Temperature 101F. Prescribed Amoxicillin 500mg."
   
   ChatGPT: [Calls tool and shows extracted data]
   ```

4. **Try other tools**:
   ```
   "Search for patient records for John Doe"
   "Get all medical records"
   "Save this extracted data to the database"
   ```

---

## 🔧 Configuration & Customization

### Adjust Extraction Rules

Edit `medical_extractor_simple.py`:

```python
# Add custom medical terms
MEDICAL_TERMS = {
    "symptoms": ["headache", "fever", "cough", "pain", "nausea"],
    "medications": ["aspirin", "ibuprofen", "amoxicillin"],
    # Add your terms here
}
```

### Change Database Location

Edit `database_saver.py`:

```python
DB_PATH = "path/to/your/database.db"
```

### Disable Translation

```python
processor = ChatGPTVoiceProcessor(use_translation=False)
```

---

## 🐛 Troubleshooting

### Issue: Translation not working

**Solution**:
```bash
pip install transformers torch
```
First run downloads ~2.5GB model (one-time)

### Issue: spaCy model not found

**Solution**:
```bash
python -m spacy download en_core_web_sm
```

### Issue: MCP server won't start

**Solution**:
```bash
pip install mcp
python mcp_server.py
```
Check for error messages

### Issue: No data extracted

**Possible causes**:
1. Conversation too short (needs 20+ words)
2. No medical keywords detected
3. Text format issue

**Solution**: Try the test conversation first

---

## 📈 Best Practices

### For Accurate Extraction

1. **Clear conversation structure**:
   ```
   Doctor: [question]
   Patient: [response]
   ```

2. **Include key information**:
   - Patient name and age
   - Specific symptoms
   - Vital signs with units
   - Medication names and dosages

3. **Use medical terminology**:
   - "Temperature 101.5F" not "really hot"
   - "Ibuprofen 400mg" not "pain pill"

### For Multilingual Use

1. **Consistent language**: Don't mix languages in one conversation
2. **Standard medical terms**: Use common medical vocabulary
3. **Clear pronunciation**: In voice mode, speak clearly

### For Database Management

1. **Regular backups**:
   ```bash
   copy medical_records.db medical_records_backup.db
   ```

2. **View records regularly**:
   ```bash
   python show_records.py
   ```

3. **Search before adding**: Check for duplicates

---

## 🎯 Common Use Cases

### Use Case 1: Clinical Documentation
- Doctor sees patient
- Uses ChatGPT voice mode to record conversation
- MediScribe extracts structured data
- Saves to EHR system

### Use Case 2: Telemedicine
- Remote consultation via ChatGPT
- Conversation automatically documented
- Medical data extracted and stored

### Use Case 3: Medical Training
- Students practice consultations
- Conversations recorded and analyzed
- Feedback on documentation quality

### Use Case 4: Multilingual Clinic
- Patients speak native language
- Automatic translation to English
- Standardized medical records

---

## 📚 Additional Resources

- **Test Suite**: `python test_chatgpt_processor.py`
- **View Records**: `python show_records.py`
- **Search Records**: `python mediscribe.py --search "name"`
- **Help**: `python mediscribe.py --help`

---

## ⚠️ Important Disclaimers

1. **Not for Production**: This is a research/demonstration tool
2. **Verify Data**: Always review extracted information
3. **Privacy**: Handle patient data according to regulations
4. **Accuracy**: AI extraction may have errors - human review required
