# Vibe-MediScribe Quick Setup (5 Minutes)

## Step 1: Install Dependencies (1 min)

```bash
pip install watchdog
```

## Step 2: Configure Vibe (2 min)

1. Open **Vibe** application
2. Go to **Settings** (gear icon)
3. Find **"Default Save Location"** or **"Export Directory"**
4. Set it to: `C:\Users\YourName\Documents\Vibe Transcripts`
   - Or any folder you prefer
5. Choose export format: **TXT** (recommended) or JSON/SRT/VTT

## Step 3: Configure MediScribe (1 min)

Edit `vibe_config.json` and update the watch directory:

```json
{
  "watch_directory": "C:\\Users\\YourName\\Documents\\Vibe Transcripts"
}
```

**Important:** Use double backslashes `\\` on Windows!

## Step 4: Start Integration (30 seconds)

**Windows:**
```bash
start_vibe_integration.bat
```

**Or manually:**
```bash
python vibe_watcher.py
```

You should see:
```
✓ Vibe-MediScribe Integration Active
✓ Watching: C:\Users\YourName\Documents\Vibe Transcripts
👀 Monitoring for new transcripts...
```

## Step 5: Test It! (30 seconds)

**Option A: Create test file**
```bash
python test_vibe_integration.py
```

**Option B: Use Vibe**
1. Record or import audio in Vibe
2. Transcribe it
3. Save to your configured directory
4. Watch MediScribe process it automatically!

## That's It! 🎉

Now whenever you save a transcript in Vibe, MediScribe will:
- ✅ Automatically detect the new file
- ✅ Extract patient information
- ✅ Save to database
- ✅ Create a `*_mediscribe.json` file

## View Your Records

```bash
python view_database.py
```

## Troubleshooting

**Not detecting files?**
- Make sure the paths match in Vibe settings and `vibe_config.json`
- Use absolute paths with double backslashes: `C:\\Users\\...`

**Need help?**
- See full guide: `VIBE_INTEGRATION.md`
- Test extraction: `python medical_extractor_simple.py`

---

**Pro Tip:** Keep the watcher running in a minimized terminal window. It uses minimal resources and processes files instantly!
