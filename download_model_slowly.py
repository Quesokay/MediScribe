"""
Download NLLB model with better timeout handling and resume capability
This script downloads the model in a more network-friendly way
"""
import os
os.environ['HF_HUB_DOWNLOAD_TIMEOUT'] = '600'  # 10 minutes timeout
os.environ['HF_HUB_ENABLE_HF_TRANSFER'] = '0'  # Disable fast transfer (more stable)

print("="*70)
print("  NLLB MODEL DOWNLOADER")
print("="*70)
print("  This will download ~2.5GB translation model")
print("  The download will resume if interrupted")
print("  Be patient - this may take 10-30 minutes depending on your connection")
print("="*70)
print()

try:
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
    
    model_name = "facebook/nllb-200-distilled-600M"
    
    print("📥 Step 1/2: Downloading tokenizer...")
    print("   (This is small, ~5MB)")
    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        resume_download=True,
        force_download=False
    )
    print("✓ Tokenizer downloaded!\n")
    
    print("📥 Step 2/2: Downloading model...")
    print("   (This is large, ~2.5GB - be patient!)")
    print("   If it fails, just run this script again - it will resume")
    print()
    
    model = AutoModelForSeq2SeqLM.from_pretrained(
        model_name,
        resume_download=True,
        force_download=False
    )
    print("\n✓ Model downloaded!\n")
    
    print("="*70)
    print("✅ SUCCESS! NLLB model is ready to use")
    print("="*70)
    print()
    print("You can now run:")
    print("  python vibe_watcher_multilingual.py")
    print()
    print("The model is cached and won't need to download again!")
    
except KeyboardInterrupt:
    print("\n\n⚠️  Download interrupted by user")
    print("   Run this script again to resume the download")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print()
    print("Troubleshooting:")
    print("  1. Check your internet connection")
    print("  2. Try again during off-peak hours")
    print("  3. Run this script again (it will resume)")
    print("  4. Consider using Google Translate API instead")
    print()
    print("See NETWORK_ISSUES_SOLUTION.md for alternatives")
