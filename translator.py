"""
Multilingual Translation Module for MediScribe
Supports Shona, Ndebele, and other languages → English
Uses NLLB (No Language Left Behind) by Meta and Google Translate API
"""
import os
from pathlib import Path
from typing import Dict, Optional, Tuple
import json


class MultilingualTranslator:
    """Handles translation from multiple languages to English"""
    
    def __init__(self, translation_method: str = "nllb", google_api_key: Optional[str] = None):
        """
        Initialize translator
        
        Args:
            translation_method: "nllb" (offline, free) or "google" (requires API key)
            google_api_key: Google Translate API key (if using Google)
        """
        self.method = translation_method
        self.google_api_key = google_api_key or os.getenv("GOOGLE_TRANSLATE_API_KEY")
        
        # Language code mappings
        self.language_codes = {
            "shona": {"nllb": "sna_Latn", "google": "sn", "name": "Shona"},
            "ndebele": {"nllb": "nde_Latn", "google": "nd", "name": "Ndebele"},
            "english": {"nllb": "eng_Latn", "google": "en", "name": "English"},
            "zulu": {"nllb": "zul_Latn", "google": "zu", "name": "Zulu"},
            "xhosa": {"nllb": "xho_Latn", "google": "xh", "name": "Xhosa"},
            "afrikaans": {"nllb": "afr_Latn", "google": "af", "name": "Afrikaans"},
        }
        
        self.model = None
        self.tokenizer = None
        
        if self.method == "nllb":
            self._load_nllb_model()
        elif self.method == "google" and not self.google_api_key:
            print("⚠️  Warning: Google Translate API key not found")
            print("   Set GOOGLE_TRANSLATE_API_KEY environment variable")
            print("   Falling back to NLLB (offline translation)")
            self.method = "nllb"
            self._load_nllb_model()
    
    def _load_nllb_model(self):
        """Load NLLB model for offline translation"""
        try:
            from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
            
            print("📥 Loading NLLB translation model...")
            print("   (First run will download ~2.5GB model)")
            
            # Use the smaller distilled model for faster performance
            model_name = "facebook/nllb-200-distilled-600M"
            
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            
            print("✓ NLLB model loaded successfully")
            
        except Exception as e:
            print(f"❌ Error loading NLLB model: {e}")
            print("   Install with: pip install transformers torch")
            raise
    
    def detect_language(self, text: str) -> str:
        """
        Detect the language of the input text
        
        Args:
            text: Input text
            
        Returns:
            Detected language code (e.g., "shona", "ndebele", "english")
        """
        # Simple keyword-based detection for common medical phrases
        # In production, use a proper language detection library
        
        text_lower = text.lower()
        
        # Shona indicators
        shona_words = ["ndiri", "ndinoda", "ndine", "murwere", "chipatara", "mushonga"]
        if any(word in text_lower for word in shona_words):
            return "shona"
        
        # Ndebele indicators
        ndebele_words = ["ngiyafuna", "ngilapha", "umkhuhlane", "isibhedlela", "umuthi"]
        if any(word in text_lower for word in ndebele_words):
            return "ndebele"
        
        # Default to English
        return "english"
    
    def translate_nllb(self, text: str, source_lang: str, target_lang: str = "english") -> str:
        """
        Translate using NLLB model (offline)
        
        Args:
            text: Text to translate
            source_lang: Source language (e.g., "shona", "ndebele")
            target_lang: Target language (default: "english")
            
        Returns:
            Translated text
        """
        if not self.model or not self.tokenizer:
            raise RuntimeError("NLLB model not loaded")
        
        # Get NLLB language codes
        src_code = self.language_codes[source_lang]["nllb"]
        tgt_code = self.language_codes[target_lang]["nllb"]
        
        # Tokenize
        self.tokenizer.src_lang = src_code
        inputs = self.tokenizer(text, return_tensors="pt", padding=True)
        
        # Get target language token ID
        # Handle both old and new tokenizer API
        if hasattr(self.tokenizer, 'lang_code_to_id'):
            forced_bos_token_id = self.tokenizer.lang_code_to_id[tgt_code]
        else:
            # Newer API: convert language code to token ID
            forced_bos_token_id = self.tokenizer.convert_tokens_to_ids(tgt_code)
        
        # Generate translation
        translated_tokens = self.model.generate(
            **inputs,
            forced_bos_token_id=forced_bos_token_id,
            max_length=512
        )
        
        # Decode
        translation = self.tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]
        
        return translation
    
    def translate_google(self, text: str, source_lang: str, target_lang: str = "english") -> str:
        """
        Translate using Google Translate API
        
        Args:
            text: Text to translate
            source_lang: Source language (e.g., "shona", "ndebele")
            target_lang: Target language (default: "english")
            
        Returns:
            Translated text
        """
        try:
            from google.cloud import translate_v2 as translate
            
            translate_client = translate.Client(api_key=self.google_api_key)
            
            # Get Google language codes
            src_code = self.language_codes[source_lang]["google"]
            tgt_code = self.language_codes[target_lang]["google"]
            
            # Translate
            result = translate_client.translate(
                text,
                source_language=src_code,
                target_language=tgt_code
            )
            
            return result['translatedText']
            
        except Exception as e:
            print(f"❌ Google Translate error: {e}")
            print("   Falling back to NLLB...")
            return self.translate_nllb(text, source_lang, target_lang)
    
    def translate(self, text: str, source_lang: Optional[str] = None, target_lang: str = "english") -> Tuple[str, str]:
        """
        Translate text to English
        
        Args:
            text: Text to translate
            source_lang: Source language (auto-detect if None)
            target_lang: Target language (default: "english")
            
        Returns:
            Tuple of (translated_text, detected_language)
        """
        # Auto-detect language if not specified
        if source_lang is None:
            source_lang = self.detect_language(text)
            print(f"🔍 Detected language: {self.language_codes[source_lang]['name']}")
        
        # Skip translation if already in target language
        if source_lang == target_lang:
            print(f"✓ Text already in {self.language_codes[target_lang]['name']}")
            return text, source_lang
        
        print(f"🌐 Translating from {self.language_codes[source_lang]['name']} to {self.language_codes[target_lang]['name']}...")
        
        # Translate based on method
        if self.method == "google":
            translated = self.translate_google(text, source_lang, target_lang)
        else:
            translated = self.translate_nllb(text, source_lang, target_lang)
        
        print("✓ Translation complete")
        
        return translated, source_lang
    
    def translate_file(self, input_path: str, output_path: Optional[str] = None, source_lang: Optional[str] = None) -> Dict:
        """
        Translate a transcript file
        
        Args:
            input_path: Path to input file
            output_path: Path to save translated file (optional)
            source_lang: Source language (auto-detect if None)
            
        Returns:
            Dictionary with translation info
        """
        # Read input file
        with open(input_path, "r", encoding="utf-8") as f:
            original_text = f.read()
        
        # Translate
        translated_text, detected_lang = self.translate(original_text, source_lang)
        
        # Save translated file if output path provided
        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(translated_text)
            print(f"✓ Saved translated file: {output_path}")
        
        # Return info
        return {
            "original_text": original_text,
            "translated_text": translated_text,
            "source_language": detected_lang,
            "target_language": "english",
            "translation_method": self.method,
            "input_file": input_path,
            "output_file": output_path
        }


