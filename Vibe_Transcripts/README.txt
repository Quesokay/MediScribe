VIBE TRANSCRIPTS FOLDER
=======================

This folder is monitored by MediScribe.

HOW IT WORKS:
1. Save Vibe transcripts here (or configure Vibe to save here automatically)
2. MediScribe detects new files automatically
3. Extracts medical information
4. Saves to database
5. Creates *_mediscribe.json file with extracted data

SUPPORTED FILE TYPES:
- .txt (recommended)
- .srt
- .vtt
- .json

CONFIGURE VIBE:
Open Vibe → Settings → Set save directory to:
C:\Clone_wars\MediScribe\Vibe_Transcripts

WHAT HAPPENS:
When you save "patient_visit.txt" here, MediScribe will:
- Detect the new file
- Extract patient information
- Save to medical_records.json database
- Create patient_visit_mediscribe.json with extracted data

FILES YOU'LL SEE:
- patient_visit.txt (your original transcript)
- patient_visit_mediscribe.json (extracted medical data)

For multilingual:
- patient_visit.txt (original in Shona/Ndebele)
- patient_visit_english.txt (translated to English)
- patient_visit_mediscribe.json (extracted from English)

IMPORTANT:
- Don't delete files while watcher is running
- Don't manually edit *_mediscribe.json files
- Keep original transcripts for reference

NEED HELP?
See: READY_TO_USE.md in the main folder
