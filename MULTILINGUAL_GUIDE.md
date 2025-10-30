# Multilingual MediScribe Guide

## 🌐 Overview

MediScribe now supports **multilingual medical conversations**! Patients can speak in their native language (Shona, Ndebele, Zulu, Xhosa, Afrikaans), and MediScribe will automatically translate to English before extracting medical information.

## Supported Languages

✅ **Shona** (Zimbabwe)
✅ **Ndebele** (Zimbabwe, South Africa)
✅ **Zulu** (South Africa)
✅ **Xhosa** (South Africa)
✅ **Afrikaans** (South Africa, Namibia)
✅ **English** (no translation needed)

## How It Works

```
┌─────────────────────────────────────────────────────────────┐
│  PATIENT SPEAKS IN NATIVE LANGUAGE                          │
│  (Shona, Ndebele, Zulu, Xhosa, Afrikaans)                  │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  VIBE TRANSCRIBES                                           │
│  (Speech → Text in original language)                       │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  MEDISCRIBE DETECTS LANGUAGE                                │
│  (Automatic language detection)                             │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  MEDISCRIBE TRANSLATES TO ENGLISH                           │
│  (Using NLLB or Google Translate)                           │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  MEDISCRIBE EXTRACTS MEDICAL INFORMATION                    │
│  (Patient data, symptoms, diagnosis, medications)           │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  SAVES TO DATABASE                                          │
│  (With original language and translation metadata)          │
└─────────────────────────────────────────────────────────────┘
```

## Translation Methods

### 1. NLLB (Recommended) ⭐

**No Language Left Behind** by Meta AI

**Pros:**

- ✅ Completely offline (no internet needed)
- ✅ Free (no API costs)
- ✅ Privacy-first (data never leaves your machine)
- ✅ Supports 200+ languages
- ✅ Good quality for African languages

**Cons:**

- ⚠️ First download: ~2.5GB model
- ⚠️ Slightly slower than Google (still fast: 2-5 seconds)

**Setup:**

```bash
pip install transformers torch sentencepiece
```

### 2. Google Translate API

**Pros:**

- ✅ Very fast translation
- ✅ High quality
- ✅ No model download needed

**Cons:**

- ⚠️ Requires internet connection
- ⚠️ Costs money (pay per character)
- ⚠️ Data sent to Google servers
- ⚠️ Requires API key

**Setup:**

```bash
pip install google-cloud-translate
# Set API key in vibe_config_multilingual.json
```

## Quick Start

### Step 1: Install Dependencies

```bash
pip install transformers torch sentencepiece protobuf
```

### Step 2: Configure

Edit `vibe_config_multilingual.json`:

```json
{
  "watch_directory": "C:\\Users\\YourName\\Documents\\Vibe Transcripts",
  "translation_method": "nllb",
  "source_language": null,
  "supported_languages": [
    "shona",
    "ndebele",
    "zulu",
    "xhosa",
    "afrikaans",
    "english"
  ]
}
```

**Options:**

- `translation_method`: `"nllb"` (offline) or `"google"` (API)
- `source_language`: `null` (auto-detect) or specific language
- `google_api_key`: Your Google API key (if using Google)

### Step 3: Start Multilingual Service

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

### Step 4: Use Vibe Normally

1. Patient speaks in their native language
2. Vibe transcribes (in original language)
3. Save transcript
4. MediScribe automatically:
   - Detects language
   - Translates to English
   - Extracts medical information
   - Saves both versions

## Example Conversations

### Shona Example

**Original (Shona):**

```
Chiremba: Mangwanani. Zita renyu ndiani?
Murwere: Zita rangu ndinonzi Tendai Moyo. Ndine makore 35.

Chiremba: Chii chinokutambudzai nhasi?
Murwere: Ndiri kunzwa kurwara musoro kwevhiki yese.
         Ndine fivha uye ndiri kunzwa kuneta.

Chiremba: Tembiricha yenyu yakaita sei?
Murwere: Yakaita 38.5 degrees manheru ano.

Diagnosis: Mufivha wemukati.
Mushonga: Paracetamol 500mg katatu pazuva kwemazuva manomwe.
```

