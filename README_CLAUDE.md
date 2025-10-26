# MediScribe for Claude Desktop

## 🚀 Quick Start (3 Steps)

### Step 1: Install
```bash
INSTALL_FOR_CLAUDE.bat
```

### Step 2: Configure Claude
1. Open: `%APPDATA%\Claude\claude_desktop_config.json`
2. Copy content from `claude_desktop_config.json` in this folder
3. Paste and save
4. Restart Claude Desktop

### Step 3: Start Server
```bash
python mcp_server.py
```

Keep this running!

---

## ✅ Verify It Works

In Claude Desktop:
1. Look for 🔧 tools icon
2. Should see 7 MediScribe tools
3. Try this:

```
Process this medical conversation:

Doctor: Hi, what's your name?
Patient: I'm John Doe, 45 years old.
Doctor: What brings you in?
Patient: I have a fever and headache.
Doctor: Temperature is 101.5F. I'll prescribe Ibuprofen 400mg.
```

Claude will automatically process it and show structured data!

---

## 💬 Daily Usage

Just talk to Claude normally:

```
"Process this medical conversation"
"Search for patient John Doe"
"Show me recent records"
"Process this Shona conversation: [paste]"
```

Claude handles everything automatically via MCP!

---

## 🌍 Multilingual Support

Works with:
- English
- Shona (Zimbabwe)
- Ndebele (Zimbabwe/South Africa)
- Zulu (South Africa)
- Xhosa (South Africa)
- Afrikaans (South Africa)

Just paste the conversation in any language and ask Claude to process it!

---

## 📚 Full Documentation

- **[CLAUDE_SETUP.md](CLAUDE_SETUP.md)** - Complete setup guide
- **[MCP_COMPLIANCE.md](MCP_COMPLIANCE.md)** - MCP specification compliance
- **[USAGE_GUIDE.md](USAGE_GUIDE.md)** - All features

---

## 🐛 Troubleshooting

**No tools icon?**
- Make sure server is running: `python mcp_server.py`
- Check config path is correct
- Restart Claude Desktop

**Translation not working?**
```bash
pip install transformers torch
```

---

## 🎉 That's It!

Keep `python mcp_server.py` running, use Claude normally, and ask it to process conversations. Everything else is automatic!
