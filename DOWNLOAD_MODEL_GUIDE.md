# Download NLLB Translation Model

## Overview

To use multilingual features (Shona, Ndebele, Zulu, Xhosa, Afrikaans), you need to download the NLLB model once.

**Size:** ~2.5GB
**Time:** 30-60 minutes with slow internet (one-time only)
**After download:** Works offline forever!

## Option 1: Automatic Download with Retries (Recommended)

This script handles timeouts and automatically retries:

```bash
python download_nllb_model.py
```

**Features:**
- ✅ Automatically retries on timeout
- ✅ Resumes from where it stopped
- ✅ Shows progress
- ✅ Handles slow connections

**What it does:**
1. Checks if model is already downloaded
2. Downloads with 10-minute timeout per file
3. Retries up to 10 times if it fails
4. Resumes download if interrupted

## Option 2: Manual Download

If the automatic script doesn't work, try downloading manually:

```bash
python -c "from transformers import AutoTokenizer, AutoModelForSeq2SeqLM; AutoTokenizer.from_pretrained('facebook/nllb-200-distilled-600M'); AutoModelForSeq2SeqLM.from_pretrained('facebook/nllb-200-distilled-600M')"
```

**If it times out:**
- Just run the same command again
- It will resume from where it stopped
- Keep trying until it completes

## Option 3: Download from Better Internet

If your home internet is too slow:

1. **Take your laptop to:**
   - Office with faster internet
   - Friend's house with good WiFi
   - Internet café
   - Library with free WiFi

2. **Run the download there:**
   ```bash
   python download_nllb_model.py
   ```

3. **Bring laptop back home**
   - Model is cached on your machine
   - Works offline forever after download

## Option 4: Use Google Translate API (No Download)

If downloading is impossible, use Google Translate instead:

**Pros:**
- No large download needed
- Very fast translation
- High quality

**Cons:**
- Requires internet for each translation
- Costs money (~$20 per 1 million characters)
- Needs API key

**Setup:**
1. Get Google Cloud Translation API key
2. Edit `vibe_config_multilingual.json`:
   ```json
   {
     "translation_method": "google",
     "google_api_key": "your-key-here"
   }
   ```
3. Install: `pip install google-cloud-translate`
4. Run: `python vibe_watcher_multilingual.py`

## Tips for Successful Download

### 1. Best Time to Download
- **Late night** (2 AM - 6 AM) - Less network congestion
- **Early morning** (5 AM - 7 AM) - Before peak hours
- **Weekdays** - Less traffic than weekends

### 2. Connection Tips
- Use **wired connection** (Ethernet) instead of WiFi
- **Close other apps** using internet (YouTube, downloads, etc.)
- **Disable auto-updates** on Windows/apps
- **Pause cloud sync** (OneDrive, Dropbox, etc.)

### 3. If Download Keeps Failing
- Try from a **different location** with better internet
- Use **mobile hotspot** if it's faster
- Download during **off-peak hours**
- Consider **Google Translate API** instead

### 4. Monitor Progress
The download happens in parts:
1. Tokenizer files (~5MB) - Fast
2. Model config (~1KB) - Fast  
3. Model weights (~2.5GB) - Slow, this is the big one

If it fails, it will resume from the last completed part.

## Checking Download Status

### Check if model is downloaded:
```bash
python -c "from pathlib import Path; cache=Path.home()/'.cache'/'huggingface'/'hub'; print('Model found!' if list(cache.glob('models--facebook--nllb-200-distilled-600M')) else 'Not downloaded yet')"
```

### Check cache size:
```bash
# Windows PowerShell
Get-ChildItem "$env:USERPROFILE\.cache\huggingface\hub" -Recurse | Measure-Object -Property Length -Sum
```

If you see ~2.5GB, the model is downloaded!

## After Download

Once downloaded, you can:

1. **Start multilingual watcher:**
   ```bash
   python vibe_watcher_multilingual.py
   ```

2. **Test translation:**
   ```bash
   python test_translation.py
   ```

3. **Use offline forever!**
   - No more downloads needed
   - Works without internet
   - Translate unlimited text for free

## Troubleshooting

### "Read timed out" error
- **Normal!** Your internet is slow
- Run the command again - it will resume
- Or use `download_nllb_model.py` for automatic retries

### "Disk space" error
- Need ~3GB free space
- Clear some files and try again

### "Permission denied" error
- Run as administrator (Windows)
- Or change cache directory

### Download stuck at 0%
- Wait 5-10 minutes - it might be connecting
- Check your internet connection
- Try again later

## Alternative: Smaller Model

If 2.5GB is too large, you can use a smaller model (lower quality):

Edit `translator.py`, line 54:
```python
# Instead of:
model_name = "facebook/nllb-200-distilled-600M"  # 2.5GB

# Use:
model_name = "Helsinki-NLP/opus-mt-mul-en"  # ~300MB (lower quality)
```

**Trade-off:** Smaller download but less accurate translation

## Summary

**Best option for slow internet:**
```bash
python download_nllb_model.py
```

**Best option for no internet:**
- Download from better location
- Or use Google Translate API

**After download:**
- Works offline forever
- Free unlimited translations
- Supports 6 languages

---

**Need help?** See `MULTILINGUAL_GUIDE.md` for complete documentation.
