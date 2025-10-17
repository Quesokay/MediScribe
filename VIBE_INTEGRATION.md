# Vibe-MediScribe Integration Guide

## Overview

This integration allows MediScribe to automatically process transcripts created by Vibe, extracting medical information in the background while you verify the transcription quality in Vibe's editor.

## How It Works

```
┌─────────────────────────────────────────────────────────────┐
│  1. Doctor records audio in Vibe                            │
│  2. Vibe transcribes the audio                              │
│  3. Doctor reviews transcript in Vibe's editor              │
│  4. Doctor clicks "Save Transcript" in Vibe                 │
│     └─> Saves to configured directory                       │
│                                                              │
│  5. MediScribe Watcher detects new file (background)        │
│  6. Extracts patient details automatically                  │
│  7. Saves to medical_records.json database                  │
│  8. Creates *_mediscribe.json with extracted data           │
└─────────────────────────────────────────────────────────────┘
```

## Setup Instructions

### Step 1: Install Dependencies

```bash
pip install watchdog
```

The watchdog library enables file system monitoring.

### Step 2: Configure Vibe Save Location

1. Open Vibe application
2. Go to Settings
3. Set the default save directory for transcripts to a dedicated folder
   - Example: `C:\Users\YourName\Documents\Vibe Transcripts`
4. Choose your preferred export format (TXT, SRT, VTT, or JSON)

### Step 3: Configure MediScribe Watcher

Edit `vibe_config.json`:

```json
{
  "watch_directory": "C:\\Users\\YourName\\Documents\\Vibe Transcripts",
  "file_extensions": [".txt", ".srt", ".vtt", ".json"],
  "auto_process": true,
  "process_on_modify": false,
  "save_extracted_json": true,
  "notification_sound": true,
  "database_path": "medical_records.json"
}
```

**Configuration Options:**

- `watch_directory`: Folder where Vibe saves transcripts (must match Vibe settings)
- `file_extensions`: File types to monitor
- `auto_process`: Automatically process new files (recommended: true)
- `process_on_modify`: Also process when files are modified (recommended: false)
- `save_extracted_json`: Save extracted data as separate JSON files
- `notification_sound`: Play sound when processing completes (Windows only)
- `database_path`: Database file for medical records

### Step 4: Start the Integration Service

Open a terminal and run:

```bash
python vibe_watcher.py
```

You should see:

```
======================================================================
  🎙️  VIBE-MEDISCRIBE INTEGRATION SERVICE
======================================================================
  Automatically processes Vibe transcripts with MediScribe
  Press Ctrl+C to stop

✓ Vibe-MediScribe Integration Active
✓ Watching: C:\Users\YourName\Documents\Vibe Transcripts
✓ File types: .txt, .srt, .vtt, .json
✓ Auto-process: ON

👀 Monitoring for new transcripts...
💡 Tip: Configure Vibe to save transcripts to the watch directory
```

### Step 5: Use the Integration

1. **Record/Import Audio in Vibe**
   - Use Vibe's microphone recording feature, or
   - Import an audio/video file

2. **Transcribe**
   - Let Vibe transcribe the audio
   - Review the transcript in Vibe's editor
   - Make any necessary corrections

3. **Save**
   - Click "Save Transcript" in Vibe
   - Choose your configured directory
   - Save as TXT, SRT, VTT, or JSON

4. **Automatic Processing**
   - MediScribe watcher detects the new file
   - Extracts medical information automatically
   - Saves to database
   - Creates `*_mediscribe.json` with extracted data

5. **View Results**
   ```bash
   python view_database.py
   ```

## Workflow Example

### In Vibe:
```
1. Record: "Patient John Doe, 45 year old male, presents with fever..."
2. Transcribe: Review the text output
3. Save: patient_visit_2024.txt → Vibe Transcripts folder
```

### MediScribe (Automatic):
```
======================================================================
📄 New transcript detected: patient_visit_2024.txt
⏰ Time: 2024-05-15 14:30:22
======================================================================

🔍 Extracting medical information...

✓ Extraction complete!
  👤 Patient: John Doe
  📅 Age: 45
  ⚧ Gender: male
  🏥 Diagnosis: Pneumonia
  💊 Medications: Amoxicillin

💾 Saving to database...
✓ Record saved with ID: REC-20240515143025
✓ Saved extracted data: patient_visit_2024_mediscribe.json

✅ Successfully processed and saved as REC-20240515143025
======================================================================
```

