# 🚀 Start Here - MediScribe MCP Integration

## What This Does

**ChatGPT automatically processes your medical conversations!**

1. You talk in ChatGPT voice mode
2. You say "process this conversation"
3. ChatGPT sends it to MediScribe
4. MediScribe translates (if needed) and extracts medical data
5. ChatGPT shows you the structured results
6. Everything saved to database

**No copy/paste. No manual work. Just talk and ask ChatGPT to process.**

---

## Quick Setup (5 Minutes)

### Step 1: Install

```bash
setup_chatgpt_mode.bat
```

### Step 2: Start MCP Server

```bash
python mcp_server.py
```

Keep this running!

### Step 3: Configure ChatGPT

1. Open `mcp_config.json`
2. Change this line:

   ```json
   "args": ["C:/full/path/to/your/mcp_server.py"]
   ```

   To your actual path, like:

   ```json
   "args": ["C:/Users/YourName/Documents/mediscribe/mcp_server.py"]
   ```

3. Copy the whole `mcp_config.json` content
4. In ChatGPT: Settings → MCP → Add Server → Paste
5. Save

### Step 4: Test

In ChatGPT, type:

```
"I'm going to give you a medical conversation to process.

Doctor: Good morning! What's your name?
Patient: I'm John Doe, 45 years old, male.
Doctor: What brings you in today?
Patient: I have a fever and headache for 3 days.
Doctor: Let me check. Temperature is 101.5F.
Doctor: I'll prescribe Ibuprofen 400mg three times daily.

Please process this conversation."
```

ChatGPT will automatically:

- Call the MediScribe tool
- Extract the medical data
- Show you the results

✅ **If this works, you're done!**

---

## How to Use

### With Voice Mode

1. Enable voice in ChatGPT
2. Have your medical conversation
3. Say: "Process this conversation"
4. Done!

### With Text

1. Type or paste a conversation
2. Say: "Process this medical conversation"
3. Done!

### Multilingual

Works with:

- English
- Shona
- Ndebele
- Zulu
- Xhosa
- Afrikaans

Just say: "Process this Shona conversation" (or any language)

---

## What You Get

### Input

```
Doctor: Hi, what's your name?
Patient: I'm Sarah, 28. I have a headache and fever.
Doctor: Temperature is 101.5F. I'll prescribe Ibuprofen 400mg.
```

### Output (from ChatGPT)

```
Patient: Sarah, 28 years old
Symptoms: headache, fever
Vital Signs: temperature 101.5F
Medications: Ibuprofen 400mg

Saved to database as: REC-20251024103000
```

---

## Troubleshooting

### ChatGPT doesn't see the tools

1. Make sure MCP server is running
2. Check the path in `mcp_config.json` is correct
3. Restart ChatGPT

### Server won't start

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### Translation not working

```bash
pip install transformers torch
```

First run downloads ~2.5GB (one-time, be patient)

---

## Next Steps

- **[MCP_SETUP_GUIDE.md](MCP_SETUP_GUIDE.md)** - Detailed setup
- **[CHATGPT_MCP_WORKFLOW.md](CHATGPT_MCP_WORKFLOW.md)** - Complete workflow guide
- **[USAGE_GUIDE.md](USAGE_GUIDE.md)** - All features

---

## That's It!

Keep the MCP server running, talk in ChatGPT, and ask it to process your conversations. Everything else is automatic!

🎉 **Happy processing!**
