# Vibe-MediScribe Setup Checklist

Use this checklist to ensure everything is configured correctly.

## ☐ Prerequisites

- [ ] Python 3.7 or higher installed
- [ ] Vibe application installed ([Download here](https://thewh1teagle.github.io/vibe/))
- [ ] Basic familiarity with command line/terminal

## ☐ Step 1: Install MediScribe Dependencies

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

**Verify:**
- [ ] No error messages during installation
- [ ] spaCy model downloaded successfully

**Test:**
```bash
python verify_setup.py
```

## ☐ Step 2: Configure Vibe

Open Vibe application:

- [ ] Launch Vibe
- [ ] Go to Settings (gear icon)
- [ ] Find "Default Save Location" or "Export Directory"
- [ ] Set to a dedicated folder (e.g., `C:\Users\YourName\Documents\Vibe Transcripts`)
- [ ] Note down the exact path (you'll need it for Step 3)
- [ ] Choose export format: TXT (recommended) or JSON/SRT/VTT
- [ ] Save settings

**Your Vibe save path:**
```
_____________________________________________________________
```

## ☐ Step 3: Configure MediScribe

Edit `vibe_config.json`:

- [ ] Open `vibe_config.json` in a text editor
- [ ] Update `watch_directory` to match your Vibe save path
- [ ] Use double backslashes on Windows: `C:\\Users\\...`
- [ ] Verify `file_extensions` includes your chosen format
- [ ] Set `auto_process` to `true`
- [ ] Save the file

**Example:**
```json
{
  "watch_directory": "C:\\Users\\YourName\\Documents\\Vibe Transcripts",
  "file_extensions": [".txt", ".srt", ".vtt", ".json"],
  "auto_process": true
}
```

## ☐ Step 4: Test the Setup

Run verification:
```bash
python verify_setup.py
```

- [ ] All checks pass (green checkmarks)
- [ ] Watch directory exists
- [ ] Dependencies installed
- [ ] Core files present

## ☐ Step 5: Start the Integration Service

**Option A: Windows Batch File**
```bash
start_vibe_integration.bat
```

**Option B: Python Command**
```bash
python vibe_watcher.py
```

**Verify:**
- [ ] Console shows "Vibe-MediScribe Integration Active"
- [ ] Watch directory is correct
- [ ] No error messages
- [ ] Shows "Monitoring for new transcripts..."

## ☐ Step 6: Test with Sample Transcript

Create a test file:
```bash
python test_vibe_integration.py
```

**Verify:**
- [ ] Test file created in watch directory
- [ ] vibe_watcher.py console shows detection
- [ ] Extraction completes successfully
- [ ] Record saved to database
- [ ] `*_mediscribe.json` file created

## ☐ Step 7: View Test Results

```bash
python view_database.py
```

**Verify:**
- [ ] Test record appears in database
- [ ] Patient information extracted correctly
- [ ] Diagnosis and medications present
- [ ] Timestamp is correct

## ☐ Step 8: Test with Real Vibe Transcript

1. Open Vibe
2. Record or import a short audio clip
3. Transcribe it
4. Review the transcript
5. Save to your configured directory

**Verify:**
- [ ] File appears in watch directory
- [ ] vibe_watcher.py detects it
- [ ] Processing completes
- [ ] Record saved to database
- [ ] Can view record with `python view_database.py`

## ☐ Step 9: Configure for Daily Use

**For continuous use:**

- [ ] Keep vibe_watcher.py running in a terminal window
- [ ] Or set up as a startup script (see VIBE_INTEGRATION.md)
- [ ] Or run as a Windows service (advanced)

**Recommended:**
- [ ] Pin terminal window to taskbar
- [ ] Minimize (don't close) the terminal
- [ ] Check console occasionally for any errors

## ☐ Step 10: Learn the Commands

Practice these commands:

**View all records:**
```bash
python view_database.py
```
- [ ] Tested and working

**Search by patient:**
```bash
python mediscribe.py --search "Patient Name"
```
- [ ] Tested and working

**Manual processing (if needed):**
```bash
python batch_process.py transcript.txt
```
- [ ] Tested and working

## ☐ Optional: Advanced Configuration

**Customize extraction patterns:**
- [ ] Review `medical_extractor_simple.py`
- [ ] Add custom medical terms if needed
- [ ] Test with sample transcripts

**Database backup:**
- [ ] Set up automatic backup of `medical_records.json`
- [ ] Consider cloud sync (Dropbox, OneDrive, etc.)
- [ ] Test restore procedure

**Security:**
- [ ] Restrict folder permissions
- [ ] Consider encrypting database
- [ ] Review privacy policy

## ☐ Troubleshooting Checklist

If something doesn't work:

- [ ] Run `python verify_setup.py` again
- [ ] Check paths match in Vibe and `vibe_config.json`
- [ ] Ensure vibe_watcher.py is running
- [ ] Check console for error messages
- [ ] Verify file extensions match
- [ ] Test with `python test_vibe_integration.py`
- [ ] Review VIBE_INTEGRATION.md for detailed help

## ☐ Documentation Review

Familiarize yourself with:

- [ ] `VIBE_QUICK_SETUP.md` - Quick reference
- [ ] `VIBE_INTEGRATION.md` - Complete guide
- [ ] `INTEGRATION_SUMMARY.md` - Overview
- [ ] `WORKFLOW_DIAGRAM.txt` - Visual workflow
- [ ] `README.md` - Project overview

## ☐ Final Verification

Everything working:

- [ ] Vibe transcribes audio correctly
- [ ] Transcripts save to configured directory
- [ ] vibe_watcher.py detects new files
- [ ] Medical information extracted accurately
- [ ] Records saved to database
- [ ] Can search and view records
- [ ] No error messages in console

## 🎉 Setup Complete!

If all items are checked, you're ready to use Vibe-MediScribe integration!

### Your Workflow:
1. Record/import audio in Vibe
2. Review transcript in Vibe's editor
3. Save transcript
4. MediScribe processes automatically
5. View records anytime with `python view_database.py`

### Need Help?

- Console shows errors → Check VIBE_INTEGRATION.md troubleshooting section
- Files not detected → Verify paths in `vibe_config.json`
- Extraction issues → Test with `python medical_extractor_simple.py`
- General questions → Review documentation files

---

**Happy transcribing! 🎙️ + 🏥 = ✨**

Date completed: _______________

Notes:
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
