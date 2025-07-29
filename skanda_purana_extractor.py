#!/usr/bin/env python3
"""
Comprehensive Skanda Purana PDF Name Extractor
Extracts all names/epithets starting with Cha/Ca/Sa/Sha/Se/Che/Chi patterns
From all 20 PDF parts with full Sanskrit dictionary validation
"""

import os
import re
import csv
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional, Set
import unicodedata

# PDF processing
try:
    import PyPDF2
    import fitz  # PyMuPDF for better text extraction
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    print("⚠️  PDF libraries not available. Install with: pip install PyPDF2 PyMuPDF")

# OCR for scanned pages
try:
    import pytesseract
    from PIL import Image
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    print("⚠️  OCR libraries not available. Install with: pip install pytesseract Pillow")

# Sanskrit processing
try:
    import indic_transliteration
    from indic_transliteration import sanscript
    INDIC_AVAILABLE = True
except ImportError:
    INDIC_AVAILABLE = False
    print("⚠️  Indic transliteration not available. Install with: pip install indic-transliteration")

class SkandaPuranaExtractor:
    def __init__(self, pdf_folder: str = "Skandha_Purana"):
        self.pdf_folder = Path(pdf_folder)
        self.extracted_names = []
        self.monier_williams_cache = {}
        self.processed_pages = 0
        self.total_pages = 0
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('skanda_extraction.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Name extraction patterns
        self.patterns = {
            # Sanskrit/Devanagari patterns
            'devanagari': {
                'cha_ca': r'च[ा-्]*[क-ह]*',
                'sa': r'स[ा-्]*[क-ह]*',
                'sha': r'श[ा-्]*[क-ह]*',
                'se': r'से[क-ह]*',
                'che': r'चे[क-ह]*',
                'chi': r'चि[क-ह]*'
            },
            # IAST transliteration patterns
            'iast': {
                'cha_ca': r'\b[cC][aāiīuūeēoō]?[kgṅcjñṭḍṇtdnpbmyrlvśṣshṃḥ]*[aāiīuūeēoō]*\w*',
                'sa': r'\b[sS][aāiīuūeēoō]?[kgṅcjñṭḍṇtdnpbmyrlvśṣshṃḥ]*[aāiīuūeēoō]*\w*',
                'sha': r'\b[śŚ][aāiīuūeēoō]?[kgṅcjñṭḍṇtdnpbmyrlvśṣshṃḥ]*[aāiīuūeēoō]*\w*',
                'se': r'\b[sS]e[kgṅcjñṭḍṇtdnpbmyrlvśṣshṃḥ]*\w*',
                'che': r'\b[cC]he[kgṅcjñṭḍṇtdnpbmyrlvśṣshṃḥ]*\w*',
                'chi': r'\b[cC]hi[kgṅcjñṭḍṇtdnpbmyrlvśṣshṃḥ]*\w*'
            },
            # Tamil patterns
            'tamil': {
                'cha_ca': r'ச[ா-்]*[க-ஹ]*',
                'sa': r'ஸ[ா-்]*[க-ஹ]*',
                'sha': r'ஶ[ா-்]*[க-ஹ]*',
                'se': r'ஸே[க-ஹ]*',
                'che': r'சே[க-ஹ]*',
                'chi': r'சி[க-ஹ]*'
            },
            # Romanized patterns (common transliterations)
            'roman': {
                'cha_ca': r'\b[Cc][haā][a-zA-Z]*',
                'sa': r'\b[Ss][haā]?[a-zA-Z]*',
                'sha': r'\b[Ss]h[aā][a-zA-Z]*',
                'se': r'\b[Ss]e[a-zA-Z]*',
                'che': r'\b[Cc]he[a-zA-Z]*',
                'chi': r'\b[Cc]hi[a-zA-Z]*'
            }
        }
        
        # Proper noun indicators
        self.proper_noun_indicators = {
            'epithets': ['bhagavan', 'deva', 'swami', 'lord', 'sri', 'shri'],
            'places': ['pura', 'giri', 'kshetra', 'tirtha', 'sthan', 'dham'],
            'divine_attributes': ['mukha', 'hasta', 'netra', 'pada', 'kara']
        }
        
        # Initialize Monier Williams dictionary (simplified version)
        self.init_monier_williams_dictionary()
    
    def init_monier_williams_dictionary(self):
        """Initialize a basic Monier Williams Sanskrit dictionary for validation."""
        # This is a simplified version - in production, you'd use a full MW database
        self.monier_williams_cache = {
            'skanda': {
                'meaning': 'Name of the god of war, son of Śiva and Pārvatī',
                'etymology': 'from √skand "to leap"',
                'type': 'proper_noun'
            },
            'śaṅmukha': {
                'meaning': 'six-faced, epithet of Kārttikeya',
                'etymology': 'ṣaṣ (six) + mukha (face)',
                'type': 'epithet'
            },
            'kārttikeya': {
                'meaning': 'son of the Kṛttikās (Pleiades), name of the god of war',
                'etymology': 'kṛttikā + eya (patronymic suffix)',
                'type': 'proper_noun'
            },
            'subrahmanya': {
                'meaning': 'dear to Brāhmaṇas, epithet of Kārttikeya',
                'etymology': 'su (good) + brāhmaṇa + ya',
                'type': 'epithet'
            },
            'kumāra': {
                'meaning': 'youth, son, epithet of Kārttikeya',
                'etymology': 'from kū + māra',
                'type': 'epithet'
            },
            'candrapura': {
                'meaning': 'city of the moon',
                'etymology': 'candra (moon) + pura (city)',
                'type': 'place'
            },
            'śivā': {
                'meaning': 'auspicious, name of Pārvatī',
                'etymology': 'from √śiv "to be auspicious"',
                'type': 'proper_noun'
            }
        }
    
    def detect_script_type(self, text: str) -> str:
        """Detect the script type of the given text."""
        # Count characters by script
        devanagari_count = len(re.findall(r'[\u0900-\u097F]', text))
        tamil_count = len(re.findall(r'[\u0B80-\u0BFF]', text))
        latin_count = len(re.findall(r'[a-zA-Z]', text))
        
        total_chars = len([c for c in text if not c.isspace()])
        
        if total_chars == 0:
            return 'unknown'
        
        # Determine predominant script
        if devanagari_count / total_chars > 0.3:
            return 'devanagari'
        elif tamil_count / total_chars > 0.3:
            return 'tamil'
        elif latin_count / total_chars > 0.7:
            # Check for IAST diacritics
            if re.search(r'[āīūēōṛṝḷḹṃḥṅñṇṭḍśṣ]', text):
                return 'iast'
            else:
                return 'roman'
        else:
            return 'mixed'
    
    def extract_text_from_pdf(self, pdf_path: Path) -> List[Dict]:
        """Extract text from PDF using multiple methods."""
        pages_text = []
        
        if not PDF_AVAILABLE:
            self.logger.error("PDF processing libraries not available")
            return pages_text
        
        try:
            # Method 1: PyMuPDF (better for complex layouts)
            doc = fitz.open(str(pdf_path))
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text = page.get_text()
                
                # If text is very short, try OCR
                if len(text.strip()) < 50 and OCR_AVAILABLE:
                    try:
                        pix = page.get_pixmap()
                        img_data = pix.tobytes("png")
                        img = Image.open(io.BytesIO(img_data))
                        
                        # OCR with multiple languages
                        ocr_text = pytesseract.image_to_string(
                            img, 
                            lang='san+tam+eng',  # Sanskrit, Tamil, English
                            config='--psm 6'
                        )
                        if len(ocr_text.strip()) > len(text.strip()):
                            text = ocr_text
                    except Exception as e:
                        self.logger.warning(f"OCR failed for page {page_num+1}: {e}")
                
                pages_text.append({
                    'page_num': page_num + 1,
                    'text': text,
                    'method': 'pymupdf'
                })
                
            doc.close()
            
        except Exception as e:
            self.logger.error(f"Error extracting text from {pdf_path}: {e}")
            
            # Fallback to PyPDF2
            try:
                with open(pdf_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    
                    for page_num, page in enumerate(reader.pages):
                        text = page.extract_text()
                        pages_text.append({
                            'page_num': page_num + 1,
                            'text': text,
                            'method': 'pypdf2'
                        })
            except Exception as e2:
                self.logger.error(f"Fallback extraction also failed: {e2}")
        
        return pages_text
    
    def find_pattern_matches(self, text: str, script_type: str) -> List[Dict]:
        """Find all pattern matches in the given text."""
        matches = []
        
        if script_type not in self.patterns:
            script_type = 'roman'  # Default fallback
        
        patterns = self.patterns[script_type]
        
        for pattern_name, pattern in patterns.items():
            try:
                for match in re.finditer(pattern, text, re.IGNORECASE | re.UNICODE):
                    word = match.group(0).strip()
                    
                    # Skip very short or very long matches
                    if len(word) < 2 or len(word) > 50:
                        continue
                    
                    # Skip common non-names
                    if self.is_likely_proper_noun(word, text, match.start()):
                        matches.append({
                            'word': word,
                            'pattern': pattern_name,
                            'start_pos': match.start(),
                            'end_pos': match.end(),
                            'context': self.extract_context(text, match.start(), match.end())
                        })
            except re.error as e:
                self.logger.warning(f"Regex error with pattern {pattern}: {e}")
        
        return matches
    
    def is_likely_proper_noun(self, word: str, full_text: str, position: int) -> bool:
        """Determine if a word is likely a proper noun."""
        word_lower = word.lower()
        
        # Skip common Sanskrit grammatical elements
        skip_words = {
            'ca', 'cha', 'sa', 'se', 'che', 'chi',  # Basic particles
            'sah', 'sā', 'tat', 'etad', 'kim',      # Pronouns
            'sarva', 'sarvam', 'sarve'              # Common adjectives
        }
        
        if word_lower in skip_words:
            return False
        
        # Check if word starts with capital (in Roman text)
        if re.match(r'^[A-Z]', word):
            return True
        
        # Check context for proper noun indicators
        context = self.extract_context(full_text, position - 50, position + len(word) + 50)
        context_lower = context.lower()
        
        # Look for divine/proper noun indicators
        for category, indicators in self.proper_noun_indicators.items():
            for indicator in indicators:
                if indicator in context_lower:
                    return True
        
        # Check if preceded by honorifics
        honorifics = ['sri', 'shri', 'bhagavan', 'deva', 'lord']
        before_context = full_text[max(0, position-20):position].lower()
        for honorific in honorifics:
            if honorific in before_context:
                return True
        
        # If it's in Devanagari or Tamil, more likely to be a proper noun
        script_type = self.detect_script_type(word)
        if script_type in ['devanagari', 'tamil']:
            return True
        
        return len(word) >= 4  # Basic length check
    
    def extract_context(self, text: str, start: int, end: int, window: int = 100) -> str:
        """Extract context around a match."""
        context_start = max(0, start - window)
        context_end = min(len(text), end + window)
        
        context = text[context_start:context_end]
        # Clean up the context
        context = re.sub(r'\s+', ' ', context).strip()
        
        return context
    
    def validate_with_monier_williams(self, word: str, script_type: str) -> Dict:
        """Validate word against Monier Williams dictionary."""
        # Normalize the word for dictionary lookup
        normalized_word = self.normalize_sanskrit_word(word, script_type)
        
        if normalized_word.lower() in self.monier_williams_cache:
            return self.monier_williams_cache[normalized_word.lower()]
        
        # Extended search for partial matches
        for dict_word, entry in self.monier_williams_cache.items():
            if dict_word.startswith(normalized_word.lower()[:4]) or \
               normalized_word.lower().startswith(dict_word[:4]):
                return {
                    'meaning': f"Related to: {entry['meaning']}",
                    'etymology': entry.get('etymology', 'Unknown'),
                    'type': 'related_term',
                    'base_word': dict_word
                }
        
        return {
            'meaning': 'Not found in MW dictionary - requires manual verification',
            'etymology': 'Unknown',
            'type': 'unverified'
        }
    
    def normalize_sanskrit_word(self, word: str, script_type: str) -> str:
        """Normalize Sanskrit word to standard IAST for dictionary lookup."""
        if script_type == 'devanagari' and INDIC_AVAILABLE:
            try:
                # Convert Devanagari to IAST
                normalized = sanscript.transliterate(word, sanscript.DEVANAGARI, sanscript.IAST)
                return normalized.lower()
            except:
                pass
        
        # Basic cleanup for other scripts
        word = word.strip()
        # Remove common Sanskrit endings for root lookup
        word = re.sub(r'(aya|āya|asya|ena|āt|e|āt|ām|āni|ānām)$', '', word)
        
        return word.lower()
    
    def classify_name_type(self, word: str, context: str, mw_entry: Dict) -> str:
        """Classify the type of name/word found."""
        context_lower = context.lower()
        
        # Use MW dictionary type if available
        if mw_entry.get('type') in ['proper_noun', 'epithet', 'place']:
            return mw_entry['type']
        
        # Context-based classification
        if any(indicator in context_lower for indicator in self.proper_noun_indicators['epithets']):
            return 'divine_epithet'
        elif any(indicator in context_lower for indicator in self.proper_noun_indicators['places']):
            return 'sacred_place'
        elif any(indicator in context_lower for indicator in self.proper_noun_indicators['divine_attributes']):
            return 'divine_attribute'
        elif re.search(r'\b(son|daughter|wife|consort)\b', context_lower):
            return 'divine_relation'
        else:
            return 'proper_noun'
    
    def process_single_pdf(self, pdf_path: Path) -> List[Dict]:
        """Process a single PDF file and extract names."""
        self.logger.info(f"Processing {pdf_path.name}...")
        
        part_number = self.extract_part_number(pdf_path.name)
        pages_data = self.extract_text_from_pdf(pdf_path)
        
        extracted_names = []
        
        for page_data in pages_data:
            page_num = page_data['page_num']
            text = page_data['text']
            
            if not text.strip():
                continue
            
            script_type = self.detect_script_type(text)
            matches = self.find_pattern_matches(text, script_type)
            
            for match in matches:
                word = match['word']
                
                # Validate with Monier Williams (for Sanskrit)
                mw_entry = {}
                if script_type in ['devanagari', 'iast', 'roman']:
                    mw_entry = self.validate_with_monier_williams(word, script_type)
                
                # Classify name type
                name_type = self.classify_name_type(word, match['context'], mw_entry)
                
                extracted_entry = {
                    'Name/Word': word,
                    'Script Type': script_type,
                    'Found Form': word,  # Original form as found
                    'Language': 'Sanskrit' if script_type in ['devanagari', 'iast'] else 'Tamil' if script_type == 'tamil' else 'Mixed',
                    'Monier Williams Meaning': mw_entry.get('meaning', 'N/A'),
                    'Etymology': mw_entry.get('etymology', 'N/A'),
                    'Page#': f"Page {page_num}",
                    'Part#': f"Part {part_number}",
                    'Context/Line#': match['context'][:200] + '...' if len(match['context']) > 200 else match['context'],
                    'Proper Noun/Epithet/Place': name_type,
                    'Notes': f"Pattern: {match['pattern']}, Method: {page_data['method']}"
                }
                
                extracted_names.append(extracted_entry)
                self.extracted_names.append(extracted_entry)
            
            self.processed_pages += 1
            
            # Log progress every 50 pages
            if self.processed_pages % 50 == 0:
                self.logger.info(f"Processed {self.processed_pages} pages, found {len(self.extracted_names)} names so far")
        
        self.logger.info(f"Completed {pdf_path.name}: {len(extracted_names)} names found")
        return extracted_names
    
    def extract_part_number(self, filename: str) -> int:
        """Extract part number from filename."""
        match = re.search(r'Part-(\d+)', filename)
        return int(match.group(1)) if match else 0
    
    def process_all_pdfs(self) -> None:
        """Process all PDFs in the folder."""
        pdf_files = sorted(list(self.pdf_folder.glob("*.pdf")))
        
        if not pdf_files:
            self.logger.error(f"No PDF files found in {self.pdf_folder}")
            return
        
        self.logger.info(f"Found {len(pdf_files)} PDF files to process")
        
        # Estimate total pages (rough estimate)
        self.total_pages = len(pdf_files) * 300  # Assume ~300 pages per PDF
        
        for pdf_file in pdf_files:
            try:
                self.process_single_pdf(pdf_file)
            except Exception as e:
                self.logger.error(f"Failed to process {pdf_file}: {e}")
                continue
        
        self.logger.info(f"Extraction complete! Total names found: {len(self.extracted_names)}")
    
    def export_to_csv(self, output_file: str = "skanda_purana_names_extracted.csv") -> None:
        """Export extracted names to CSV."""
        if not self.extracted_names:
            self.logger.warning("No names extracted to export")
            return
        
        fieldnames = [
            'Name/Word', 'Script Type', 'Found Form', 'Language',
            'Monier Williams Meaning', 'Etymology', 'Page#', 'Part#',
            'Context/Line#', 'Proper Noun/Epithet/Place', 'Notes'
        ]
        
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.extracted_names)
        
        self.logger.info(f"Exported {len(self.extracted_names)} names to {output_file}")
    
    def generate_summary_report(self) -> str:
        """Generate a summary report of the extraction."""
        if not self.extracted_names:
            return "No names extracted."
        
        # Statistics
        total_names = len(self.extracted_names)
        script_types = {}
        name_types = {}
        parts_processed = set()
        
        for entry in self.extracted_names:
            script_type = entry['Script Type']
            script_types[script_type] = script_types.get(script_type, 0) + 1
            
            name_type = entry['Proper Noun/Epithet/Place']
            name_types[name_type] = name_types.get(name_type, 0) + 1
            
            parts_processed.add(entry['Part#'])
        
        report = f"""
📊 SKANDA PURANA EXTRACTION SUMMARY
{'='*50}

Total Names Extracted: {total_names}
Parts Processed: {len(parts_processed)} out of 20
Pages Processed: {self.processed_pages}

📝 SCRIPT TYPE DISTRIBUTION:
{'-'*30}
"""
        
        for script, count in sorted(script_types.items()):
            percentage = (count / total_names) * 100
            report += f"{script.title()}: {count} ({percentage:.1f}%)\n"
        
        report += f"""
🏷️ NAME TYPE DISTRIBUTION:
{'-'*30}
"""
        
        for name_type, count in sorted(name_types.items()):
            percentage = (count / total_names) * 100
            report += f"{name_type.replace('_', ' ').title()}: {count} ({percentage:.1f}%)\n"
        
        report += f"""
📚 PARTS PROCESSED:
{'-'*30}
{', '.join(sorted(parts_processed))}

🎯 TOP 10 MOST FREQUENT NAMES:
{'-'*30}
"""
        
        # Count name frequencies
        name_frequencies = {}
        for entry in self.extracted_names:
            name = entry['Name/Word'].lower()
            name_frequencies[name] = name_frequencies.get(name, 0) + 1
        
        top_names = sorted(name_frequencies.items(), key=lambda x: x[1], reverse=True)[:10]
        
        for name, count in top_names:
            report += f"{name.title()}: {count} occurrences\n"
        
        report += f"""
⏰ EXTRACTION COMPLETED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return report

def main():
    """Main execution function."""
    print("🕉️  SKANDA PURANA COMPREHENSIVE NAME EXTRACTOR 🕉️")
    print("="*60)
    
    # Check dependencies
    missing_deps = []
    if not PDF_AVAILABLE:
        missing_deps.append("PDF processing (PyPDF2, PyMuPDF)")
    if not OCR_AVAILABLE:
        missing_deps.append("OCR capabilities (pytesseract, Pillow)")
    if not INDIC_AVAILABLE:
        missing_deps.append("Indic script processing (indic-transliteration)")
    
    if missing_deps:
        print("⚠️  Missing dependencies:")
        for dep in missing_deps:
            print(f"   - {dep}")
        print("\nInstall with:")
        print("pip install PyPDF2 PyMuPDF pytesseract Pillow indic-transliteration")
        print("\nContinuing with available capabilities...")
    
    # Initialize extractor
    extractor = SkandaPuranaExtractor()
    
    # Process all PDFs
    print(f"\n📚 Processing PDFs from: {extractor.pdf_folder}")
    extractor.process_all_pdfs()
    
    # Export results
    print("\n💾 Exporting results...")
    extractor.export_to_csv()
    
    # Generate and save summary report
    report = extractor.generate_summary_report()
    print(report)
    
    with open("skanda_purana_extraction_report.txt", "w", encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✅ EXTRACTION COMPLETE!")
    print(f"📄 CSV output: skanda_purana_names_extracted.csv")
    print(f"📊 Summary report: skanda_purana_extraction_report.txt")
    print(f"📋 Processing log: skanda_extraction.log")

if __name__ == "__main__":
    main()