**Translated (English):**

```
Doctor: Good morning. What is your name?
Patient: My name is Tendai Moyo. I am 35 years old.

Doctor: What is troubling you today?
Patient: I have been having headaches for a week.
         I have a fever and I feel tired.

Doctor: What was your temperature?
Patient: It was 38.5 degrees this evening.

Diagnosis: Internal fever/flu.
Medication: Paracetamol 500mg three times daily for seven days.
```

### Ndebele Example

**Original (Ndebele):**

```
Udokotela: Sawubona. Ungubani igama lakho?
Isiguli: Igama lami nginguNomsa Dube. Ngineminyaka engu-28.

Udokotela: Yini ekuhluphelayo lamuhla?
Isiguli: Nginobuhlungu besifuba lokukhwehlela okwensuku ezintathu.

Udokotela: Izinga lokushisa lakho linjani?
Isiguli: Lithi 38.2 degrees ekuseni.

Diagnosis: Isifo lwamaphaphu.
Imithi: Amoxicillin 500mg kathathu ngosuku okwensuku eziyisikhombisa.
```

**Translated (English):**

```
Doctor: Hello. What is your name?
Patient: My name is Nomsa Dube. I am 28 years old.

Doctor: What is troubling you today?
Patient: I have chest pain and coughing for three days.

Doctor: What is your temperature?
Patient: It is 38.2 degrees in the morning.

Diagnosis: Lung infection/pneumonia.
Medication: Amoxicillin 500mg three times daily for seven days.
```

## Testing

### Test Translation

```bash
python test_translation.py
```

This will:

- Test Shona → English translation
- Test Ndebele → English translation
- Test automatic language detection
- Test full pipeline (translation + extraction)

### Test with Sample Files

Create a test file in Shona:

**test_shona.txt:**

```
Murwere: John Doe, makore 45, murume.
Ndiri kunzwa kurwara musoro uye ndine fivha.
Tembiricha: 38.6 degrees. BP: 130/85.

Diagnosis: Mufivha wemukati.
Mushonga: Paracetamol 500mg katatu pazuva.
```

Save to your watch directory and MediScribe will:

1. Detect it's Shona
2. Translate to English
3. Extract medical information
4. Save both versions

## File Structure

After processing a multilingual transcript:

```
Vibe Transcripts/
├── patient_shona.txt                    ← Original (Shona)
├── patient_shona_english.txt            ← Translated (English)
└── patient_shona_mediscribe.json        ← Extracted data
```

The JSON file includes:

```json
{
  "patient_name": "John Doe",
  "age": "45",
  "gender": "male",
  "original_language": "shona",
  "translation_method": "nllb",
  "original_text": "Murwere: John Doe...",
  "symptoms": [...],
  "diagnosis": [...],
  "medications": [...]
}
```

## Configuration Options

### vibe_config_multilingual.json

```json
{
  "watch_directory": "C:\\path\\to\\transcripts",
  "file_extensions": [".txt", ".srt", ".vtt", ".json"],
  "auto_process": true,
  "translation_method": "nllb",
  "source_language": null,
  "google_api_key": null,
  "supported_languages": [
    "shona",
    "ndebele",
    "zulu",
    "xhosa",
    "afrikaans",
    "english"
  ],
  "save_extracted_json": true,
  "notification_sound": true
}
```

**Key Options:**

- `translation_method`:

  - `"nllb"` - Offline, free, privacy-first (recommended)
  - `"google"` - Online, paid, requires API key

- `source_language`:

  - `null` - Auto-detect language (recommended)
  - `"shona"` - Force Shona
  - `"ndebele"` - Force Ndebele
  - etc.

