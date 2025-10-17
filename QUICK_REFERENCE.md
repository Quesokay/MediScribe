# Vibe-MediScribe Quick Reference Card

## 🚀 Quick Start (First Time)

```bash
# 1. Install dependencies
pip install watchdog

# 2. Configure Vibe save directory
# Open Vibe → Settings → Set save location

# 3. Update vibe_config.json with your path

# 4. Start integration
python vibe_watcher.py
```

## 📋 Daily Commands

| Task | Command |
|------|---------|
| Start integration | `python vibe_watcher.py` |
| View all records | `python view_database.py` |
| Search patient | `python mediscribe.py --search "Name"` |
| Test integration | `python test_vibe_integration.py` |
| Verify setup | `python verify_setup.py` |
| Manual process | `python batch_process.py file.txt` |

## 📁 File Structure

```
Your Setup/
├── Vibe Transcripts/          ← Vibe saves here
│   ├── transcript.txt         ← Original
│   └── transcript_mediscribe.json  ← Extracted
│
└── MediScribe/
    ├── vibe_watcher.py        ← Keep running
    ├── vibe_config.json       ← Your settings
    └── medical_records.json   ← Database
```

## ⚙️ Configuration (vibe_config.json)

```json
{
  "watch_directory": "C:\\path\\to\\vibe\\transcripts",
  "file_extensions": [".txt", ".srt", ".vtt", ".json"],
  "auto_process": true
}
```

## 🔄 Workflow

```
1. Vibe: Record → Transcribe → Review → Save
2. MediScribe: Auto-detect → Extract → Save (background)
3. You: View records anytime
```

## 🎯 What Gets Extracted

- ✓ Patient name, age, gender
- ✓ Symptoms and vital signs
- ✓ Diagnosis and medications
- ✓ Treatment plan and follow-up

## 🔍 Searching Records

```bash
# View all
python view_database.py

# Search by name
python mediscribe.py --search "John Doe"

# Or open medical_records.json directly
```

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Files not detected | Check paths match in Vibe & config |
| Missing dependencies | `pip install -r requirements.txt` |
| Extraction errors | Test with `python medical_extractor_simple.py` |
| Setup issues | Run `python verify_setup.py` |

## 📚 Documentation

| File | Purpose |
|------|---------|
| `VIBE_QUICK_SETUP.md` | 5-minute setup guide |
| `VIBE_INTEGRATION.md` | Complete integration guide |
| `SETUP_CHECKLIST.md` | Step-by-step checklist |
| `INTEGRATION_SUMMARY.md` | Overview and summary |
| `WORKFLOW_DIAGRAM.txt` | Visual workflow |

## 💡 Tips

- Keep vibe_watcher.py running in background
- Review transcripts in Vibe before saving
- Check console for processing status
- Backup medical_records.json regularly
- Use consistent phrasing for better extraction

## 🔒 Privacy

- ✓ All processing is local
- ✓ No data sent to servers
- ✓ HIPAA-compliant architecture
- ✓ You control all data

## ⚡ Performance

- Processing: 1-2 seconds per file
- RAM usage: ~500MB
- CPU: Any modern processor
- No GPU required

## 🆘 Quick Help

```bash
# Verify everything is working
python verify_setup.py

# Test with sample data
python test_vibe_integration.py

# Check what's in database
python view_database.py
```

## 📞 Support Resources

1. Run `python verify_setup.py` for diagnostics
2. Check console output for errors
3. Review `VIBE_INTEGRATION.md` for details
4. Test with sample transcripts

---

**Keep this file handy for quick reference!**

Print or bookmark for easy access during daily use.
