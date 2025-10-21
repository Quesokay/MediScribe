# MediScribe MCP Quick Reference

## Available Tools

### 1. extract_medical_data
Extract structured medical info from text.

**Usage:**
```
Extract medical data from: "Patient John Doe, 45 year old male, fever 101.5F"
```

### 2. translate_and_extract
Translate and extract from non-English text.

**Usage:**
```
Translate and extract: "Murwere John, makore 45, ndine fivha"
```

### 3. search_patient_records
Find records by patient name.

**Usage:**
```
Search for patient records: "John Doe"
```

### 4. get_patient_record
Get specific record by ID.

**Usage:**
```
Get record: REC-20251018120000
```

### 5. get_all_records
List all medical records.

**Usage:**
```
Show all medical records (limit 10)
```

### 6. save_to_database
Save extracted data to database.

**Usage:**
```
Save this extracted data to database: {...}
```

### 7. process_file
Process a transcription file.

**Usage:**
```
Process file: sample_transcription.txt
```

## Quick Commands

**Extract and save:**
```
Extract and save to database: "Patient Sarah Lee, 32 female, headache..."
```

**Multilingual:**
```
Process this Shona transcription: "Murwere..."
```

**Search:**
```
Find all records for John Doe
```

**View database:**
```
Show me the last 5 medical records
```

## Status

✅ MCP module installed  
✅ MediScribe modules loaded  
✅ Server configured in `.kiro/settings/mcp.json`  
✅ Ready to use!

## Test It

Try asking:
- "Extract medical data from: Patient John Doe, 45 year old male, fever and cough"
- "Search for patient records: John Doe"
- "Show all medical records"
