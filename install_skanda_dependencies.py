#!/usr/bin/env python3
"""
Install dependencies for Skanda Purana extraction
Handles system-specific installations and configurations
"""

import subprocess
import sys
import os
import platform
from pathlib import Path

def run_command(command, description=""):
    """Run a system command with progress indication."""
    print(f"🔧 {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print(f"✅ Success: {description}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed: {description}")
        print(f"Error: {e.stderr}")
        return False

def install_python_packages():
    """Install Python packages from requirements."""
    print("📦 Installing Python packages...")
    
    # Upgrade pip first
    run_command(f"{sys.executable} -m pip install --upgrade pip", "Upgrading pip")
    
    # Install packages with break-system-packages flag if needed
    packages = [
        "PyPDF2>=3.0.1",
        "PyMuPDF>=1.23.0", 
        "pytesseract>=0.3.10",
        "Pillow>=9.5.0",
        "indic-transliteration>=2.3.0",
        "pandas>=1.5.0",
        "numpy>=1.24.0",
        "regex>=2023.0.0",
        "tqdm>=4.65.0"
    ]
    
    for package in packages:
        # Try normal install first
        success = run_command(f"{sys.executable} -m pip install {package}", 
                             f"Installing {package}")
        
        # If failed, try with --break-system-packages
        if not success:
            run_command(f"{sys.executable} -m pip install --break-system-packages {package}", 
                       f"Installing {package} (with --break-system-packages)")

def install_tesseract():
    """Install Tesseract OCR based on operating system."""
    system = platform.system().lower()
    
    print(f"🔍 Installing Tesseract OCR for {system}...")
    
    if system == "linux":
        # For Ubuntu/Debian
        commands = [
            "sudo apt-get update",
            "sudo apt-get install -y tesseract-ocr",
            "sudo apt-get install -y tesseract-ocr-san",  # Sanskrit
            "sudo apt-get install -y tesseract-ocr-tam",  # Tamil
            "sudo apt-get install -y tesseract-ocr-eng"   # English
        ]
        
        for cmd in commands:
            run_command(cmd, f"Running: {cmd}")
            
    elif system == "darwin":  # macOS
        commands = [
            "brew install tesseract",
            "brew install tesseract-lang"
        ]
        
        for cmd in commands:
            run_command(cmd, f"Running: {cmd}")
            
    elif system == "windows":
        print("📝 For Windows, please manually install Tesseract:")
        print("   1. Download from: https://github.com/UB-Mannheim/tesseract/wiki")
        print("   2. Install and add to PATH")
        print("   3. Download language packs for Sanskrit (san), Tamil (tam), English (eng)")
        
    else:
        print(f"⚠️  Unknown system: {system}")
        print("Please install Tesseract OCR manually for your system")

def verify_installation():
    """Verify that all dependencies are properly installed."""
    print("\n🔍 Verifying installation...")
    
    # Test Python imports
    test_imports = [
        ("PyPDF2", "PyPDF2"),
        ("PyMuPDF", "fitz"),
        ("Pytesseract", "pytesseract"),
        ("Pillow", "PIL"),
        ("Indic Transliteration", "indic_transliteration"),
        ("Pandas", "pandas"),
        ("NumPy", "numpy"),
        ("Regex", "regex"),
        ("tqdm", "tqdm")
    ]
    
    failed_imports = []
    
    for name, module in test_imports:
        try:
            __import__(module)
            print(f"✅ {name}: OK")
        except ImportError:
            print(f"❌ {name}: FAILED")
            failed_imports.append(name)
    
    # Test Tesseract
    try:
        import pytesseract
        version = pytesseract.get_tesseract_version()
        print(f"✅ Tesseract: OK (version {version})")
    except Exception as e:
        print(f"❌ Tesseract: FAILED - {e}")
        failed_imports.append("Tesseract")
    
    if failed_imports:
        print(f"\n⚠️  Failed imports: {', '.join(failed_imports)}")
        print("Please install missing dependencies manually")
        return False
    else:
        print("\n🎉 All dependencies installed successfully!")
        return True

def create_test_script():
    """Create a simple test script to verify the extraction system."""
    test_script = '''#!/usr/bin/env python3
"""
Test script for Skanda Purana extraction system
"""

def test_dependencies():
    """Test all required dependencies."""
    print("🧪 Testing Skanda Purana extraction dependencies...")
    
    try:
        import PyPDF2
        print("✅ PyPDF2: OK")
        
        import fitz  # PyMuPDF
        print("✅ PyMuPDF: OK")
        
        import pytesseract
        print("✅ Pytesseract: OK")
        
        import PIL
        print("✅ Pillow: OK")
        
        import indic_transliteration
        print("✅ Indic Transliteration: OK")
        
        import pandas
        print("✅ Pandas: OK")
        
        print("\\n🎉 All dependencies working!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_basic_functionality():
    """Test basic extraction functionality."""
    print("\\n🔧 Testing basic functionality...")
    
    # Test Sanskrit pattern matching
    import re
    
    test_text = "श्री गणेशाय नमः। कार्तिकेय स्कन्द सुब्रह्मण्य शंमुख"
    pattern = r'[चशसक][ा-्]*[क-ह]*'
    
    matches = re.findall(pattern, test_text)
    print(f"Sanskrit pattern matches: {matches}")
    
    # Test IAST pattern
    test_iast = "Śrī Gaṇeśāya namaḥ. Kārttikeya Skanda Subrahmanya Śaṅmukha"
    iast_pattern = r'\\b[śŚsScC][aāiīuūeēoō]?\\w*'
    
    iast_matches = re.findall(iast_pattern, test_iast)
    print(f"IAST pattern matches: {iast_matches}")
    
    print("✅ Pattern matching working!")

if __name__ == "__main__":
    print("=" * 60)
    print("🕉️  SKANDA PURANA EXTRACTION - DEPENDENCY TEST")
    print("=" * 60)
    
    if test_dependencies():
        test_basic_functionality()
        print("\\n🎯 Ready to run Skanda Purana extraction!")
    else:
        print("\\n❌ Please fix dependency issues before proceeding")
'''
    
    with open("test_skanda_dependencies.py", "w", encoding='utf-8') as f:
        f.write(test_script)
    
    print("📝 Created test script: test_skanda_dependencies.py")

def main():
    """Main installation process."""
    print("🕉️  SKANDA PURANA EXTRACTION - DEPENDENCY INSTALLER 🕉️")
    print("=" * 70)
    
    print("This script will install all required dependencies for:")
    print("• PDF text extraction from 20 Skanda Purana volumes")
    print("• OCR for scanned pages")
    print("• Sanskrit/Tamil script processing")
    print("• Monier Williams dictionary integration")
    print("• Multi-language pattern matching")
    
    response = input("\nProceed with installation? (y/n): ").lower().strip()
    
    if response != 'y':
        print("Installation cancelled.")
        return
    
    # Step 1: Install Python packages
    install_python_packages()
    
    # Step 2: Install Tesseract OCR
    install_tesseract()
    
    # Step 3: Verify installation
    success = verify_installation()
    
    # Step 4: Create test script
    create_test_script()
    
    print("\n" + "=" * 70)
    if success:
        print("🎉 INSTALLATION COMPLETE!")
        print("\nNext steps:")
        print("1. Run: python test_skanda_dependencies.py")
        print("2. If tests pass, run: python skanda_purana_extractor.py")
        print("3. The extraction will process all 20 PDF volumes")
        print("4. Results will be saved to: skanda_purana_names_extracted.csv")
    else:
        print("⚠️  INSTALLATION INCOMPLETE")
        print("Please resolve the failed dependencies and run again")
    
    print("=" * 70)

if __name__ == "__main__":
    main()