# Network Issues - Alternative Solutions

## Problem

Your internet connection is timing out when trying to download the 2.5GB NLLB translation model.

## Immediate Solution: Use Without Translation

For now, use the **standard (English-only) version** which doesn't require the large model download:

```bash
# Use the standard watcher (no translation)
python vibe_watcher.py
```

This will work immediately with your current setup!

## Future: Add Translation When You Have Better Internet

### Option 1: Download Model Later (Recommended)

When you have access to better/faster internet:

1. **Download the model separately:**
   ```bash
   python -c "from transformers import AutoTokenizer, AutoModelForSeq2SeqLM; AutoTokenizer.from_pretrained('facebook/nllb-200-distilled-600M'); AutoModelForSeq2SeqLM.from_pretrained('facebook/nllb-200-distilled-600M')"
   ```

2. **Then use multilingual watcher:**
   ```bash
   python vibe_watcher_multilingual.py
   ```

### Option 2: Use Google Translate API (No Large Download)

If you have API access, use Google Translate instead:

1. **Get Google Cloud Translation API key**
2. **Edit `vibe_config_multilingual.json`:**
   ```json
   {
     "translation_method": "google",
     "google_api_key": "your-key-here"
   }
   ```

3. **Install Google client:**
   ```bash
   pip install google-cloud-translate
   ```

4. **Run:**
   ```bash
   python vibe_watcher_multilingual.py
   ```

### Option 3: Manual Translation Workflow

For now, you can:

1. **Use Vibe normally** (transcribe in Shona/Ndebele)
2. **Manually translate** using online tools
3. **Save English version**
4. **Process with MediScribe:**
   ```bash
   python batch_process.py english_transcript.txt
   ```

## Tips for Downloading Large Models

### Increase Timeout
```bash
# Set longer timeout
set HF_HUB_DOWNLOAD_TIMEOUT=600
python vibe_watcher_multilingual.py
```

### Use Better Internet
- Try during off-peak hours
- Use wired connection instead of WiFi
- Try from a location with better internet
- Use mobile hotspot if faster

### Download in Parts
The model will resume if interrupted. Keep trying:
```bash
python vibe_watcher_multilingual.py
# If it fails, run again - it will resume
```

## Current Working Setup

**What works NOW:**
```bash
# Standard English-only version
python vibe_watcher.py
```

**What you have:**
- ✅ Automatic Vibe integration
- ✅ Medical information extraction
- ✅ Database storage
- ✅ Searchable records
- ❌ Translation (needs model download)

**What you need for translation:**
- Better internet connection OR
- Google Translate API key OR
- Manual translation workflow

## Recommendation

**For immediate use:**
1. Use `python vibe_watcher.py` (English only)
2. Test with English transcripts
3. Get familiar with the system

**When ready for multilingual:**
1. Find better internet connection
2. Download NLLB model (one-time, ~2.5GB)
3. Switch to `python vibe_watcher_multilingual.py`

## Alternative: Smaller Translation Model

If 2.5GB is too large, you could use a smaller model (lower quality but faster download):

Edit `translator.py`, line 54, change:
```python
model_name = "facebook/nllb-200-distilled-600M"  # 2.5GB
```

To:
```python
model_name = "facebook/nllb-200-distilled-1.3B"  # 5GB (better quality)
# OR
model_name = "Helsinki-NLP/opus-mt-mul-en"  # ~300MB (lower quality)
```

## Summary

**Right now:** Use English-only version
```bash
python vibe_watcher.py
```

**Later:** Add translation when you have better internet
```bash
python vibe_watcher_multilingual.py
```

Both versions work with Vibe and extract medical information - translation is just an optional add-on!
