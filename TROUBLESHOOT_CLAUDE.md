# Troubleshooting Claude Desktop Connection

## Issue: Not Seeing MediScribe Tools in Claude

Let's diagnose and fix this step by step.

---

## Step 1: Verify Configuration

Run this command:
```powershell
Get-Content "$env:APPDATA\Claude\claude_desktop_config.json"
```

You should see:
```json
{
  "mcpServers": {
    "mediscribe": {
      "command": "python",
      "args": [
        "C:/Clone_wars/MediScribe/mcp_server.py"
      ]
    }
  }
}
```

✅ **This is correct!**

---

## Step 2: Completely Quit Claude

Claude Desktop needs to be **completely closed** to reload the configuration.

### Windows:

1. **Close all Claude windows**
2. **Open Task Manager** (Ctrl+Shift+Esc)
3. **Find all "Claude" processes**
4. **End each one** (right-click → End Task)
5. **Wait 10 seconds**

Or run this command:
```powershell
Get-Process -Name "claude" -ErrorAction SilentlyContinue | Stop-Process -Force
```

---

## Step 3: Test MCP Server

Before starting Claude, test if the server works:

```powershell
python test_mcp_connection.py
```

This will verify all components are working.

---

## Step 4: Start MCP Server

```powershell
python mcp_server.py
```

You should see:
```
🚀 Initializing MediScribe MCP Server...
✓ Medical extractor ready
✓ Database ready
✓ Multilingual translation ready (NLLB-200)

======================================================================
MediScribe MCP Server Ready!
======================================================================
Waiting for ChatGPT/Claude to connect and send conversations...
======================================================================
```

**Keep this terminal open!**

---

## Step 5: Start Claude Desktop

1. **Open Claude Desktop**
2. **Wait 30 seconds** for it to fully load
3. **Look for the tools icon** 🔧

### Where to Find Tools Icon:

The tools icon location varies by Claude version:
- **Bottom of chat input** (most common)
- **Top right corner**
- **Settings menu**
- **Three dots menu (⋮)**

Try clicking around the interface to find it.

---

## Step 6: Check Claude Logs

If still not working, check Claude's logs:

### Windows:
```powershell
Get-Content "$env:APPDATA\Claude\logs\mcp*.log" -Tail 50
```

Look for errors related to "mediscribe" or "mcp_server.py"

---

## Common Issues & Fixes

### Issue 1: Python Not Found

**Symptom:** Claude logs show "python is not recognized"

**Fix:** Use full Python path in config:
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

### Issue 2: Server Not Starting

**Symptom:** No output in MCP server terminal when Claude starts

**Fix:** Check if server is already running:
```powershell
Get-Process -Name "python" | Where-Object {$_.CommandLine -like "*mcp_server*"}
```

Kill any existing instances and restart.

### Issue 3: Wrong Python Version

**Symptom:** Import errors in server

**Fix:** Make sure you're using Python 3.8+:
```powershell
python --version
```

### Issue 4: Claude Desktop Too Old

**Symptom:** No MCP support at all

**Fix:** Update Claude Desktop to latest version:
- Download from: https://claude.ai/download
- Install latest version
- Restart computer

---

## Alternative: Use Absolute Python Path

Edit the config to use the full Python path:

```powershell
# Find Python path
(Get-Command python).Path
```

Then update config:
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

---

## Step 7: Enable MCP Developer Mode (If Available)

Some Claude versions have a developer mode:

1. Open Claude Settings
2. Look for "Developer" or "Advanced"
3. Enable "MCP Developer Mode" or "Show MCP Tools"
4. Restart Claude

---

## Step 8: Check Claude Version

Make sure you have Claude Desktop with MCP support:

1. Open Claude Desktop
2. Go to Settings → About
3. Check version number
4. MCP support requires version **0.7.0+**

If older, update from: https://claude.ai/download

---

## Step 9: Manual Test

Try this in Claude (even without seeing tools):

```
Can you list your available tools?
```

or

```
Do you have access to any MCP servers?
```

Claude might respond with the tools even if the icon isn't visible.

---

## Step 10: Check Firewall/Antivirus

Sometimes security software blocks MCP:

1. Check Windows Defender
2. Check antivirus software
3. Temporarily disable and test
4. Add exception for Python and Claude

---

## Still Not Working?

### Create a Simple Test Server

Let's test with a minimal MCP server:

```python
# test_simple_mcp.py
from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio
import asyncio

app = Server("test")

@app.list_tools()
async def list_tools():
    return [
        Tool(
            name="hello",
            description="Say hello",
            inputSchema={"type": "object", "properties": {}}
        )
    ]

@app.call_tool()
async def call_tool(name, arguments):
    return [TextContent(type="text", text="Hello from MCP!")]

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
```

Update Claude config to use this:
```json
{
  "mcpServers": {
    "test": {
      "command": "python",
      "args": ["C:/Clone_wars/MediScribe/test_simple_mcp.py"]
    }
  }
}
```

If this works, the issue is with MediScribe server. If not, it's a Claude configuration issue.

---

## Get Help

If nothing works, check:
1. Claude Desktop documentation
2. MCP GitHub issues: https://github.com/modelcontextprotocol/
3. Claude support

---

## Quick Checklist

- [ ] Claude Desktop completely closed (check Task Manager)
- [ ] Config file in correct location
- [ ] Config file has correct JSON format
- [ ] Python path is correct
- [ ] MCP server starts without errors
- [ ] Claude Desktop restarted after config change
- [ ] Waited 30+ seconds after Claude starts
- [ ] Checked all possible tool icon locations
- [ ] Claude Desktop version 0.7.0+
- [ ] No firewall/antivirus blocking

---

**Most common fix:** Completely quit Claude (kill all processes), wait 10 seconds, restart Claude, wait 30 seconds.
