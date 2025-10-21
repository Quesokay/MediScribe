"""
MediScribe MCP Server
Exposes medical transcription extraction capabilities via Model Context Protocol
"""
import asyncio
import json
from typing import Any, Dict, List, Optional
from pathlib import Path

# MCP SDK imports
from mcp.server import Server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
from mcp.server.stdio import stdio_server

# MediScribe imports
from medical_extractor_simple import MedicalExtractor
from database_saver import MedicalRecordDB
from translator_simple import SimpleTranslator


class MediScribeMCPServer:
    """MCP Server for MediScribe medical transcription extraction"""
    
    def __init__(self):
        self.server = Server("mediscribe")
        self.extractor = MedicalExtractor()
        self.db = MedicalRecordDB()
        self.translator = SimpleTranslator(method="pattern")
        
        # Register handlers
        self.setup_handlers()
    
    def setup_handlers(self):
        """Register MCP protocol handlers"""
        
        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            """List available MediScribe tools"""
            return [
                Tool(
                    name="extract_medical_data",
                    description="Extract structured medical information from transcription text. Returns patient info, symptoms, diagnosis, medications, vital signs, etc.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "transcription": {
                                "type": "string",
                                "description": "Medical transcription text to process"
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
                    name="translate_and_extract",
                    description="Translate non-English medical transcription to English and extract structured data. Supports Shona, Ndebele, Zulu, Xhosa, Afrikaans.",
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
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Any) -> List[TextContent]:
            """Handle tool calls"""
            
            try:
                if name == "extract_medical_data":
                    return await self.extract_medical_data(arguments)
                
                elif name == "translate_and_extract":
                    return await self.translate_and_extract(arguments)
                
                elif name == "search_patient_records":
                    return await self.search_patient_records(arguments)
                
                elif name == "get_patient_record":
                    return await self.get_patient_record(arguments)
                
                elif name == "get_all_records":
                    return await self.get_all_records(arguments)
                
                elif name == "save_to_database":
                    return await self.save_to_database(arguments)
                
                elif name == "process_file":
                    return await self.process_file(arguments)
                
                else:
                    return [TextContent(
                        type="text",
                        text=f"Unknown tool: {name}"
                    )]
            
            except Exception as e:
                return [TextContent(
                    type="text",
                    text=f"Error executing {name}: {str(e)}"
                )]
    
    async def extract_medical_data(self, args: Dict) -> List[TextContent]:
        """Extract medical data from transcription"""
        transcription = args["transcription"]
        save_to_db = args.get("save_to_db", False)
        
        # Extract data
        extracted = self.extractor.extract_from_text(transcription)
        
        # Save to database if requested
        record_id = None
        if save_to_db:
            record_id = self.db.add_record(extracted)
            extracted["record_id"] = record_id
        
        result = {
            "success": True,
            "extracted_data": extracted,
            "saved_to_database": save_to_db,
            "record_id": record_id
        }
        
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
    
    async def translate_and_extract(self, args: Dict) -> List[TextContent]:
        """Translate and extract medical data"""
        transcription = args["transcription"]
        source_lang = args.get("source_language")
        save_to_db = args.get("save_to_db", False)
        
        # Translate
        translated_text, detected_lang = self.translator.translate(
            transcription, 
            source_lang
        )
        
        # Extract from translated text
        extracted = self.extractor.extract_from_text(translated_text)
        extracted["original_language"] = detected_lang
        extracted["original_transcription"] = transcription
        
        # Save to database if requested
        record_id = None
        if save_to_db:
            record_id = self.db.add_record(extracted)
            extracted["record_id"] = record_id
        
        result = {
            "success": True,
            "detected_language": detected_lang,
            "translated_text": translated_text,
            "extracted_data": extracted,
            "saved_to_database": save_to_db,
            "record_id": record_id
        }
        
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
    
    async def search_patient_records(self, args: Dict) -> List[TextContent]:
        """Search for patient records"""
        patient_name = args["patient_name"]
        
        records = self.db.search_by_patient(patient_name)
        
        result = {
            "success": True,
            "patient_name": patient_name,
            "records_found": len(records),
            "records": records
        }
        
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
    
    async def get_patient_record(self, args: Dict) -> List[TextContent]:
        """Get a specific patient record"""
        record_id = args["record_id"]
        
        record = self.db.get_record(record_id)
        
        if record:
            result = {
                "success": True,
                "record": record
            }
        else:
            result = {
                "success": False,
                "error": f"Record not found: {record_id}"
            }
        
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
    
    async def get_all_records(self, args: Dict) -> List[TextContent]:
        """Get all records"""
        limit = args.get("limit", 50)
        
        all_records = self.db.get_all_records()
        records = all_records[:limit]
        
        result = {
            "success": True,
            "total_records": len(all_records),
            "returned_records": len(records),
            "records": records
        }
        
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
    
    async def save_to_database(self, args: Dict) -> List[TextContent]:
        """Save extracted data to database"""
        extracted_data = args["extracted_data"]
        
        record_id = self.db.add_record(extracted_data)
        
        result = {
            "success": True,
            "record_id": record_id,
            "message": f"Record saved successfully with ID: {record_id}"
        }
        
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
    
    async def process_file(self, args: Dict) -> List[TextContent]:
        """Process a transcription file"""
        file_path = args["file_path"]
        save_to_db = args.get("save_to_db", False)
        
        # Check if file exists
        if not Path(file_path).exists():
            return [TextContent(
                type="text",
                text=json.dumps({
                    "success": False,
                    "error": f"File not found: {file_path}"
                }, indent=2)
            )]
        
        # Extract from file
        extracted = self.extractor.extract_from_file(file_path)
        
        # Save to database if requested
        record_id = None
        if save_to_db:
            record_id = self.db.add_record(extracted)
            extracted["record_id"] = record_id
        
        result = {
            "success": True,
            "file_path": file_path,
            "extracted_data": extracted,
            "saved_to_database": save_to_db,
            "record_id": record_id
        }
        
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
    
    async def run(self):
        """Run the MCP server"""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


async def main():
    """Main entry point"""
    server = MediScribeMCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
