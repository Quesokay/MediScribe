# Multilingual MediScribe - Quick Start (10 Minutes)

## 🌐 What This Does

Patients speak in **Shona, Ndebele, Zulu, Xhosa, or Afrikaans** → MediScribe automatically translates to English → Extracts medical information → Saves to database

## Step 1: Install Translation Dependencies (5 min)

```bash
pip install transformers torch sentencepiece protobuf
```

**Note:** First run will download ~2.5GB NLLB model (one-time only)

## Step 2: Configure (2 min)

Edit `vibe_config_multilingual.json`:

```json
{
  "watch_directory": "C:\\Users\\YourName\\Documents\\Vibe Transcripts",
  "translation_method": "nllb"
}
```

**Important:** Use double backslashes `\\` on Windows!

## Step 3: Start Multilingual Service (1 min)

```bash
python vibe_watcher_multilingual.py
```

You should see:

```
✓ Multilingual Vibe-MediScribe Integration Active
✓ Translation: NLLB
✓ Supported languages: Shona, Ndebele, Zulu, Xhosa, Afrikaans
👀 Monitoring for new transcripts in any supported language...
```

## Step 4: Test It! (2 min)

```bash
python test_translation.py
```

This tests:

- ✅ Shona → English translation
- ✅ Ndebele → English translation
- ✅ Full pipeline (translation + extraction)

## Step 5: Use with Vibe

1. **Patient speaks** in Shona, Ndebele, or any supported language
2. **Vibe transcribes** (in original language)
3. **Review** transcript in Vibe
4. **Save** transcript
5. **MediScribe automatically:**
   - Detects language
   - Translates to English
   - Extracts medical info
   - Saves both versions

## That's It! 🎉

Now patients can speak in their native language and you'll get structured English medical records automatically.

## Example Output

**Original (Shona):**

```
Murwere: John Doe, makore 45, murume.
Ndiri kunzwa kurwara musoro uye ndine fivha.
```

**Translated (English):**

```
Patient: John Doe, 45 years old, male.
I am feeling headache and I have fever.
```

**Extracted Data:**

```json
{
  "patient_name": "John Doe",
  "age": "45",
  "gender": "male",
  "original_language": "shona",
  "symptoms": ["headache", "fever"]
}
```

## Files Created

After processing:

```
Vibe Transcripts/
├── patient_visit.txt              ← Original (Shona)
├── patient_visit_english.txt      ← Translated (English)
└── patient_visit_mediscribe.json  ← Extracted data
```

## Supported Languages

✅ Shona (Zimbabwe)
✅ Ndebele (Zimbabwe, South Africa)
✅ Zulu (South Africa)
✅ Xhosa (South Africa)
✅ Afrikaans (South Africa, Namibia)
✅ English (no translation)

## Translation Methods

### NLLB (Default) ⭐

- ✅ Completely offline
- ✅ Free
- ✅ Privacy-first
- ⚠️ ~2.5GB download (one-time)

### Google Translate (Optional)

- ✅ Very fast
- ✅ High quality
- ⚠️ Requires API key
- ⚠️ Costs money
- ⚠️ Needs internet

## Commands

```bash
# Start multilingual service
python vibe_watcher_multilingual.py

# Test translation
python test_translation.py

# View records
python view_database.py

# Search patient
python mediscribe.py --search "Patient Name"
```

## Troubleshooting

**Model download slow?**

- Be patient, it's a one-time 2.5GB download
- Use good internet connection

**Translation not accurate?**

- Ensure clear speech in Vibe
- Use complete sentences
- Consider Google Translate API for better quality

**Language not detected?**

- Set `source_language` in config:
  ```json
  {
    "source_language": "shona"
  }
  ```

## Need More Help?

- **Complete guide:** `MULTILINGUAL_GUIDE.md`
- **Test translation:** `python test_translation.py`
- **Original Vibe guide:** `VIBE_INTEGRATION.md`

---

**Making healthcare accessible in every language! 🌐🏥**