## Running as Background Service

### Option 1: Keep Terminal Open
Simply run `python vibe_watcher.py` and minimize the terminal window.

### Option 2: Windows Service (Advanced)
Use NSSM (Non-Sucking Service Manager) to run as a Windows service:

```bash
# Download NSSM from https://nssm.cc/download
nssm install MediScribeWatcher "C:\Python\python.exe" "C:\path\to\vibe_watcher.py"
nssm start MediScribeWatcher
```

### Option 3: Startup Script
Create a batch file `start_mediscribe_watcher.bat`:

```batch
@echo off
cd /d "C:\path\to\mediscribe"
python vibe_watcher.py
pause
```

Add this to Windows Startup folder:
- Press `Win+R`
- Type `shell:startup`
- Copy the batch file there

## Viewing Records

### View All Records
```bash
python view_database.py
```

### Search by Patient
```bash
python mediscribe.py --search "John Doe"
```

### View Specific Record
Open `medical_records.json` or the individual `*_mediscribe.json` files.

## File Structure

After processing, you'll have:

```
Vibe Transcripts/
├── patient_visit_2024.txt              # Original Vibe transcript
└── patient_visit_2024_mediscribe.json  # Extracted medical data

MediScribe/
├── medical_records.json                # Database with all records
├── processed_files.json                # Tracking processed files
└── vibe_watcher.py                     # Running in background
```

## Troubleshooting

### Watcher Not Detecting Files

1. **Check directory path**
   - Ensure `watch_directory` in `vibe_config.json` matches Vibe's save location
   - Use absolute paths with double backslashes on Windows

2. **Check file extensions**
   - Verify Vibe is saving in a supported format (.txt, .srt, .vtt, .json)

3. **Check permissions**
   - Ensure MediScribe has read access to the watch directory

### Files Processed Multiple Times

- The watcher maintains a `processed_files.json` log
- Delete this file to reprocess all files
- Set `process_on_modify: false` to avoid reprocessing on edits

### Missing Extracted Data

- Check that the transcript contains medical information
- Review the original transcript for proper formatting
- Patient names should be clearly stated
- Use keywords like "diagnosis:", "prescribed:", "symptoms:"

## Advanced Usage

### Custom Processing Logic

Edit `vibe_watcher.py` to customize the `process_transcript` method:

```python
def process_transcript(self, file_path: Path):
    # Add custom logic here
    # Example: Send notification, update EHR, etc.
    pass
```

### Integration with EHR Systems

Modify `database_saver.py` to save to your EHR database instead of JSON:

```python
def add_record(self, extracted_data: Dict) -> str:
    # Replace with your EHR API calls
    # Example: ehr_api.create_patient_record(extracted_data)
    pass
```

## Security Considerations

- **HIPAA Compliance**: All processing happens locally, no data leaves your machine
- **File Permissions**: Restrict access to the watch directory and database files
- **Encryption**: Consider encrypting `medical_records.json` at rest
- **Audit Logs**: The watcher logs all processing activities with timestamps

## Tips for Best Results

1. **Speak Clearly**: Better transcription = better extraction
2. **Use Keywords**: Say "diagnosis:", "prescribed:", "patient name is..."
3. **Review in Vibe**: Always verify transcription before saving
4. **Consistent Format**: Use similar phrasing for patient visits
5. **Test First**: Process sample transcripts to verify extraction quality

## Stopping the Service

Press `Ctrl+C` in the terminal running `vibe_watcher.py`:

```
🛑 Stopping Vibe-MediScribe Integration...
✓ Service stopped
```

## Support

For issues or questions:
1. Check the console output for error messages
2. Review `vibe_config.json` settings
3. Test with `sample_transcription.txt`
4. Verify Vibe is saving to the correct directory

---

**Happy transcribing! 🎙️ + 🏥 = ✨**
