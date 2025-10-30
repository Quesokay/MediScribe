"""
Verify Vibe-MediScribe Integration Setup
Checks all dependencies and configuration
"""
import sys
import json
from pathlib import Path


def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)


def check_python_version():
    """Check Python version"""
    print("\n🐍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"   ✓ Python {version.major}.{version.minor}.{version.micro} (OK)")
        return True
    else:
        print(f"   ✗ Python {version.major}.{version.minor}.{version.micro} (Need 3.7+)")
        return False


def check_dependencies():
    """Check required Python packages"""
    print("\n📦 Checking dependencies...")
    
    required = {
        'spacy': 'spaCy',
        'watchdog': 'Watchdog',
        'json': 'JSON (built-in)',
        'pathlib': 'Pathlib (built-in)'
    }
    
    all_ok = True
    for module, name in required.items():
        try:
            __import__(module)
            print(f"   ✓ {name}")
        except ImportError:
            print(f"   ✗ {name} (Missing)")
            all_ok = False
    
    # Check spaCy model
    try:
        import spacy
        try:
            nlp = spacy.load("en_core_web_sm")
            print(f"   ✓ spaCy model: en_core_web_sm")
        except:
            print(f"   ✗ spaCy model: en_core_web_sm (Missing)")
            print(f"      Run: python -m spacy download en_core_web_sm")
            all_ok = False
    except:
        pass
    
    return all_ok


def check_config():
    """Check configuration file"""
    print("\n⚙️  Checking configuration...")
    
    config_path = Path("vibe_config.json")
    if not config_path.exists():
        print(f"   ⚠️  vibe_config.json not found")
        print(f"      Will be created on first run")
        return True
    
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
        
        print(f"   ✓ Configuration file exists")
        
        # Check watch directory
        watch_dir = Path(config.get('watch_directory', ''))
        if watch_dir.exists():
            print(f"   ✓ Watch directory exists: {watch_dir}")
        else:
            print(f"   ⚠️  Watch directory doesn't exist: {watch_dir}")
            print(f"      Will be created on first run")
        
        # Check file extensions
        extensions = config.get('file_extensions', [])
        print(f"   ✓ Monitoring: {', '.join(extensions)}")
        
        return True
        
    except Exception as e:
        print(f"   ✗ Error reading config: {e}")
        return False


def check_core_files():
    """Check if core MediScribe files exist"""
    print("\n📄 Checking core files...")
    
    required_files = [
        'medical_extractor_simple.py',
        'database_saver.py',
        'vibe_watcher.py',
        'batch_process.py',
        'view_database.py'
    ]
    
    all_ok = True
    for file in required_files:
        if Path(file).exists():
            print(f"   ✓ {file}")
        else:
            print(f"   ✗ {file} (Missing)")
            all_ok = False
    
    return all_ok


def check_vibe_installation():
    """Check if Vibe is installed (optional)"""
    print("\n🎙️  Checking Vibe installation...")
    
    # Common Vibe installation paths
    possible_paths = [
        Path.home() / "AppData" / "Local" / "Programs" / "Vibe",
        Path("C:/Program Files/Vibe"),
        Path("C:/Program Files (x86)/Vibe"),
    ]
    
    vibe_found = False
    for path in possible_paths:
        if path.exists():
            print(f"   ✓ Vibe found at: {path}")
            vibe_found = True
            break
    
    if not vibe_found:
        print(f"   ℹ️  Vibe not found in common locations")
        print(f"      Download from: https://thewh1teagle.github.io/vibe/")
    
    return True  # Not critical


def provide_next_steps(all_checks_passed):
    """Provide next steps based on verification results"""
    print_header("NEXT STEPS")
    
    if all_checks_passed:
        print("\n✅ All checks passed! You're ready to go.\n")
        print("To start the integration:")
        print("  1. Configure Vibe to save transcripts to your watch directory")
        print("  2. Run: python vibe_watcher.py")
        print("  3. Or use: start_vibe_integration.bat\n")
        print("To test:")
        print("  python test_vibe_integration.py\n")
        print("For help:")
        print("  See VIBE_QUICK_SETUP.md or VIBE_INTEGRATION.md")
    else:
        print("\n⚠️  Some issues need attention.\n")
        print("To install missing dependencies:")
        print("  pip install -r requirements.txt")
        print("  python -m spacy download en_core_web_sm\n")
        print("Then run this script again to verify.")


def main():
    """Main verification routine"""
    print_header("VIBE-MEDISCRIBE SETUP VERIFICATION")
    
    checks = [
        check_python_version(),
        check_dependencies(),
        check_config(),
        check_core_files(),
        check_vibe_installation()
    ]
    
    all_passed = all(checks)
    provide_next_steps(all_passed)
    
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()