- `google_api_key`:
  - Your Google Cloud Translation API key
  - Only needed if using `"google"` method

## Language Detection

MediScribe automatically detects the language using keyword matching:

**Shona indicators:**

- ndiri, ndinoda, ndine, murwere, chipatara, mushonga

**Ndebele indicators:**

- ngiyafuna, ngilapha, umkhuhlane, isibhedlela, umuthi

**English:**

- Default if no other language detected

For more accurate detection, you can specify the language in the config.

## Troubleshooting

### Model Download Issues

**Problem:** NLLB model download fails or is slow

**Solution:**

```bash
# Pre-download the model
python -c "from transformers import AutoTokenizer, AutoModelForSeq2SeqLM; \
           AutoTokenizer.from_pretrained('facebook/nllb-200-distilled-600M'); \
           AutoModelForSeq2SeqLM.from_pretrained('facebook/nllb-200-distilled-600M')"
```

### Translation Quality Issues

**Problem:** Translation is not accurate

**Solutions:**

1. Use Google Translate API for better quality
2. Ensure medical terminology is clear in original language
3. Speak in complete sentences
4. Use standard medical terms when possible

### Language Not Detected

**Problem:** Wrong language detected

**Solution:**

- Set `source_language` explicitly in config:
  ```json
  {
    "source_language": "shona"
  }
  ```

### Memory Issues

**Problem:** System runs out of memory

**Solution:**

- Use smaller NLLB model: `facebook/nllb-200-distilled-600M` (default)
- Close other applications
- Process files one at a time

## Performance

### NLLB (Offline)

- **First run:** 30-60 seconds (model loading)
- **Subsequent runs:** 2-5 seconds per transcript
- **Memory:** ~2GB RAM
- **Disk:** ~2.5GB for model

### Google Translate (Online)

- **Translation:** < 1 second
- **Memory:** ~100MB RAM
- **Disk:** Minimal
- **Cost:** ~$20 per 1 million characters

## Privacy & Security

### NLLB (Recommended)

- ✅ All processing happens locally
- ✅ No data sent to external servers
- ✅ HIPAA-compliant
- ✅ Works offline
- ✅ No API keys needed

### Google Translate

- ⚠️ Data sent to Google servers
- ⚠️ Requires internet connection
- ⚠️ Subject to Google's privacy policy
- ⚠️ May not be HIPAA-compliant without BAA

## Use Cases

### 1. Rural Clinics in Zimbabwe

- Patients speak Shona or Ndebele
- Doctors document in English
- MediScribe bridges the language gap

### 2. Multilingual Hospitals

- Patients from different regions
- Staff speaks various languages
- Consistent English medical records

### 3. Community Health Workers

- Work with local populations
- Need standardized documentation
- Automatic translation saves time

## Best Practices

1. **Speak Clearly:** Better transcription = better translation
2. **Use Medical Terms:** Standard terms translate better
3. **Complete Sentences:** Helps with context and accuracy
4. **Review Translations:** Always verify critical information
5. **Keep Original:** Both versions are saved for reference

## Commands Reference

```bash
# Start multilingual service
python vibe_watcher_multilingual.py

# Test translation
python test_translation.py

# Test specific language
python translator.py

# View records (includes language info)
python view_database.py
```

## Next Steps

1. **Install dependencies:** `pip install transformers torch sentencepiece`
2. **Configure:** Edit `vibe_config_multilingual.json`
3. **Test:** Run `python test_translation.py`
4. **Start service:** Run `python vibe_watcher_multilingual.py`
5. **Use Vibe:** Patients speak in any supported language!

## Support

For issues or questions:

1. Run `python test_translation.py` to verify setup
2. Check console output for translation status
3. Review `MULTILINGUAL_GUIDE.md` (this file)
4. Test with sample conversations

---

**Making healthcare accessible in every language! 🌐🏥**
