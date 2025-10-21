# MediScribe MCP Server Setup Guide

Transform MediScribe into an MCP server that any AI assistant can use!

## What is MCP?

Model Context Protocol (MCP) lets AI assistants call your MediScribe tools directly. Once set up, any MCP-compatible AI (Claude Desktop, Kiro IDE, etc.) can:

- Extract medical data from transcriptions
- Translate multilingual patient notes
- Search your medical records database
- Save records automatically

## Quick Setup

### 1. Install MCP Dependencies

```bash
pip install mcp>=0.9.0
```

Or install everything at once:

```bash
pip install -r mcp_requirements.txt
```

### 2. Test the MCP Server

```bash
python mcp_server.py
```

The server will start and wait for MCP protocol messages via stdin/stdout.

### 3. Configure Your MCP Client

#### For Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (Mac) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "mediscribe": {
      "command": "python",
      "args": ["C:/Clone_wars/MediScribe/mcp_server.py"],
      "env": {}
    }
  }
}
```

#### For Kiro IDE

Add to `.kiro/settings/mcp.json` in your workspace:

```json
{
  "mcpServers": {
    "mediscribe": {
      "command": "python",
      "args": ["mcp_server.py"],
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

#### For Other MCP Clients

Use the standard MCP configuration format:

```json
{
  "command": "python",
  "args": ["path/to/mcp_server.py"]
}
```

## Available Tools

Once connected, AI assistants can use these MediScribe tools:

### 1. extract_medical_data
Extract structured medical information from transcription text.

**Input:**
- `transcription` (string, required): Medical transcription text
- `save_to_db` (boolean, optional): Save to database (default: false)

**Example:**
```json
{
  "transcription": "Patient John Doe, 45 year old male, fever and cough...",
  "save_to_db": true
}
```

### 2. translate_and_extract
Translate non-English transcription and extract data.

**Input:**
- `transcription` (string, required): Text in any supported language
- `source_language` (string, optional): Language code (auto-detected if omitted)
- `save_to_db` (boolean, optional): Save to database

**Supported Languages:** Shona, Ndebele, Zulu, Xhosa, Afrikaans, English

### 3. search_patient_records
Search medical records by patient name.

**Input:**
- `patient_name` (string, required): Patient name to search

### 4. get_patient_record
Retrieve a specific record by ID.

**Input:**
- `record_id` (string, required): Record ID (format: REC-YYYYMMDDHHMMSS)

### 5. get_all_records
Get all medical records.

**Input:**
- `limit` (number, optional): Max records to return (default: 50)

### 6. save_to_database
Save extracted data to database.

**Input:**
- `extracted_data` (object, required): Extracted medical data

### 7. process_file
Process a transcription file.

**Input:**
- `file_path` (string, required): Path to .txt or .json file
- `save_to_db` (boolean, optional): Save to database

## Usage Examples

### Example 1: Extract from Text

AI Assistant prompt:
```
Use the mediscribe extract_medical_data tool to process this transcription:
"Patient Sarah Lee, 32 year old female, presents with headache and nausea..."
```

### Example 2: Multilingual Processing

AI Assistant prompt:
```
Use mediscribe translate_and_extract to process this Shona transcription:
"Murwere John, makore 45, ndine fivha..."
```

### Example 3: Search Records

AI Assistant prompt:
```
Use mediscribe search_patient_records to find all records for "John Doe"
```

## Testing the MCP Server

### Test with MCP Inspector

```bash
# Install MCP inspector
npm install -g @modelcontextprotocol/inspector

# Run inspector
mcp-inspector python mcp_server.py
```

This opens a web interface to test your MCP tools interactively.

### Test Programmatically

Create `test_mcp_client.py`:

```python
import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_mediscribe():
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # List available tools
            tools = await session.list_tools()
            print("Available tools:", [t.name for t in tools.tools])
            
            # Test extraction
            result = await session.call_tool(
                "extract_medical_data",
                {
                    "transcription": "Patient John Doe, 45 year old male, fever 101.5F",
                    "save_to_db": False
                }
            )
            print("Extraction result:", result)

asyncio.run(test_mediscribe())
```

## Troubleshooting

### Server won't start
- Ensure all dependencies are installed: `pip install -r mcp_requirements.txt`
- Check Python version: `python --version` (needs 3.8+)
- Verify spaCy model: `python -m spacy download en_core_web_sm`

### Client can't connect
- Check file paths in configuration (use absolute paths)
- Verify Python is in your PATH
- Check server logs for errors

### Tools not working
- Test individual MediScribe modules first:
  ```bash
  python medical_extractor_simple.py
  python translator_simple.py
  ```
- Check database file permissions
- Verify input format matches schema

## Advanced Configuration

### Custom Database Path

Modify `mcp_server.py`:

```python
self.db = MedicalRecordDB("custom_path/records.json")
```

### Enable Google Translate

```python
self.translator = SimpleTranslator(method="google")
```

### Add Custom Tools

Add new tools in `setup_handlers()`:

```python
Tool(
    name="your_custom_tool",
    description="Your tool description",
    inputSchema={...}
)
```

## Security Considerations

- MCP server runs locally with your user permissions
- Database files are stored locally (no cloud sync)
- No external API calls by default (privacy-first)
- Consider encrypting `medical_records.json` for production use

## Next Steps

1. ✅ Install MCP dependencies
2. ✅ Test the server locally
3. ✅ Configure your MCP client
4. ✅ Try example queries
5. 🚀 Integrate with your workflow!

## Resources

- [MCP Documentation](https://modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MediScribe Documentation](README.md)

---

**MediScribe MCP Server** - Medical transcription extraction for AI assistants
