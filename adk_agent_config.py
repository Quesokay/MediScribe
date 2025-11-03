"""
ADK Agent Configuration for MediScribe
Configures the agent to work with ADK API server and web UI
"""
import os
from pathlib import Path
from adk.agents import Agent
from adk.tools import tool
from google import genai

# Import MCP tools
from medical_extractor_simple import MedicalExtractor
from database_saver import MedicalRecordDB
from datetime import datetime

# Initialize components
PROJECT_DIR = Path(__file__).parent
DB_PATH = PROJECT_DIR / "medical_records.json"

extractor = MedicalExtractor()
db = MedicalRecordDB(db_path=str(DB_PATH))

# Try to load translator
try:
    from translator import MultilingualTranslator
    translator = MultilingualTranslator(translation_method="nllb")
    TRANSLATION_AVAILABLE = True
    print("✓ Multilingual translation ready (NLLB-200)")
except Exception as e:
    print(f"⚠ Translation not available: {e}")
    TRANSLATION_AVAILABLE = False


# Define ADK tools
@tool
def process_conversation(conversation: str, save_to_db: bool = True) -> dict:
    """
    Process a medical conversation with auto-translation and data extraction.
    Supports English, Shona, Ndebele, Zulu, Xhosa, and Afrikaans.
    
    Args:
        conversation: The conversation transcript from voice interaction
        save_to_db: Whether to save extracted data to database (default: True)
    
    Returns:
        Dictionary with extracted medical data
    """
    print(f"\n{'='*70}")
    print(f"Processing conversation ({len(conversation)} chars)")
    print(f"{'='*70}")
    
    # Language detection and translation
    original_language = "english"
    translated_text = conversation
    
    if TRANSLATION_AVAILABLE:
        original_language = translator.detect_language(conversation)
        print(f"Detected language: {original_language.title()}")
        
        if original_language != "english":
            print(f"Translating from {original_language.title()} to English...")
            translated_text, _ = translator.translate(conversation, original_language)
        else:
            print("Already in English")
    
    # Extract medical data
    print("Extracting medical data...")
    extracted_data = extractor.extract_from_text(translated_text)
    
    # Add metadata
    extracted_data["original_language"] = original_language
    extracted_data["processed_at"] = datetime.now().isoformat()
    extracted_data["source"] = "adk_voice_interaction"
    
    if original_language != "english":
        extracted_data["original_text"] = conversation
        extracted_data["translated_text"] = translated_text
    
    # Save to database
    if save_to_db:
        record_id = db.add_record(extracted_data)
        extracted_data["record_id"] = record_id
        print(f"Saved as: {record_id}")
    
    print(f"{'='*70}\n")
    
    return {
        "success": True,
        "message": "Conversation processed successfully",
        "original_language": original_language,
        "data": extracted_data
    }


@tool
def extract_medical_data(transcription: str, save_to_db: bool = False) -> dict:
    """
    Extract structured medical information from English transcription.
    
    Args:
        transcription: Medical transcription text in English
        save_to_db: Whether to save extracted data to database
    
    Returns:
        Dictionary with extracted medical data
    """
    extracted_data = extractor.extract_from_text(transcription)
    extracted_data["processed_at"] = datetime.now().isoformat()
    
    if save_to_db:
        record_id = db.add_record(extracted_data)
        extracted_data["record_id"] = record_id
    
    return extracted_data


@tool
def search_patient_records(patient_name: str) -> dict:
    """
    Search medical records database by patient name.
    
    Args:
        patient_name: Patient name to search for
    
    Returns:
        Dictionary with matching records
    """
    records = db.search_by_patient(patient_name)
    return {
        "patient_name": patient_name,
        "records_found": len(records),
        "records": records
    }


@tool
def get_all_records(limit: int = 50) -> dict:
    """
    Retrieve all medical records from the database.
    
    Args:
        limit: Maximum number of records to return
    
    Returns:
        Dictionary with all records
    """
    records = db.get_all_records(limit=limit)
    return {
        "total_records": len(records),
        "records": records
    }


@tool
def get_patient_record(record_id: str) -> dict:
    """
    Retrieve a specific medical record by ID.
    
    Args:
        record_id: Record ID (format: REC-YYYYMMDDHHMMSS)
    
    Returns:
        Dictionary with record data or error
    """
    record = db.get_record(record_id)
    if record:
        return record
    else:
        return {"error": f"Record not found: {record_id}"}


# Create the agent
def create_agent(api_key: str = None) -> Agent:
    """Create and return the MediScribe agent"""
    
    if not api_key:
        api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not set. Use: set GOOGLE_API_KEY=your_key")
    
    # Configure Gemini client
    client = genai.Client(api_key=api_key)
    
    # Create agent
    agent = Agent(
        name="MediScribe",
        model="gemini-2.0-flash-exp",
        client=client,
        system_instruction="""You are MediScribe, an AI medical assistant for healthcare professionals.

Your capabilities:
- Process voice conversations in multiple languages (English, Shona, Ndebele, Zulu, Xhosa, Afrikaans)
- Auto-detect language and translate to English if needed
- Extract structured medical data: patient info, symptoms, diagnosis, medications, vital signs
- Save records to database and retrieve them later

When processing a conversation:
1. Use process_conversation() for any medical conversation (handles translation automatically)
2. Present extracted data clearly with key medical information highlighted
3. Offer to save to database or search for related records

Be professional, accurate, and helpful. Always confirm important medical details.""",
        tools=[
            process_conversation,
            extract_medical_data,
            search_patient_records,
            get_all_records,
            get_patient_record
        ]
    )
    
    print(f"\n{'='*70}")
    print("MediScribe Agent Created")
    print(f"{'='*70}")
    print(f"Model: {agent.model}")
    print(f"Tools: {len(agent.tools)} available")
    print(f"Database: {DB_PATH}")
    print(f"Translation: {'Enabled' if TRANSLATION_AVAILABLE else 'English only'}")
    print(f"{'='*70}\n")
    
    return agent


# Export for ADK API server
root_agent = create_agent()
