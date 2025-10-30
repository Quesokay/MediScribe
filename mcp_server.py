"""
MediScribe MCP Server
Model Context Protocol server for real-time medical conversation processing
ChatGPT sends conversation transcripts directly to MediScribe for processing

WORKFLOW:
1. User connects ChatGPT to MediScribe MCP server
2. User has conversation in ChatGPT voice mode
3. ChatGPT calls process_conversation tool with transcript
4. MediScribe auto-detects language, translates if needed, extracts data
5. Returns structured medical data to ChatGPT
6. Optionally saves to database
"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio
import json
from typing import Optional
from medical_extractor_simple import MedicalExtractor
from database_saver import MedicalRecordDB
from datetime import datetime


# Initialize components
# Note: Using print() for logging - in STDIO mode, this goes to stderr automatically
import sys
import io
import os

# Force UTF-8 encoding for Windows console
if sys.platform == 'win32':
    os.system('chcp 65001 >nul 2>&1')  # Set console to UTF-8

# Set UTF-8 encoding for both stdout and stderr
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', line_buffering=True)
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace', line_buffering=True)

print("Initializing MediScribe MCP Server...", file=sys.stderr)

# Get the project directory (where this script is located)
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_DIR, "medical_records.json")

extractor = MedicalExtractor()
db = MedicalRecordDB(db_path=DB_PATH)
print("Medical extractor ready", file=sys.stderr)
print(f"Database ready at: {DB_PATH}", file=sys.stderr)

# Try to load translator
try:
    from translator import MultilingualTranslator
    translator = MultilingualTranslator(translation_method="nllb")
    TRANSLATION_AVAILABLE = True
    print("Multilingual translation ready (NLLB-200)", file=sys.stderr)
    print("  Supported: Shona, Ndebele, Zulu, Xhosa, Afrikaans -> English", file=sys.stderr)
except Exception as e:
    print(f"Translation not available: {e}", file=sys.stderr)
    print("  English-only mode", file=sys.stderr)
    TRANSLATION_AVAILABLE = False

print("\n" + "="*70, file=sys.stderr)
print("MediScribe MCP Server Ready!", file=sys.stderr)
print("="*70, file=sys.stderr)
print("Waiting for Claude to connect and send conversations...", file=sys.stderr)
print("="*70 + "\n", file=sys.stderr)

# Create MCP server
app = Server("mediscribe")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available MCP tools"""
    tools = [
        Tool(
            name="process_conversation",
            description="Process a medical conversation from ChatGPT voice mode. "
                       "Auto-detects language, translates if needed (Shona, Ndebele, Zulu, Xhosa, Afrikaans), "
                       "extracts structured medical data (patient info, symptoms, diagnosis, medications, vital signs), "
                       "and optionally saves to database. This is the main tool to use after a voice conversation.",
            inputSchema={
                "type": "object",
                "properties": {
                    "conversation": {
                        "type": "string",
                        "description": "The conversation transcript from ChatGPT voice mode. Can be in English or any supported African language."
                    },
                    "save_to_db": {
                        "type": "boolean",
                        "description": "Whether to save extracted data to database (default: true)",
                        "default": True
                    }
                },
                "required": ["conversation"]
            }
        ),
        Tool(
            name="extract_medical_data",
            description="Extract structured medical information from English transcription text only. "
                       "Use process_conversation instead if language detection/translation is needed. "
                       "Returns patient info, symptoms, diagnosis, medications, vital signs, etc.",
            inputSchema={
                "type": "object",
                "properties": {
                    "transcription": {
                        "type": "string",
                        "description": "Medical transcription text in English"
                    },
                    "save_to_db": {
                        "type": "boolean",
                        "description": "Whether to save extracted data to database (default: false)",
                        "default": False
                    }
                },
                "required": ["transcription"]
            }
        ),
        Tool(
            name="search_patient_records",
            description="Search medical records database by patient name",
            inputSchema={
                "type": "object",
                "properties": {
                    "patient_name": {
                        "type": "string",
                        "description": "Patient name to search for"
                    }
                },
                "required": ["patient_name"]
            }
        ),
        Tool(
            name="get_patient_record",
            description="Retrieve a specific medical record by record ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "record_id": {
                        "type": "string",
                        "description": "Record ID (format: REC-YYYYMMDDHHMMSS)"
                    }
                },
                "required": ["record_id"]
            }
        ),
        Tool(
            name="get_all_records",
            description="Retrieve all medical records from the database",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "number",
                        "description": "Maximum number of records to return (default: 50)",
                        "default": 50
                    }
                }
            }
        ),
        Tool(
            name="save_to_database",
            description="Save extracted medical data to the database",
            inputSchema={
                "type": "object",
                "properties": {
                    "extracted_data": {
                        "type": "object",
                        "description": "Extracted medical data object (from extract_medical_data)"
                    }
                },
                "required": ["extracted_data"]
            }
        ),
        Tool(
            name="process_file",
            description="Process a transcription file and extract medical data",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to transcription file (.txt or .json)"
                    },
                    "save_to_db": {
                        "type": "boolean",
                        "description": "Whether to save extracted data to database (default: false)",
                        "default": False
                    }
                },
                "required": ["file_path"]
            }
        )
    ]
    
    # Add translation tool if available
    if TRANSLATION_AVAILABLE:
        tools.append(
            Tool(
                name="translate_and_extract",
                description="Translate non-English medical transcription to English and extract structured data. "
                           "Supports Shona, Ndebele, Zulu, Xhosa, Afrikaans.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "transcription": {
                            "type": "string",
                            "description": "Medical transcription in any supported language"
                        },
                        "source_language": {
                            "type": "string",
                            "description": "Source language (optional, auto-detected if not provided)",
                            "enum": ["shona", "ndebele", "zulu", "xhosa", "afrikaans", "english"]
                        },
                        "save_to_db": {
                            "type": "boolean",
                            "description": "Whether to save extracted data to database (default: false)",
                            "default": False
                        }
                    },
                    "required": ["transcription"]
                }
            )
        )
    
    return tools


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls from ChatGPT"""
    
    try:
        if name == "process_conversation":
            # Main tool: Process conversation with auto-translation
            conversation = arguments["conversation"]
            save_to_db = arguments.get("save_to_db", True)
            
            print("\n" + "="*70, file=sys.stderr)
            print(f"Processing conversation from Claude", file=sys.stderr)
            print(f"   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", file=sys.stderr)
            print(f"   Length: {len(conversation)} characters", file=sys.stderr)
            print("="*70, file=sys.stderr)
            
            # Step 1: Language detection
            original_language = "english"
            translated_text = conversation
            
            if TRANSLATION_AVAILABLE:
                print("Detecting language...", file=sys.stderr)
                original_language = translator.detect_language(conversation)
                print(f"   Detected: {original_language.title()}", file=sys.stderr)
                
                # Step 2: Translation if needed
                if original_language != "english":
                    print(f"Translating from {original_language.title()} to English...", file=sys.stderr)
                    translated_text, _ = translator.translate(conversation, original_language)
                    print("   Translation complete", file=sys.stderr)
                else:
                    print("   Already in English", file=sys.stderr)
            else:
                print("Translation not available - processing as English", file=sys.stderr)
            
            # Step 3: Extract medical data
            print("Extracting medical data...", file=sys.stderr)
            extracted_data = extractor.extract_from_text(translated_text)
            
            # Add metadata
            extracted_data["original_language"] = original_language
            extracted_data["processed_at"] = datetime.now().isoformat()
            extracted_data["source"] = "chatgpt_voice_mode"
            
            if original_language != "english":
                extracted_data["original_text"] = conversation
                extracted_data["translated_text"] = translated_text
            
            print("   Extraction complete", file=sys.stderr)
            
            # Step 4: Save to database if requested
            if save_to_db:
                print("Saving to database...", file=sys.stderr)
                record_id = db.add_record(extracted_data)
                extracted_data["record_id"] = record_id
                print(f"   Saved as: {record_id}", file=sys.stderr)
            
            # Display summary
            print("\nSummary:", file=sys.stderr)
            if extracted_data.get("patient_name"):
                print(f"   Patient: {extracted_data['patient_name']}", file=sys.stderr)
            if extracted_data.get("symptoms"):
                print(f"   Symptoms: {len(extracted_data['symptoms'])} found", file=sys.stderr)
            if extracted_data.get("diagnosis"):
                print(f"   Diagnosis: {len(extracted_data['diagnosis'])} found", file=sys.stderr)
            if extracted_data.get("medications"):
                print(f"   Medications: {len(extracted_data['medications'])} found", file=sys.stderr)
            print("="*70 + "\n", file=sys.stderr)
            
            # Return formatted response
            response = {
                "success": True,
                "message": "Conversation processed successfully",
                "original_language": original_language,
                "data": extracted_data
            }
            
            # Ensure ASCII-safe JSON output
            return [TextContent(
                type="text",
                text=json.dumps(response, indent=2, ensure_ascii=True)
            )]
        
        elif name == "extract_medical_data":
            # Extract medical data from transcription
            transcription = arguments["transcription"]
            save_to_db = arguments.get("save_to_db", False)
            
            # Extract data
            extracted_data = extractor.extract_from_text(transcription)
            extracted_data["processed_at"] = datetime.now().isoformat()
            
            # Save to database if requested
            if save_to_db:
                record_id = db.add_record(extracted_data)
                extracted_data["record_id"] = record_id
            
            return [TextContent(
                type="text",
                text=json.dumps(extracted_data, indent=2, ensure_ascii=True)
            )]
        
        elif name == "translate_and_extract":
            if not TRANSLATION_AVAILABLE:
                return [TextContent(
                    type="text",
                    text=json.dumps({
                        "error": "Translation not available. Install required packages: pip install transformers torch"
                    }, ensure_ascii=True)
                )]
            
            transcription = arguments["transcription"]
            source_lang = arguments.get("source_language")
            save_to_db = arguments.get("save_to_db", False)
            
            # Translate
            translated_text, detected_lang = translator.translate(transcription, source_lang)
            
            # Extract from translated text
            extracted_data = extractor.extract_from_text(translated_text)
            extracted_data["original_language"] = detected_lang
            extracted_data["translated_text"] = translated_text
            extracted_data["processed_at"] = datetime.now().isoformat()
            
            # Save to database if requested
            if save_to_db:
                record_id = db.add_record(extracted_data)
                extracted_data["record_id"] = record_id
            
            return [TextContent(
                type="text",
                text=json.dumps(extracted_data, indent=2, ensure_ascii=True)
            )]
        
        elif name == "search_patient_records":
            patient_name = arguments["patient_name"]
            records = db.search_by_patient(patient_name)
            
            return [TextContent(
                type="text",
                text=json.dumps({
                    "patient_name": patient_name,
                    "records_found": len(records),
                    "records": records
                }, indent=2, ensure_ascii=True)
            )]
        
        elif name == "get_patient_record":
            record_id = arguments["record_id"]
            record = db.get_record(record_id)
            
            if record:
                return [TextContent(
                    type="text",
                    text=json.dumps(record, indent=2, ensure_ascii=True)
                )]
            else:
                return [TextContent(
                    type="text",
                    text=json.dumps({"error": f"Record not found: {record_id}"}, ensure_ascii=True)
                )]
        
        elif name == "get_all_records":
            limit = arguments.get("limit", 50)
            records = db.get_all_records(limit=limit)
            
            return [TextContent(
                type="text",
                text=json.dumps({
                    "total_records": len(records),
                    "records": records
                }, indent=2, ensure_ascii=True)
            )]
        
        elif name == "save_to_database":
            extracted_data = arguments["extracted_data"]
            record_id = db.add_record(extracted_data)
            
            return [TextContent(
                type="text",
                text=json.dumps({
                    "success": True,
                    "record_id": record_id,
                    "message": f"Record saved successfully as {record_id}"
                }, indent=2, ensure_ascii=True)
            )]
        
        elif name == "process_file":
            file_path = arguments["file_path"]
            save_to_db = arguments.get("save_to_db", False)
            
            # Extract from file
            extracted_data = extractor.extract_from_file(file_path)
            extracted_data["source_file"] = file_path
            extracted_data["processed_at"] = datetime.now().isoformat()
            
            # Save to database if requested
            if save_to_db:
                record_id = db.add_record(extracted_data)
                extracted_data["record_id"] = record_id
            
            return [TextContent(
                type="text",
                text=json.dumps(extracted_data, indent=2, ensure_ascii=True)
            )]
        
        else:
            return [TextContent(
                type="text",
                text=json.dumps({"error": f"Unknown tool: {name}"}, ensure_ascii=True)
            )]
    
    except Exception as e:
        return [TextContent(
            type="text",
            text=json.dumps({
                "error": str(e),
                "tool": name,
                "arguments": arguments
            }, ensure_ascii=True)
        )]


async def main():
    """Run the MCP server"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
