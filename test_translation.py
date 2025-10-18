"""
Test translation functionality with sample medical conversations
"""
from translator import MultilingualTranslator
import json


def test_shona_translation():
    """Test Shona to English translation"""
    print("\n" + "="*70)
    print("TEST: Shona Medical Conversation")
    print("="*70)
    
    shona_conversation = """
Chiremba: Mangwanani. Zita renyu ndiani?
Murwere: Zita rangu ndinonzi Tendai Moyo. Ndine makore 35.

Chiremba: Chii chinokutambudzai nhasi?
Murwere: Ndiri kunzwa kurwara musoro kwevhiki yese. Ndine fivha uye ndiri kunzwa kuneta.

Chiremba: Tembiricha yenyu yakaita sei?
Murwere: Yakaita 38.5 degrees manheru ano.

Chiremba: Mune kurwara kwemwoyo here kana chirwere cheShuga?
Murwere: Kwete, handina.

Chiremba: Zvakanaka. Ndinofunga mune mufivha wemukati. Ndichakupai mushonga.

Mushonga: Paracetamol 500mg katatu pazuva kwemazuva manomwe.
Nwirai mvura yakawanda uye muzorore.

Kudzoka: Vhiki inouya kana pasina kuvandudzika.
"""
    
    print("\nOriginal (Shona):")
    print(shona_conversation)
    
    translator = MultilingualTranslator(translation_method="nllb")
    translated, lang = translator.translate(shona_conversation, source_lang="shona")
    
    print("\nTranslated (English):")
    print(translated)
    
    return translated


def test_ndebele_translation():
    """Test Ndebele to English translation"""
    print("\n" + "="*70)
    print("TEST: Ndebele Medical Conversation")
    print("="*70)
    
    ndebele_conversation = """
Udokotela: Sawubona. Ungubani igama lakho?
Isiguli: Igama lami nginguNomsa Dube. Ngineminyaka engu-28.

Udokotela: Yini ekuhluphelayo lamuhla?
Isiguli: Nginobuhlungu besifuba lokukhwehlela okwensuku ezintathu.

Udokotela: Izinga lokushisa lakho linjani?
Isiguli: Lithi 38.2 degrees ekuseni.

Udokotela: Unezinhlungu zomzimba yini?
Isiguli: Yebo, nginezinhlungu emhlane nasemilenzeni.

Udokotela: Kulungile. Ngicabanga ukuthi ulosifo lwamaphaphu.
Ngizokunika imithi.

Imithi: Amoxicillin 500mg kathathu ngosuku okwensuku eziyisikhombisa.
Phuza amanzi amaningi futhi uphumule.

Ukubuya: Ngeviki elizayo uma kungekho ukwehla.
"""
    
    print("\nOriginal (Ndebele):")
    print(ndebele_conversation)
    
    translator = MultilingualTranslator(translation_method="nllb")
    translated, lang = translator.translate(ndebele_conversation, source_lang="ndebele")
    
    print("\nTranslated (English):")
    print(translated)
    
    return translated


def test_auto_detection():
    """Test automatic language detection"""
    print("\n" + "="*70)
    print("TEST: Automatic Language Detection")
    print("="*70)
    
    texts = {
        "Shona": "Ndiri kunzwa kurwara musoro uye ndine fivha.",
        "Ndebele": "Nginobuhlungu bekhanda futhi nginesiyezi.",
        "English": "I have a headache and fever."
    }
    
    translator = MultilingualTranslator(translation_method="nllb")
    
    for expected_lang, text in texts.items():
        print(f"\nText: {text}")
        detected = translator.detect_language(text)
        print(f"Expected: {expected_lang}")
        print(f"Detected: {translator.language_codes[detected]['name']}")


def test_with_mediscribe():
    """Test full pipeline: Translation → Extraction"""
    print("\n" + "="*70)
    print("TEST: Full Pipeline (Translation + Extraction)")
    print("="*70)
    
    from medical_extractor_simple import MedicalExtractor
    
    # Shona medical note
    shona_note = """
Murwere: Rudo Chikwanha, makore 42, mukadzi.
Ari kunzwa kurwara musoro kwevhiki mbiri.
Tembiricha: 37.8 degrees. BP: 125/80.
Ane chikosoro uye ari kunzwa kuneta.

Diagnosis: Migraine headache.
Mushonga: Sumatriptan 50mg panodiwa, maximum maviri pazuva.

Treatment: Zorora munzvimbo yakasviba. Nwa mvura yakawanda.
Follow-up: Vhiki mbiri kana pasina kuvandudzika.
"""
    
    print("\nOriginal (Shona):")
    print(shona_note)
    
    # Translate
    translator = MultilingualTranslator(translation_method="nllb")
    translated, lang = translator.translate(shona_note, source_lang="shona")
    
    print("\nTranslated (English):")
    print(translated)
    
    # Extract medical information
    print("\n" + "-"*70)
    print("Extracting Medical Information...")
    print("-"*70)
    
    extractor = MedicalExtractor()
    result = extractor.extract_from_text(translated)
    
    print("\nExtracted Data:")
    print(json.dumps({
        "patient_name": result.get("patient_name"),
        "age": result.get("age"),
        "gender": result.get("gender"),
        "symptoms": [s["text"] for s in result.get("symptoms", [])],
        "diagnosis": [d["text"] for d in result.get("diagnosis", [])],
        "medications": [m["text"] for m in result.get("medications", [])],
        "vital_signs": [v["text"] for v in result.get("vital_signs", [])]
    }, indent=2))


def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("  MULTILINGUAL TRANSLATION TESTS")
    print("="*70)
    print("  Testing Shona and Ndebele → English translation")
    print("  Using NLLB (No Language Left Behind) by Meta")
    print("="*70)
    
    try:
        # Test individual translations
        test_shona_translation()
        test_ndebele_translation()
        
        # Test auto-detection
        test_auto_detection()
        
        # Test full pipeline
        test_with_mediscribe()
        
        print("\n" + "="*70)
        print("✅ All tests completed successfully!")
        print("="*70)
        print("\nNext steps:")
        print("1. Run: python vibe_watcher_multilingual.py")
        print("2. Patients can speak in Shona, Ndebele, or English")
        print("3. MediScribe will translate and extract automatically")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        print("\nMake sure you have installed:")
        print("  pip install transformers torch")


if __name__ == "__main__":
    main()
