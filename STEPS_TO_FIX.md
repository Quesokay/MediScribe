# Fix Claude Desktop Connection - Simple Steps

## ✅ I've Already Done:

1. ✅ Updated Claude config with **full Python path**
2. ✅ Killed all Claude processes
3. ✅ Verified all files are in place

---

## 🚀 What You Need to Do Now:

### Step 1: Wait 10 Seconds

Just wait 10 seconds to make sure Claude is fully closed.

---

### Step 2: Start MCP Server

Open a **new terminal** and run:

```powershell
python mcp_server.py
```

You should see:
```
🚀 Initializing MediScribe MCP Server...
✓ Medical extractor ready
✓ Database ready
✓ Multilingual translation ready

======================================================================
MediScribe MCP Server Ready!
======================================================================
```

**Keep this terminal open!** Don't close it or type anything in it.

---

### Step 3: Start Claude Desktop

1. **Open Claude Desktop**
2. **Wait 30 seconds** for it to fully load and connect to MCP

---

### Step 4: Look for Tools

The tools icon might be in different places depending on your Claude version:

**Option 1:** Look at the **bottom of the chat input box** for a 🔧 icon

**Option 2:** Look in the **top right corner** for a tools menu

**Option 3:** Try typing this in Claude:
```
List your available tools
```

or

```
What MCP servers are you connected to?
```

Claude should respond with information about MediScribe tools even if you don't see an icon.

---

### Step 5: Test It

If Claude responds that it has tools, try this:

```
Process this medical conversation:

Doctor: Hi, what's your name?
Patient: I'm John Doe, 45 years old.
Doctor: What brings you in?
Patient: I have a fever.
Doctor: Temperature is 101.5F. I'll prescribe Ibuprofen 400mg.
```

---

## 🔍 Check MCP Server Terminal

When Claude connects, you should see activity in the MCP server terminal. If you see nothing when Claude starts, that means Claude isn't connecting.

---

## 🐛 If Still Not Working:

### Check Claude Version

1. Open Claude Desktop
2. Go to Settings → About
3. Check version number

**MCP requires Claude Desktop version 0.7.0 or higher**

If you have an older version:
- Download latest from: https://claude.ai/download
- Install and restart

### Check Claude Logs

Run this to see if there are errors:

```powershell
Get-ChildItem "$env:APPDATA\Claude\logs" | Sort-Object LastWriteTime -Descending | Select-Object -First 1 | Get-Content -Tail 50
```

Look for errors mentioning "mediscribe" or "mcp_server"

### Try Simple Test

Run this to test if MCP works at all:

```powershell
python test_mcp_connection.py
```

This will verify all components are working.

---

## 📊 Current Configuration

Your Claude config is now set to:
```json
{
  "mcpServers": {
    "mediscribe": {
      "command": "C:/Users/moyov/AppData/Local/Programs/Python/Python311/python.exe",
      "args": [
        "C:/Clone_wars/MediScribe/mcp_server.py"
      ]
    }
  }
}
```

Location: `C:\Users\moyov\AppData\Roaming\Claude\claude_desktop_config.json`

---

## ⚠️ Important Notes

1. **MCP server must be running** before you start Claude
2. **Don't type in the MCP server terminal** - it only accepts JSON-RPC from Claude
3. **Wait 30 seconds** after starting Claude for MCP to connect
4. **Check Claude version** - MCP requires 0.7.0+

---

## 🎯 Quick Checklist

- [ ] MCP server is running (`python mcp_server.py`)
- [ ] Claude Desktop is completely closed (check Task Manager)
- [ ] Waited 10 seconds after closing Claude
- [ ] Started Claude Desktop fresh
- [ ] Waited 30 seconds after Claude starts
- [ ] Checked for tools icon or asked Claude about tools
- [ ] Claude version is 0.7.0 or higher

---

**Try these steps and let me know what happens!**
