# MediScribe MCP Usage Examples

Real-world examples of how AI assistants can use MediScribe via MCP.

## Example 1: Doctor's Workflow Assistant

**Scenario:** Doctor uses Claude Desktop to process patient notes

### Conversation:

**Doctor:** "I just saw a patient. Here are my notes: Patient Maria Garcia, 38 year old female, complains of severe headache for 3 days, sensitivity to light, nausea. Temperature 99.2F. Diagnosed with migraine. Prescribed Sumatriptan 50mg as needed."

**Claude (using MediScribe MCP):**
```
I'll extract and save this medical information for you.

[Calls: extract_medical_data with save_to_db=true]

✓ Medical record created successfully!

Record ID: REC-20251018143022

Extracted Information:
- Patient: Maria Garcia
- Age: 38
- Gender: Female
- Symptoms: Severe headache, sensitivity to light, nausea
- Vital Signs: 99.2F
- Diagnosis: Migraine
- Medications: Sumatriptan 50mg as needed

The record has been saved to your database.
```

---

## Example 2: Multilingual Clinic

**Scenario:** Patient speaks Shona, AI assistant translates and processes

### Conversation:

**Nurse:** "Process this patient interview: Murwere Sarah Moyo, makore 32, mukadzi. Ndine fivha uye ndiri kunzwa kurwara musoro. Tembiricha 38.5 degrees. Chiremba akapa mushonga Paracetamol 500mg."

**AI Assistant (using MediScribe MCP):**
```
I'll translate from Shona and extract the medical information.

[Calls: translate_and_extract with save_to_db=true]

✓ Translation and extraction complete!

Original Language: Shona

Translated Text:
"Patient Sarah Moyo, 32 years, female. I have fever and I am feeling pain head. 
Temperature 38.5 degrees. Doctor gave medicine Paracetamol 500mg."

Extracted Information:
- Patient: Sarah Moyo
- Age: 32
- Gender: Female
- Symptoms: Fever, headache
- Vital Signs: 38.5 degrees
- Medications: Paracetamol 500mg

Record ID: REC-20251018143145
```

---

## Example 3: Patient History Lookup

**Scenario:** Doctor needs to review previous visits

### Conversation:

**Doctor:** "Show me all records for John Doe"

**AI Assistant (using MediScribe MCP):**
```
[Calls: search_patient_records with patient_name="John Doe"]

Found 3 records for John Doe:

1. Record REC-20251015120000 (Oct 15, 2025)
   - Diagnosis: Pneumonia
   - Medications: Amoxicillin 500mg
   - Status: Follow-up scheduled

2. Record REC-20251001093000 (Oct 1, 2025)
   - Diagnosis: Annual checkup
   - Vital Signs: BP 120/80, Normal
   - Status: Healthy

3. Record REC-20250920140000 (Sep 20, 2025)
   - Diagnosis: Seasonal allergies
   - Medications: Loratadine 10mg
   - Status: Resolved

Would you like details on any specific visit?
```

---

## Example 4: Batch Processing

**Scenario:** Process multiple transcription files at once

### Conversation:

**Admin:** "Process all transcription files in the Vibe_Transcripts folder"

**AI Assistant (using MediScribe MCP):**
```
I'll process each transcription file.

[Calls: process_file for each .txt file with save_to_db=true]

Processing results:

✓ patient_001.txt → REC-20251018144001
  Patient: James Wilson, Diagnosis: Hypertension

✓ patient_002.txt → REC-20251018144002
  Patient: Lisa Chen, Diagnosis: Type 2 Diabetes

✓ patient_003.txt → REC-20251018144003
  Patient: Ahmed Hassan, Diagnosis: Asthma

✓ patient_004.txt → REC-20251018144004
  Patient: Emma Brown, Diagnosis: Anxiety

Processed 4 files successfully.
All records saved to database.
```

---

## Example 5: Data Analysis

**Scenario:** Generate insights from medical records

### Conversation:

**Doctor:** "What are the most common diagnoses this month?"

**AI Assistant (using MediScribe MCP):**
```
[Calls: get_all_records with limit=100]

Analyzing 47 records from October 2025...

Most Common Diagnoses:
1. Upper Respiratory Infection - 12 cases (25.5%)
2. Hypertension - 8 cases (17.0%)
3. Type 2 Diabetes - 6 cases (12.8%)
4. Migraine - 5 cases (10.6%)
5. Seasonal Allergies - 4 cases (8.5%)

Most Prescribed Medications:
1. Amoxicillin - 15 prescriptions
2. Lisinopril - 8 prescriptions
3. Metformin - 6 prescriptions
4. Sumatriptan - 5 prescriptions

Average Patient Age: 42.3 years
Gender Distribution: 55% Female, 45% Male
```

---

## Example 6: Quality Assurance

**Scenario:** Review incomplete records

### Conversation:

**Admin:** "Check for any records missing vital information"

**AI Assistant (using MediScribe MCP):**
```
[Calls: get_all_records]

Reviewing 47 records for completeness...

⚠️ Found 3 records with missing information:

1. REC-20251018120000 - Patient: Unknown
   Missing: Patient name, age, gender
   Has: Symptoms (fever, cough), Diagnosis (Flu)

2. REC-20251017150000 - Patient: John Smith
   Missing: Diagnosis
   Has: Symptoms, vital signs, patient info

3. REC-20251016093000 - Patient: Mary Johnson
   Missing: Medications
   Has: Diagnosis (Hypertension), patient info

Recommendation: Review original transcriptions for these records.
```

---

## Example 7: Integration with EHR

**Scenario:** Export data for external system

### Conversation:

**IT Admin:** "Export all records for patient ID 12345 in JSON format"

