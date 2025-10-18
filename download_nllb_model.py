"""
Download NLLB model with retry logic for slow/unstable connections
This script downloads the model in a way that handles timeouts and resumes
"""
import os
import time
from pathlib import Path

def download_with_retries():
    """Download NLLB model with automatic retries"""
    print("="*70)
    print("  NLLB MODEL DOWNLOADER")
    print("="*70)
    print("  Model: facebook/nllb-200-distilled-600M")
    print("  Size: ~2.5GB")
    print("  This will take time with slow internet - be patient!")
    print("="*70)
    print()
    
    # Set longer timeouts
    os.environ['HF_HUB_DOWNLOAD_TIMEOUT'] = '600'  # 10 minutes per file
    
    max_retries = 10
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            print(f"\n{'='*70}")
            print(f"  Attempt {retry_count + 1}/{max_retries}")
            print(f"{'='*70}\n")
            
            from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
            
            model_name = "facebook/nllb-200-distilled-600M"
            
            print("📥 Downloading tokenizer...")
            tokenizer = AutoTokenizer.from_pretrained(
                model_name,
                resume_download=True,  # Resume if interrupted
                force_download=False   # Use cached files if available
            )
            print("✓ Tokenizer downloaded!\n")
            
            print("📥 Downloading model (this is the big one - ~2.5GB)...")
            print("   This may take 30-60 minutes with slow internet")
            print("   The download will resume if interrupted\n")
            
            model = AutoModelForSeq2SeqLM.from_pretrained(
                model_name,
                resume_download=True,
                force_download=False
            )
            print("✓ Model downloaded!\n")
            
            print("="*70)
            print("  ✅ SUCCESS! NLLB model is ready to use")
            print("="*70)
            print("\nYou can now run:")
            print("  python vibe_watcher_multilingual.py")
            print("\nThe model is cached and won't need to download again!")
            return True
            
        except Exception as e:
            retry_count += 1
            print(f"\n❌ Download failed: {e}")
            
            if retry_count < max_retries:
                wait_time = min(60, retry_count * 10)  # Wait longer each retry
                print(f"\n⏳ Waiting {wait_time} seconds before retry...")
                print("   (The download will resume from where it stopped)")
                time.sleep(wait_time)
            else:
                print("\n❌ Max retries reached. Please try again later.")
                print("\nTips:")
                print("  1. Try during off-peak hours (late night)")
                print("  2. Use wired connection instead of WiFi")
                print("  3. Close other internet-using applications")
                print("  4. Try from a location with better internet")
                print("\nOr use Google Translate API instead (see MULTILINGUAL_GUIDE.md)")
                return False
    
    return False


def check_if_downloaded():
    """Check if model is already downloaded"""
    try:
        from transformers import AutoTokenizer
        cache_dir = Path.home() / ".cache" / "huggingface" / "hub"
        
        # Look for the model in cache
        model_dirs = list(cache_dir.glob("models--facebook--nllb-200-distilled-600M"))
        
        if model_dirs:
            print("✓ Model appears to be already downloaded!")
            print(f"  Location: {model_dirs[0]}")
            print("\nTrying to load it...")
            
            tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")
            print("✓ Model loads successfully!")
            print("\nYou can run: python vibe_watcher_multilingual.py")
            return True
    except:
        pass
    
    return False


def main():
    """Main entry point"""
    print("\n" + "="*70)
    print("  NLLB MODEL DOWNLOAD HELPER")
    print("="*70)
    print("  For slow/unstable internet connections")
    print("  Automatically retries on timeout")
    print("="*70)
    print()
    
    # Check if already downloaded
    if check_if_downloaded():
        return
    
    print("\nModel not found in cache. Starting download...\n")
    
    # Confirm before starting
    response = input("This will download ~2.5GB. Continue? (y/n): ")
    if response.lower() != 'y':
        print("Download cancelled.")
        return
    
    # Start download with retries
    success = download_with_retries()
    
    if success:
        print("\n🎉 All done! Your multilingual system is ready!")
    else:
        print("\n😞 Download failed. See tips above or use Google Translate API.")


if __name__ == "__main__":
    main()
