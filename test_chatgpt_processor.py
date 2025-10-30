"""
Test the ChatGPT Voice Mode Processor
"""
from realtime_chatgpt_processor import ChatGPTVoiceProcessor


def test_english_conversation():
    """Test with English conversation"""
    print("\n" + "="*70)
    print("TEST 1: English Medical Conversation")
    print("="*70)
    
    conversation = """
    Doctor: Good morning! What's your name and age?
    
    Patient: Hi doctor. I'm Michael Chen, I'm 35 years old, male.
    
    Doctor: What brings you in today, Michael?
    
    Patient: I've been having severe chest pain for the past 2 days. 
    It gets worse when I breathe deeply or cough.
    
    Doctor: I see. Let me check your vitals. Your blood pressure is 140/90, 
    which is a bit elevated. Temperature is 99.2 Fahrenheit. Heart rate is 88 bpm.
    Any other symptoms?
    
    Patient: Yes, I have a persistent cough and some shortness of breath.
    
    Doctor: Have you had any recent injuries or trauma to your chest?
    
    Patient: No, nothing like that.
    
    Doctor: Based on your symptoms, I'm concerned about possible pleurisy or 
    a respiratory infection. I'm going to order a chest X-ray and some blood tests.
    In the meantime, I'll prescribe you Ibuprofen 600mg three times daily for the pain,
    and an antibiotic - Azithromycin 500mg once daily for 5 days.
    
    Patient: Should I be worried?
    
    Doctor: Let's wait for the test results. If the pain gets worse or you have 
    difficulty breathing, go to the emergency room immediately. Otherwise, 
    follow up with me in 3 days with your test results.
    
    Patient: Okay, thank you doctor.
    
    Doctor: Take care, Michael.
    """
    
    processor = ChatGPTVoiceProcessor(use_translation=False)
    result = processor.process_conversation(conversation, auto_save=True)
    
    return result


def test_multilingual_conversation():
    """Test with Shona conversation"""
    print("\n" + "="*70)
    print("TEST 2: Shona Medical Conversation (with translation)")
    print("="*70)
    
    shona_conversation = """
    Chiremba: Mangwanani. Zita renyu ndiani uye makore mangani?
    
    Murwere: Mangwanani chiremba. Ndini Tendai Moyo, ndine makore 42, murume.
    
    Chiremba: Muri kunzwa sei nhasi?
    
    Murwere: Ndiri kunzwa kurwara musoro zvikuru uye ndine fivha kubva mazuva matatu apfuura.
    Ndiri kunzwa kutonhora uye kurema mumuviri.
    
    Chiremba: Ndinzwa. Regai ndikuenzei. Tembiricha yenyu iri pa 39.2 degrees Celsius.
    BP yenyu iri pa 135/88. Mune mamwe matambudziko here?
    
    Murwere: Hongu, ndine chikosoro chakaoma uye ndiri kunzwa kurwara pahuro.
    
    Chiremba: Makambobatwa nemukutu here kana kuti mune allergies?
    
    Murwere: Kwete, handina.
    
    Chiremba: Zvakanaka. Ndinoona kuti mune chirwere chemukati, pamwe influenza.
    Ndichakupai mishonga - Paracetamol 500mg katatu pazuva kuti fivha idzike,
    uye Amoxicillin 500mg katatu pazuva kwemazuva manomwe kurwisa hutachiona.
    
    Murwere: Ndingadzokerazve here?
    
    Chiremba: Hongu, kana matambudziko asingapere mumazuva mana kana mashanu,
    dzokai muzondiona. Zororerai uye munwe mvura yakawanda.
    
    Murwere: Ndatenda chiremba.
    
    Chiremba: Zvakanaka. Porai zvakanaka.
    """
    
    processor = ChatGPTVoiceProcessor(use_translation=True)
    result = processor.process_conversation(shona_conversation, auto_save=True)
    
    return result


def test_group_conversation():
    """Test with multi-person conversation"""
    print("\n" + "="*70)
    print("TEST 3: Group Medical Consultation")
    print("="*70)
    
    group_conversation = """
    Doctor: Good afternoon. I have the patient here with their family. 
    Can you introduce yourselves?
    
    Patient: I'm Lisa Martinez, 52 years old, female.
    
    Daughter: I'm her daughter, Maria. I brought her in because she's been 
    having memory problems.
    
    Doctor: Thank you for coming. Lisa, can you tell me what's been happening?
    
    Patient: Well, I've been forgetting things a lot lately. Where I put my keys,
    appointments, even conversations I had yesterday.
    
    Daughter: It's been getting worse over the past 6 months. She also seems 
    confused sometimes and has trouble finding words.
    
    Doctor: I see. Lisa, do you have any headaches, dizziness, or vision problems?
    
    Patient: Sometimes I get headaches, yes. And I feel dizzy when I stand up quickly.
    
    Doctor: Let me check your blood pressure. It's 150/95, which is high. 
    Have you been taking any medications?
    
    Patient: Just my blood pressure medication, but I forget to take it sometimes.
    
    Daughter: That's part of the problem - she forgets her medications.
    
    Doctor: I understand. Based on what you're telling me, we need to do some tests.
    I'm going to order a cognitive assessment, brain MRI, and blood work to check 
    for vitamin deficiencies and thyroid function. These memory issues could be 
    related to several things - medication management, high blood pressure affecting 
    the brain, or early signs of cognitive decline.
    
    For now, I'm going to adjust your blood pressure medication to Amlodipine 10mg 
    once daily. Maria, can you help make sure she takes it every morning?
    
    Daughter: Yes, of course.
    
    Doctor: Good. I'm also prescribing a vitamin B12 supplement. Let's schedule 
    a follow-up in two weeks after we get the test results.
    
    Patient: Will I be okay?
    
    Doctor: We'll figure this out together. The tests will help us understand 
    what's causing these symptoms and how best to treat them.
    
    Daughter: Thank you, doctor.
    
    Doctor: You're welcome. Take care, both of you.
    """
    
    processor = ChatGPTVoiceProcessor(use_translation=False)
    result = processor.process_conversation(group_conversation, auto_save=True)
    
    return result


def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("  __  __          _ _ ____            _ _          ")
    print(" |  \\/  | ___  __| (_) ___|  ___ _ __(_) |__   ___ ")
    print(" | |\\/| |/ _ \\/ _` | \\___ \\ / __| '__| | '_ \\ / _ \\")
    print(" | |  | |  __/ (_| | |___) | (__| |  | | |_) |  __/")
    print(" |_|  |_|\\___|\\__,_|_|____/ \\___|_|  |_|_.__/ \\___|")
    print("\n ChatGPT Voice Mode Processor - Test Suite")
    print("="*70)
    
    # Run tests
    test_english_conversation()
    
    # Uncomment to test multilingual (requires NLLB model)
    # test_multilingual_conversation()
    
    test_group_conversation()
    
    print("\n" + "="*70)
    print("✓ ALL TESTS COMPLETE")
    print("="*70)
    print("\nCheck your database for the saved records:")
    print("  python show_records.py")


if __name__ == "__main__":
    main()