**AI Assistant (using MediScribe MCP):**
```
[Calls: search_patient_records, then formats for export]

Exporting records for Patient ID 12345 (Sarah Johnson)...

{
  "patient_id": "12345",
  "patient_name": "Sarah Johnson",
  "records": [
    {
      "record_id": "REC-20251018120000",
      "date": "2025-10-18",
      "diagnosis": ["Migraine"],
      "medications": ["Sumatriptan 50mg"],
      "vital_signs": ["BP 120/80", "Temp 98.6F"],
      "follow_up": "2 weeks"
    }
  ],
  "export_date": "2025-10-18T14:45:00Z",
  "format_version": "1.0"
}

✓ Export complete. Ready for EHR import.
```

---

## Example 8: Voice-to-Database Pipeline

**Scenario:** Complete workflow from speech to database

### Conversation:

**Doctor:** "I just finished recording a patient consultation in Vibe. The file is saved as consultation_2025_10_18.txt. Process it and let me know what was extracted."

**AI Assistant (using MediScribe MCP):**
```
[Calls: process_file with save_to_db=true]

✓ Processed consultation_2025_10_18.txt

Extracted Medical Record:

Patient Information:
- Name: Robert Taylor
- Age: 56
- Gender: Male

Chief Complaint:
- Chest pain (3 days)
- Shortness of breath
- Fatigue

Vital Signs:
- BP: 145/92 (elevated)
- Heart Rate: 88 bpm
- Temperature: 98.4F

Diagnosis:
- Suspected angina
- Hypertension

Treatment Plan:
- Ordered EKG and cardiac enzymes
- Prescribed Nitroglycerin sublingual PRN
- Prescribed Lisinopril 10mg daily
- Referred to cardiology

Follow-up:
- Return in 3 days with test results
- Emergency instructions provided

Record ID: REC-20251018145500

⚠️ Note: Elevated blood pressure and cardiac symptoms detected.
Consider priority follow-up.
```

---

## Example 9: Research Query

**Scenario:** Researcher analyzing treatment patterns

### Conversation:

**Researcher:** "How many patients with diabetes were prescribed Metformin in the last 30 days?"

**AI Assistant (using MediScribe MCP):**
```
[Calls: get_all_records, then filters and analyzes]

Analyzing diabetes treatment patterns...

Results for last 30 days:

Total Diabetes Diagnoses: 14 patients

Metformin Prescriptions: 11 patients (78.6%)
- Average dosage: 850mg
- Frequency: Twice daily (most common)

Alternative Treatments: 3 patients (21.4%)
- Insulin therapy: 2 patients
- Lifestyle modification only: 1 patient

Patient Demographics:
- Average age: 58.2 years
- Gender: 57% Male, 43% Female

Comorbidities:
- Hypertension: 9 patients (64.3%)
- Obesity: 7 patients (50.0%)
- Hyperlipidemia: 5 patients (35.7%)
```

---

## Example 10: Emergency Triage

**Scenario:** Quick assessment of urgent cases

### Conversation:

**Triage Nurse:** "Process this emergency case: Patient collapsed, 68 year old male, chest pain radiating to left arm, sweating, BP 160/100, heart rate 110."

**AI Assistant (using MediScribe MCP):**
```
[Calls: extract_medical_data with save_to_db=true]

🚨 URGENT CASE DETECTED

Extracted Information:
- Age: 68
- Gender: Male
- Symptoms: 
  • Chest pain (radiating to left arm)
  • Sweating
  • Collapsed
- Vital Signs:
  • BP: 160/100 (CRITICAL - Hypertensive)
  • Heart Rate: 110 bpm (Tachycardia)

⚠️ ALERT: Symptoms consistent with acute myocardial infarction (heart attack)

Recommended Actions:
1. Activate cardiac emergency protocol
2. Administer aspirin 325mg (if not contraindicated)
3. Obtain 12-lead EKG immediately
4. Prepare for possible cardiac catheterization
5. Contact cardiology on-call

Record ID: REC-20251018150000
Priority: CRITICAL

Time is critical for cardiac events. Immediate intervention required.
```

---

## Integration Patterns

### Pattern 1: Real-time Processing
```
Doctor speaks → Vibe transcribes → AI assistant monitors folder
→ MCP auto-processes → Database updated → Doctor notified
```

### Pattern 2: Interactive Review
```
Doctor reviews transcript → Asks AI to extract → AI uses MCP
→ Shows extracted data → Doctor confirms → Saves to database
```

### Pattern 3: Batch Analysis
```
End of day → AI assistant processes all new files → Generates summary
→ Flags incomplete records → Sends report to doctor
```

### Pattern 4: Multi-language Clinic
```
Patient speaks native language → Vibe transcribes → AI detects language
→ MCP translates and extracts → English record saved → Original preserved
```

---

## Best Practices

1. **Always verify critical information** - AI extraction is helpful but should be reviewed for medical decisions

2. **Use save_to_db=false for testing** - Test extraction before committing to database

3. **Preserve original transcriptions** - Keep raw audio/text for legal compliance

4. **Regular backups** - Export database regularly for disaster recovery

5. **Privacy compliance** - Ensure MCP server runs locally, no cloud transmission

6. **Audit trail** - Record IDs include timestamps for tracking

7. **Error handling** - Review records flagged with missing information

---

## Next Steps

Ready to use MediScribe MCP? 

1. Install: `install_mcp.bat`
2. Configure: See `MCP_SETUP.md`
3. Test: `python test_mcp_client.py`
4. Integrate: Configure your AI assistant
5. Use: Start processing medical transcriptions!

---

**MediScribe MCP** - Making medical documentation effortless through AI integration
