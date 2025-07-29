#!/usr/bin/env python3
"""
Test the Skanda Purana extraction system
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
        
        print("\n🎉 All dependencies working!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_basic_functionality():
    """Test basic extraction functionality."""
    print("\n🔧 Testing basic functionality...")
    
    # Test Sanskrit pattern matching
    import re
    
    test_text = "श्री गणेशाय नमः। कार्तिकेय स्कन्द सुब्रह्मण्य शंमुख"
    pattern = r'[चशसक][ा-्]*[क-ह]*'
    
    matches = re.findall(pattern, test_text)
    print(f"Sanskrit pattern matches: {matches}")
    
    # Test IAST pattern
    test_iast = "Śrī Gaṇeśāya namaḥ. Kārttikeya Skanda Subrahmanya Śaṅmukha"
    iast_pattern = r'\b[śŚsScC][aāiīuūeēoō]?\w*'
    
    iast_matches = re.findall(iast_pattern, test_iast)
    print(f"IAST pattern matches: {iast_matches}")
    
    print("✅ Pattern matching working!")

def test_pdf_access():
    """Test if we can access the PDF files."""
    print("\n📚 Testing PDF access...")
    
    import os
    from pathlib import Path
    
    pdf_folder = Path("Skandha_Purana")
    
    if not pdf_folder.exists():
        print(f"❌ PDF folder not found: {pdf_folder}")
        return False
    
    pdf_files = list(pdf_folder.glob("*.pdf"))
    
    if not pdf_files:
        print(f"❌ No PDF files found in {pdf_folder}")
        return False
    
    print(f"✅ Found {len(pdf_files)} PDF files:")
    for pdf_file in sorted(pdf_files)[:5]:  # Show first 5
        print(f"   - {pdf_file.name}")
    
    if len(pdf_files) > 5:
        print(f"   ... and {len(pdf_files) - 5} more")
    
    return True

def test_single_pdf():
    """Test extraction from a single PDF."""
    print("\n🔍 Testing single PDF extraction...")
    
    try:
        import fitz
        from pathlib import Path
        
        pdf_folder = Path("Skandha_Purana")
        pdf_files = list(pdf_folder.glob("*.pdf"))
        
        if not pdf_files:
            print("❌ No PDF files to test")
            return False
        
        # Test with first PDF
        test_pdf = pdf_files[0]
        print(f"Testing with: {test_pdf.name}")
        
        doc = fitz.open(str(test_pdf))
        
        if len(doc) == 0:
            print("❌ PDF appears to be empty")
            return False
        
        # Extract text from first page
        page = doc.load_page(0)
        text = page.get_text()
        
        print(f"✅ Successfully extracted {len(text)} characters from first page")
        
        if text.strip():
            print("Sample text:")
            print(text[:200] + "..." if len(text) > 200 else text)
        else:
            print("⚠️  First page appears to contain no extractable text (may be image-based)")
        
        doc.close()
        return True
        
    except Exception as e:
        print(f"❌ PDF test failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🕉️  SKANDA PURANA EXTRACTION - SYSTEM TEST") 
    print("=" * 60)
    
    all_tests_passed = True
    
    # Test 1: Dependencies
    if not test_dependencies():
        all_tests_passed = False
    
    # Test 2: Basic functionality
    try:
        test_basic_functionality()
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        all_tests_passed = False
    
    # Test 3: PDF access
    if not test_pdf_access():
        all_tests_passed = False
    
    # Test 4: Single PDF extraction
    if not test_single_pdf():
        all_tests_passed = False
    
    print("\n" + "=" * 60)
    if all_tests_passed:
        print("🎉 ALL TESTS PASSED!")
        print("\n🚀 Ready to run full Skanda Purana extraction:")
        print("   python3 skanda_purana_extractor.py")
    else:
        print("❌ SOME TESTS FAILED")
        print("Please resolve issues before running full extraction")
    print("=" * 60)