def main():
    """Example usage"""
    print("="*70)
    print("MULTILINGUAL TRANSLATOR - MediScribe")
    print("="*70)
    print("Supports: Shona, Ndebele, Zulu, Xhosa, Afrikaans → English\n")
    
    # Sample medical conversation in Shona
    shona_text = """
    Murwere: John Doe, makore 45, murume. Ndiri kunzwa kurwara musoro uye ndine fivha.
    Tembiricha: 38.6 degrees. BP: 130/85.
    Ndine chikosoro uye ndiri kunzwa kurema mumuviri.
    
    Diagnosis: Mufivha wemukati. 
    Mushonga: Paracetamol 500mg katatu pazuva.
    """
    
    # Sample in Ndebele
    ndebele_text = """
    Isiguli: Sarah Moyo, iminyaka 32, owesifazane.
    Ngilobuhlungu bekhanda futhi nginesiyezi.
    Izinga lokushisa: 37.8 degrees.
    
    Ukuhlolwa: Umkhuhlane.
    Imithi: Ibuprofen 400mg kabili ngosuku.
    """
    
    # Initialize translator (NLLB - offline, free)
    translator = MultilingualTranslator(translation_method="nllb")
    
    print("\n" + "="*70)
    print("TEST 1: Shona → English")
    print("="*70)
    print("\nOriginal (Shona):")
    print(shona_text)
    
    translated_shona, lang = translator.translate(shona_text, source_lang="shona")
    print("\nTranslated (English):")
    print(translated_shona)
    
    print("\n" + "="*70)
    print("TEST 2: Ndebele → English")
    print("="*70)
    print("\nOriginal (Ndebele):")
    print(ndebele_text)
    
    translated_ndebele, lang = translator.translate(ndebele_text, source_lang="ndebele")
    print("\nTranslated (English):")
    print(translated_ndebele)
    
    print("\n" + "="*70)
    print("✓ Translation tests complete!")
    print("="*70)


if __name__ == "__main__":
    main()
