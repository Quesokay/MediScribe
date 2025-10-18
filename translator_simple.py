"""
Simple Translation Module - Lightweight Alternative
Uses smaller models or API-based translation
"""
from typing import Tuple, Optional
import re


class SimpleTranslator:
    """Lightweight translator using pattern matching and optional API"""
    
    def __init__(self, method: str = "pattern"):
        """
        Initialize translator
        
        Args:
            method: "pattern" (offline, instant) or "google" (requires API key)
        """
        self.method = method
        
        # Common medical phrases in Shona/Ndebele → English
        self.medical_phrases = {
            # Shona
            "ndiri kunzwa kurwara": "I am feeling pain",
            "ndine fivha": "I have fever",
            "ndine chikosoro": "I have a cough",
            "murwere": "patient",
            "chiremba": "doctor",
            "mushonga": "medicine",
            "tembiricha": "temperature",
            "makore": "years",
            "murume": "male",
            "mukadzi": "female",
            
            # Ndebele
            "nginobuhlungu": "I have pain",
            "nginesiyezi": "I have fever",
            "ngikhwehlela": "I am coughing",
            "isiguli": "patient",
            "udokotela": "doctor",
            "umuthi": "medicine",
            "izinga lokushisa": "temperature",
            "iminyaka": "years",
            "owesilisa": "male",
            "owesifazane": "female",
        }
        
        self.language_codes = {
            "shona": {"name": "Shona"},
            "ndebele": {"name": "Ndebele"},
            "english": {"name": "English"},
        }
    
    def detect_language(self, text: str) -> str:
        """Detect language using keyword matching"""
        text_lower = text.lower()
        
        # Shona indicators
        shona_words = ["ndiri", "ndine", "murwere", "chiremba", "mushonga", "makore"]
        shona_count = sum(1 for word in shona_words if word in text_lower)
        
        # Ndebele indicators  
        ndebele_words = ["ngi", "isiguli", "udokotela", "umuthi", "iminyaka"]
        ndebele_count = sum(1 for word in ndebele_words if word in text_lower)
        
        if shona_count > ndebele_count and shona_count > 0:
            return "shona"
        elif ndebele_count > 0:
            return "ndebele"
        else:
            return "english"
    
    def translate_pattern(self, text: str, source_lang: str) -> str:
        """Simple pattern-based translation"""
        if source_lang == "english":
            return text
        
        translated = text
        
        # Replace known medical phrases
        for phrase, translation in self.medical_phrases.items():
            translated = re.sub(
                r'\b' + re.escape(phrase) + r'\b',
                translation,
                translated,
                flags=re.IGNORECASE
            )
        
        # Add note about partial translation
        if translated != text:
            note = "\n\n[Note: This is a partial translation. Some phrases may remain in original language.]"
            translated = translated + note
        
        return translated
    
    def translate_google(self, text: str, source_lang: str) -> str:
        """Translate using Google Translate API"""
        try:
            from googletrans import Translator
            translator = Translator()
            
            lang_map = {"shona": "sn", "ndebele": "nd", "english": "en"}
            src_code = lang_map.get(source_lang, "auto")
            
            result = translator.translate(text, src=src_code, dest="en")
            return result.text
            
        except ImportError:
            print("⚠️  googletrans not installed. Install with: pip install googletrans==3.1.0a0")
            print("   Falling back to pattern matching...")
            return self.translate_pattern(text, source_lang)
        except Exception as e:
            print(f"⚠️  Google Translate error: {e}")
            print("   Falling back to pattern matching...")
            return self.translate_pattern(text, source_lang)
    
    def translate(self, text: str, source_lang: Optional[str] = None) -> Tuple[str, str]:
        """
        Translate text to English
        
        Args:
            text: Text to translate
            source_lang: Source language (auto-detect if None)
            
        Returns:
            Tuple of (translated_text, detected_language)
        """
        # Auto-detect language if not specified
        if source_lang is None:
            source_lang = self.detect_language(text)
            print(f"🔍 Detected language: {self.language_codes[source_lang]['name']}")
        
        # Skip translation if already in English
        if source_lang == "english":
            print(f"✓ Text already in English")
            return text, source_lang
        
        print(f"🌐 Translating from {self.language_codes[source_lang]['name']} to English...")
        
        # Translate based on method
        if self.method == "google":
            translated = self.translate_google(text, source_lang)
        else:
            translated = self.translate_pattern(text, source_lang)
        
        print("✓ Translation complete")
        
        return translated, source_lang


def main():
    """Test the simple translator"""
    print("="*70)
    print("SIMPLE TRANSLATOR TEST")
    print("="*70)
    print("Using lightweight pattern-based translation")
    print("(No large model download needed!)")
    print()
    
    translator = SimpleTranslator(method="pattern")
    
    # Test Shona
    shona_text = """
    Murwere: John Doe, makore 45, murume.
    Ndiri kunzwa kurwara musoro uye ndine fivha.
    Tembiricha: 38.5 degrees.
    Chiremba: Ndine chikosoro.
    Mushonga: Paracetamol 500mg.
    """
    
    print("TEST 1: Shona → English")
    print("-" * 70)
    print("Original:")
    print(shona_text)
    
    translated, lang = translator.translate(shona_text)
    print("\nTranslated:")
    print(translated)
    print()
    
    # Test Ndebele
    ndebele_text = """
    Isiguli: Sarah Moyo, iminyaka 32, owesifazane.
    Nginobuhlungu bekhanda futhi nginesiyezi.
    Izinga lokushisa: 37.8 degrees.
    Udokotela: Umuthi: Ibuprofen 400mg.
    """
    
    print("\n" + "="*70)
    print("TEST 2: Ndebele → English")
    print("-" * 70)
    print("Original:")
    print(ndebele_text)
    
    translated, lang = translator.translate(ndebele_text)
    print("\nTranslated:")
    print(translated)
    print()
    
    print("="*70)
    print("✓ Tests complete!")
    print()
    print("Note: This is a simple pattern-based translator.")
    print("For better quality, use:")
    print("  1. NLLB model (run download_model_slowly.py)")
    print("  2. Google Translate API (pip install googletrans==3.1.0a0)")


if __name__ == "__main__":
    main()
