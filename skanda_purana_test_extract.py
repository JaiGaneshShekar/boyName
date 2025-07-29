#!/usr/bin/env python3
"""
Test Skanda Purana extraction on first PDF only
To verify the system before running full extraction
"""

import os
import re
import csv
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional, Set

import fitz  # PyMuPDF
from indic_transliteration import sanscript

class SkandaPuranaTestExtractor:
    def __init__(self, pdf_folder: str = "Skandha_Purana"):
        self.pdf_folder = Path(pdf_folder)
        self.extracted_names = []
        
        # Setup logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        
        # Enhanced patterns for better matching
        self.patterns = {
            'devanagari': {
                'cha_ca': r'च[ािीुूेैोौं्]*[क-ह]*[ािीुूेैोौं्]*',
                'sa': r'स[ािीुूेैोौं्]*[क-ह]*[ािीुूेैोौं्]*',
                'sha': r'श[ािीुूेैोौं्]*[क-ह]*[ािीुूेैोौं्]*',
                'se': r'से[क-ह]*[ािीुूेैोौं्]*',
                'che': r'चे[क-ह]*[ािीुूेैोौं्]*',
                'chi': r'चि[क-ह]*[ािीुूेैोौं्]*'
            },
            'roman': {
                'cha_ca': r'\b[Cc][aāhā][a-zA-Zāīūēōṛṝḷḹṃḥṅñṇṭḍśṣ]*',
                'sa': r'\b[Ss][aāhā]?[a-zA-Zāīūēōṛṝḷḹṃḥṅñṇṭḍśṣ]*',
                'sha': r'\b[Ss]h[aāhā][a-zA-Zāīūēōṛṝḷḹṃḥṅñṇṭḍśṣ]*',
                'se': r'\b[Ss]e[a-zA-Zāīūēōṛṝḷḹṃḥṅñṇṭḍśṣ]*',
                'che': r'\b[Cc]he[a-zA-Zāīūēōṛṝḷḹṃḥṅñṇṭḍśṣ]*',
                'chi': r'\b[Cc]hi[a-zA-Zāīūēōṛṝḷḹṃḥṅñṇṭḍśṣ]*'
            }
        }
        
        # Known Skanda-related names for testing
        self.known_names = {
            'skanda', 'karttikeya', 'subrahmanya', 'shanmukha', 'kumara',
            'siva', 'shiva', 'chandrapur', 'saravana', 'ṣaṅmukha'
        }
    
    def detect_script_type(self, text: str) -> str:
        """Detect the script type of the given text."""
        devanagari_count = len(re.findall(r'[\u0900-\u097F]', text))
        total_chars = len([c for c in text if not c.isspace() and c.isalpha()])
        
        if total_chars == 0:
            return 'roman'
        
        if devanagari_count / total_chars > 0.1:
            return 'devanagari'
        else:
            return 'roman'
    
    def extract_text_from_pdf(self, pdf_path: Path, max_pages: int = 10) -> List[Dict]:
        """Extract text from first few pages of PDF."""
        pages_text = []
        
        try:
            doc = fitz.open(str(pdf_path))
            
            total_pages = min(len(doc), max_pages)
            self.logger.info(f"Processing first {total_pages} pages of {pdf_path.name}")
            
            for page_num in range(total_pages):
                page = doc.load_page(page_num)
                text = page.get_text()
                
                if text.strip():
                    pages_text.append({
                        'page_num': page_num + 1,
                        'text': text,
                        'char_count': len(text)
                    })
                
            doc.close()
            
        except Exception as e:
            self.logger.error(f"Error extracting text from {pdf_path}: {e}")
        
        return pages_text
    
    def find_pattern_matches(self, text: str, script_type: str) -> List[Dict]:
        """Find all pattern matches in the given text."""
        matches = []
        
        if script_type not in self.patterns:
            script_type = 'roman'
        
        patterns = self.patterns[script_type]
        
        for pattern_name, pattern in patterns.items():
            try:
                for match in re.finditer(pattern, text, re.IGNORECASE | re.UNICODE):
                    word = match.group(0).strip()
                    
                    # Skip very short matches
                    if len(word) < 2:
                        continue
                    
                    # Skip common particles
                    if word.lower() in ['ca', 'cha', 'sa', 'se']:
                        continue
                    
                    # Check if it's a potential proper noun
                    if self.is_potential_name(word, text, match.start()):
                        matches.append({
                            'word': word,
                            'pattern': pattern_name,
                            'start_pos': match.start(),
                            'end_pos': match.end(),
                            'context': self.extract_context(text, match.start(), match.end()),
                            'is_known': word.lower() in self.known_names
                        })
            except re.error as e:
                self.logger.warning(f"Regex error with pattern {pattern}: {e}")
        
        return matches
    
    def is_potential_name(self, word: str, full_text: str, position: int) -> bool:
        """Simple check if word might be a name."""
        # Skip very common words
        common_words = {'and', 'the', 'of', 'in', 'to', 'a', 'is', 'was', 'are', 'were'}
        if word.lower() in common_words:
            return False
        
        # Proper nouns often start with capital
        if word[0].isupper():
            return True
        
        # Sanskrit/Devanagari words
        if re.search(r'[\u0900-\u097F]', word):
            return True
        
        # Words with IAST diacritics
        if re.search(r'[āīūēōṛṝḷḹṃḥṅñṇṭḍśṣ]', word):
            return True
        
        return len(word) >= 4
    
    def extract_context(self, text: str, start: int, end: int, window: int = 80) -> str:
        """Extract context around a match."""
        context_start = max(0, start - window)
        context_end = min(len(text), end + window)
        
        context = text[context_start:context_end]
        context = re.sub(r'\s+', ' ', context).strip()
        
        return context
    
    def classify_name_type(self, word: str, context: str) -> str:
        """Basic classification of name type."""
        context_lower = context.lower()
        
        if any(x in context_lower for x in ['lord', 'god', 'deity', 'bhagavan']):
            return 'divine_name'
        elif any(x in context_lower for x in ['son', 'daughter', 'child']):
            return 'divine_relation'
        elif any(x in context_lower for x in ['mountain', 'hill', 'temple', 'shrine']):
            return 'sacred_place'
        else:
            return 'proper_noun'
    
    def process_test_pdf(self) -> List[Dict]:
        """Process first PDF for testing."""
        pdf_files = sorted(list(self.pdf_folder.glob("*.pdf")))
        
        if not pdf_files:
            self.logger.error(f"No PDF files found in {self.pdf_folder}")
            return []
        
        # Use first PDF for testing
        test_pdf = pdf_files[0]
        self.logger.info(f"Testing with: {test_pdf.name}")
        
        pages_data = self.extract_text_from_pdf(test_pdf, max_pages=10)
        
        extracted_names = []
        
        for page_data in pages_data:
            page_num = page_data['page_num']
            text = page_data['text']
            
            script_type = self.detect_script_type(text)
            matches = self.find_pattern_matches(text, script_type)
            
            self.logger.info(f"Page {page_num}: {len(matches)} potential matches found")
            
            for match in matches:
                word = match['word']
                name_type = self.classify_name_type(word, match['context'])
                
                extracted_entry = {
                    'Name/Word': word,
                    'Script Type': script_type,
                    'Found Form': word,
                    'Language': 'Sanskrit' if script_type == 'devanagari' else 'Mixed',
                    'Monier Williams Meaning': 'Test extraction - dictionary not integrated',
                    'Etymology': 'N/A',
                    'Page#': f"Page {page_num}",
                    'Part#': "Part 1 (Test)",
                    'Context/Line#': match['context'][:150] + '...' if len(match['context']) > 150 else match['context'],
                    'Proper Noun/Epithet/Place': name_type,
                    'Notes': f"Pattern: {match['pattern']}, Known name: {match['is_known']}"
                }
                
                extracted_names.append(extracted_entry)
                self.extracted_names.append(extracted_entry)
        
        return extracted_names
    
    def export_test_results(self, output_file: str = "skanda_purana_test_extraction.csv") -> None:
        """Export test results to CSV."""
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
        
        self.logger.info(f"Exported {len(self.extracted_names)} test results to {output_file}")
    
    def generate_test_report(self) -> str:
        """Generate a test report."""
        if not self.extracted_names:
            return "No names extracted in test."
        
        total_names = len(self.extracted_names)
        known_names = sum(1 for entry in self.extracted_names if 'True' in entry['Notes'])
        
        script_types = {}
        for entry in self.extracted_names:
            script_type = entry['Script Type']
            script_types[script_type] = script_types.get(script_type, 0) + 1
        
        report = f"""
🧪 SKANDA PURANA TEST EXTRACTION REPORT
{'='*50}

Test Scope: First PDF, first 10 pages
Total Names Found: {total_names}
Known Skanda Names: {known_names}

Script Distribution:
"""
        
        for script, count in script_types.items():
            report += f"  {script}: {count}\n"
        
        report += f"""
Sample Extracted Names:
"""
        
        # Show first 10 names
        for i, entry in enumerate(self.extracted_names[:10]):
            report += f"  {i+1}. {entry['Name/Word']} (Page {entry['Page#']})\n"
        
        if len(self.extracted_names) > 10:
            report += f"  ... and {len(self.extracted_names) - 10} more\n"
        
        return report

def main():
    """Main test extraction function."""
    print("🧪 SKANDA PURANA TEST EXTRACTION")
    print("="*50)
    
    # Initialize test extractor
    extractor = SkandaPuranaTestExtractor()
    
    # Process test PDF
    print("\n📚 Processing first PDF (test mode)...")
    extractor.process_test_pdf()
    
    # Export results
    print("\n💾 Exporting test results...")
    extractor.export_test_results()
    
    # Generate and display report
    report = extractor.generate_test_report()
    print(report)
    
    # Save report
    with open("skanda_test_report.txt", "w", encoding='utf-8') as f:
        f.write(report)
    
    print("\n✅ TEST EXTRACTION COMPLETE!")
    print("📄 Test results: skanda_purana_test_extraction.csv")
    print("📊 Test report: skanda_test_report.txt")
    
    if len(extractor.extracted_names) > 0:
        print(f"\n🎯 Found {len(extractor.extracted_names)} potential names in test run")
        print("Ready to run full extraction on all 20 PDFs!")
    else:
        print("\n⚠️  No names found in test. Check patterns and PDF content.")

if __name__ == "__main__":
    main()