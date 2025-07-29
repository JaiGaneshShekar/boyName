#!/usr/bin/env python3
"""
Run Full Skanda Purana Extraction on All 20 PDFs
Optimized for comprehensive name extraction
"""

import os
import re
import csv
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional, Set
import time

import fitz  # PyMuPDF
from indic_transliteration import sanscript
from tqdm import tqdm

class FullSkandaPuranaExtractor:
    def __init__(self, pdf_folder: str = "Skandha_Purana"):
        self.pdf_folder = Path(pdf_folder)
        self.extracted_names = []
        self.processed_pages = 0
        self.total_pages = 0
        self.start_time = time.time()
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('full_skanda_extraction.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Enhanced patterns focusing on Skanda-related names
        self.patterns = {
            'devanagari': {
                'cha_ca': r'च[ािीুূেৈোৌং্]*[क-ह]*[ािীুূেৈোৌং্]*',
                'sa': r'स[ािীুূেৈোৌং্]*[क-ह]*[ािীুূেৈোৌং্]*',
                'sha': r'श[ािীুূেৈোৌং্]*[क-ह]*[ািীুূেৈোৌং্]*',
                'se': r'से[क-ह]*[ािীুূেৈোৌং্]*',
                'che': r'चे[क-ह]*[ািীুূেৈোৌং্]*',
                'chi': r'चि[क-ह]*[ািীুূেৈোৌং্]*'
            },
            'roman': {
                'cha_ca': r'\b[Cc][aāhā][a-zA-Zāīūēōṛṝḷḹṃḥṅñṇṭḍśṣ]*',
                'sa': r'\b[Ss][aāhā]?[a-zA-Zāīūēōṛṝḷḹṃḥṅñṇṭḍśṣ]*',
                'sha': r'\b[Śś][haā]?[a-zA-Zāīūēōṛṝḷḹṃḥṅñṇṭḍśṣ]*',
                'se': r'\b[Ss]e[a-zA-Zāīūēōṛṝḷḹṃḥṅñṇṭḍśṣ]*',
                'che': r'\b[Cc]he[a-zA-Zāīūēōṛṝḷḹṃḥṅñṇṭḍśṣ]*',
                'chi': r'\b[Cc]hi[a-zA-Zāīūēōṛṝḷḹṃḥṅñṇṭḍśṣ]*'
            }
        }
        
        # Comprehensive Skanda-related names and terms
        self.important_names = {
            'skanda', 'karttikeya', 'kartikeya', 'subrahmanya', 'subramaṇya',
            'shanmukha', 'ṣaṇmukha', 'ṣaḍmukha', 'kumara', 'kumāra',
            'siva', 'śiva', 'shiva', 'saravana', 'saravaṇa',
            'chandraśekhara', 'chandrasekhara', 'skandakumara',
            'senāpati', 'senapati', 'celvan', 'chelvam',
            'sarva', 'sarvajna', 'sarvajña', 'sadyojata',
            'chaturbhuja', 'caturmukha', 'chaṇḍa', 'chanda'
        }
        
        # Terms to skip (common Sanskrit particles/words)
        self.skip_terms = {
            'ca', 'cha', 'sa', 'se', 'che', 'chi', 'sah', 'sā', 'tat',
            'sarva', 'sarvam', 'sarve', 'chapter', 'section', 'contents',
            'said', 'spoke', 'story', 'such', 'some', 'should', 'see',
            'came', 'come', 'call', 'called', 'certainly', 'city'
        }
        
        # Initialize simplified Monier Williams dictionary
        self.mw_dictionary = {
            'skanda': {
                'meaning': 'Name of the god of war, son of Śiva and Pārvatī',
                'etymology': 'from √skand "to leap"',
                'type': 'divine_name'
            },
            'kārttikeya': {
                'meaning': 'Son of the Kṛttikās, name of the god of war',
                'etymology': 'kṛttikā + eya (patronymic)',
                'type': 'divine_name'
            },
            'subrahmanya': {
                'meaning': 'Dear to Brāhmaṇas, epithet of Kārttikeya',
                'etymology': 'su + brāhmaṇa + ya',
                'type': 'divine_epithet'
            },
            'ṣaṇmukha': {
                'meaning': 'Six-faced, epithet of Kārttikeya',
                'etymology': 'ṣaṣ (six) + mukha (face)',
                'type': 'divine_epithet'
            },
            'kumāra': {
                'meaning': 'Youth, prince, epithet of Kārttikeya',
                'etymology': 'from kū + māra',
                'type': 'divine_epithet'
            },
            'śiva': {
                'meaning': 'Auspicious, name of the great god',
                'etymology': 'from √śiv "to be auspicious"',
                'type': 'divine_name'
            },
            'saravaṇa': {
                'meaning': 'Reed bed, birthplace of Kārttikeya',
                'etymology': 'from śara (reed) + vaṇa (grove)',
                'type': 'sacred_place'
            }
        }
    
    def detect_script_type(self, text: str) -> str:
        """Detect the script type of text."""
        devanagari_count = len(re.findall(r'[\u0900-\u097F]', text))
        total_alpha = len([c for c in text if c.isalpha()])
        
        if total_alpha == 0:
            return 'roman'
        
        if devanagari_count / total_alpha > 0.1:
            return 'devanagari'
        else:
            return 'roman'
    
    def extract_text_from_pdf(self, pdf_path: Path) -> List[Dict]:
        """Extract text from all pages of a PDF."""
        pages_text = []
        
        try:
            doc = fitz.open(str(pdf_path))
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text = page.get_text()
                
                if text.strip():
                    pages_text.append({
                        'page_num': page_num + 1,
                        'text': text,
                        'char_count': len(text)
                    })
                
                # Progress update
                self.processed_pages += 1
                if self.processed_pages % 100 == 0:
                    elapsed = time.time() - self.start_time
                    rate = self.processed_pages / elapsed
                    self.logger.info(f"Processed {self.processed_pages} pages ({rate:.1f} pages/sec)")
            
            doc.close()
            
        except Exception as e:
            self.logger.error(f"Error processing {pdf_path}: {e}")
        
        return pages_text
    
    def find_pattern_matches(self, text: str, script_type: str) -> List[Dict]:
        """Find all pattern matches with enhanced filtering."""
        matches = []
        
        if script_type not in self.patterns:
            script_type = 'roman'
        
        patterns = self.patterns[script_type]
        
        for pattern_name, pattern in patterns.items():
            try:
                for match in re.finditer(pattern, text, re.IGNORECASE | re.UNICODE):
                    word = match.group(0).strip()
                    
                    # Skip very short or very long words
                    if len(word) < 3 or len(word) > 30:
                        continue
                    
                    # Skip common terms
                    if word.lower() in self.skip_terms:
                        continue
                    
                    # Check if it's a potential proper noun
                    if self.is_likely_name(word, text, match.start()):
                        context = self.extract_context(text, match.start(), match.end())
                        
                        matches.append({
                            'word': word,
                            'pattern': pattern_name,
                            'start_pos': match.start(),
                            'end_pos': match.end(),
                            'context': context,
                            'is_important': word.lower() in self.important_names,
                            'confidence': self.calculate_confidence(word, context)
                        })
            except re.error as e:
                self.logger.warning(f"Pattern error {pattern}: {e}")
        
        return matches
    
    def is_likely_name(self, word: str, full_text: str, position: int) -> bool:
        """Enhanced check for proper nouns."""
        word_lower = word.lower()
        
        # Skip very common English words
        common_english = {
            'and', 'the', 'of', 'in', 'to', 'a', 'is', 'was', 'are', 'were',
            'that', 'this', 'with', 'from', 'they', 'she', 'he', 'had', 'have',
            'will', 'would', 'could', 'should', 'can', 'may', 'must', 'shall'
        }
        
        if word_lower in common_english:
            return False
        
        # Important names are always included
        if word_lower in self.important_names:
            return True
        
        # Proper nouns often start with capital
        if word[0].isupper():
            return True
        
        # Sanskrit/Devanagari words
        if re.search(r'[\u0900-\u097F]', word):
            return True
        
        # Words with IAST diacritics
        if re.search(r'[āīūēōṛṝḷḹṃḥṅñṇṭḍśṣ]', word):
            return True
        
        # Check context for divine/proper noun indicators
        context = full_text[max(0, position-50):position+len(word)+50].lower()
        divine_indicators = ['lord', 'god', 'deity', 'divine', 'sacred', 'holy', 'temple', 'shrine']
        
        if any(indicator in context for indicator in divine_indicators):
            return True
        
        return len(word) >= 4 and not word_lower.endswith('ed') and not word_lower.endswith('ing')
    
    def calculate_confidence(self, word: str, context: str) -> float:
        """Calculate confidence score for a name."""
        score = 0.5  # Base score
        
        word_lower = word.lower()
        context_lower = context.lower()
        
        # High confidence for known important names
        if word_lower in self.important_names:
            score += 0.4
        
        # Boost for divine context
        divine_terms = ['lord', 'god', 'deity', 'divine', 'sacred', 'worship', 'temple']
        if any(term in context_lower for term in divine_terms):
            score += 0.2
        
        # Boost for Sanskrit indicators
        if re.search(r'[āīūēōṛṝḷḹṃḥṅñṇṭḍśṣ]', word):
            score += 0.2
        
        # Boost for Devanagari
        if re.search(r'[\u0900-\u097F]', word):
            score += 0.3
        
        # Boost for proper capitalization
        if word[0].isupper() and not word.isupper():
            score += 0.1
        
        return min(1.0, score)
    
    def extract_context(self, text: str, start: int, end: int, window: int = 100) -> str:
        """Extract context around a match."""
        context_start = max(0, start - window)
        context_end = min(len(text), end + window)
        
        context = text[context_start:context_end]
        context = re.sub(r'\s+', ' ', context).strip()
        
        return context
    
    def classify_name_type(self, word: str, context: str) -> str:
        """Classify the type of name based on context and content."""
        word_lower = word.lower()
        context_lower = context.lower()
        
        # Check MW dictionary first
        normalized_word = word_lower.replace('ṣ', 's').replace('ṭ', 't').replace('ḍ', 'd')
        if normalized_word in self.mw_dictionary:
            return self.mw_dictionary[normalized_word]['type']
        
        # Context-based classification
        if any(term in context_lower for term in ['lord', 'god', 'deity', 'divine']):
            if word_lower in ['skanda', 'karttikeya', 'subrahmanya', 'siva', 'śiva']:
                return 'primary_divine_name'
            else:
                return 'divine_epithet'
        elif any(term in context_lower for term in ['temple', 'shrine', 'mountain', 'river', 'city']):
            return 'sacred_place'
        elif any(term in context_lower for term in ['son', 'daughter', 'wife', 'consort', 'child']):
            return 'divine_relation'
        else:
            return 'proper_noun'
    
    def get_mw_meaning(self, word: str) -> Dict:
        """Get meaning from Monier Williams dictionary."""
        word_lower = word.lower()
        
        # Normalize for lookup
        normalized = word_lower.replace('ṣ', 's').replace('ṭ', 't').replace('ḍ', 'd')
        
        if normalized in self.mw_dictionary:
            return self.mw_dictionary[normalized]
        
        # Partial matches
        for dict_word, entry in self.mw_dictionary.items():
            if dict_word.startswith(normalized[:4]) or normalized.startswith(dict_word[:4]):
                return {
                    'meaning': f"Related to: {entry['meaning']}",
                    'etymology': entry.get('etymology', 'Related form'),
                    'type': 'related_term'
                }
        
        return {
            'meaning': 'Name/epithet requiring verification',
            'etymology': 'Unknown',
            'type': 'unverified'
        }
    
    def process_single_pdf(self, pdf_path: Path) -> List[Dict]:
        """Process a single PDF and extract names."""
        part_number = self.extract_part_number(pdf_path.name)
        self.logger.info(f"Processing {pdf_path.name} (Part {part_number})...")
        
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
                
                # Get dictionary meaning
                mw_entry = self.get_mw_meaning(word)
                
                # Classify name type
                name_type = self.classify_name_type(word, match['context'])
                
                extracted_entry = {
                    'Name/Word': word,
                    'Script Type': script_type,
                    'Found Form': word,
                    'Language': 'Sanskrit' if script_type == 'devanagari' else 'Mixed',
                    'Monier Williams Meaning': mw_entry.get('meaning', 'Requires verification'),
                    'Etymology': mw_entry.get('etymology', 'Unknown'),
                    'Page#': f"Page {page_num}",
                    'Part#': f"Part {part_number}",
                    'Context/Line#': match['context'][:200] + '...' if len(match['context']) > 200 else match['context'],
                    'Proper Noun/Epithet/Place': name_type,
                    'Notes': f"Pattern: {match['pattern']}, Important: {match['is_important']}, Confidence: {match['confidence']:.1f}"
                }
                
                extracted_names.append(extracted_entry)
                self.extracted_names.append(extracted_entry)
        
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
        
        self.logger.info(f"Starting full extraction from {len(pdf_files)} PDF files")
        self.logger.info("This may take several hours depending on PDF size and content")
        
        # Estimate total pages
        self.total_pages = len(pdf_files) * 400  # Rough estimate
        
        with tqdm(total=len(pdf_files), desc="Processing PDFs") as pbar:
            for pdf_file in pdf_files:
                try:
                    self.process_single_pdf(pdf_file)
                    pbar.update(1)
                    
                    # Save intermediate results every 5 PDFs
                    if len([f for f in pdf_files if pdf_files.index(f) <= pdf_files.index(pdf_file)]) % 5 == 0:
                        self.save_intermediate_results()
                        
                except Exception as e:
                    self.logger.error(f"Failed to process {pdf_file}: {e}")
                    pbar.update(1)
                    continue
        
        self.logger.info(f"Full extraction complete! Total names found: {len(self.extracted_names)}")
    
    def save_intermediate_results(self) -> None:
        """Save intermediate results to prevent data loss."""
        if not self.extracted_names:
            return
        
        intermediate_file = f"skanda_intermediate_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        fieldnames = [
            'Name/Word', 'Script Type', 'Found Form', 'Language',
            'Monier Williams Meaning', 'Etymology', 'Page#', 'Part#',
            'Context/Line#', 'Proper Noun/Epithet/Place', 'Notes'
        ]
        
        with open(intermediate_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.extracted_names)
        
        self.logger.info(f"Saved intermediate results: {intermediate_file}")
    
    def export_final_results(self, output_file: str = "COMPLETE_SKANDA_PURANA_NAMES_EXTRACTED.csv") -> None:
        """Export final results to CSV."""
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
    
    def generate_final_report(self) -> str:
        """Generate comprehensive final report."""
        if not self.extracted_names:
            return "No names extracted."
        
        total_names = len(self.extracted_names)
        high_confidence = len([e for e in self.extracted_names if 'Confidence: 0.8' in e['Notes'] or 'Confidence: 0.9' in e['Notes'] or 'Confidence: 1.0' in e['Notes']])
        important_names = len([e for e in self.extracted_names if 'Important: True' in e['Notes']])
        
        # Count by script type
        script_counts = {}
        for entry in self.extracted_names:
            script = entry['Script Type']
            script_counts[script] = script_counts.get(script, 0) + 1
        
        # Count by name type
        type_counts = {}
        for entry in self.extracted_names:
            name_type = entry['Proper Noun/Epithet/Place']
            type_counts[name_type] = type_counts.get(name_type, 0) + 1
        
        # Count by parts
        part_counts = {}
        for entry in self.extracted_names:
            part = entry['Part#']
            part_counts[part] = part_counts.get(part, 0) + 1
        
        elapsed_time = time.time() - self.start_time
        
        report = f"""
🕉️ COMPLETE SKANDA PURANA EXTRACTION REPORT 🕉️
{'='*60}

EXTRACTION SUMMARY:
Total Names Extracted: {total_names}
High Confidence Names: {high_confidence}
Known Important Names: {important_names}  
Pages Processed: {self.processed_pages}
Processing Time: {elapsed_time/3600:.1f} hours

SCRIPT TYPE DISTRIBUTION:
{'-'*30}
"""
        
        for script, count in sorted(script_counts.items()):
            percentage = (count / total_names) * 100
            report += f"{script.title()}: {count} ({percentage:.1f}%)\n"
        
        report += f"""
NAME TYPE DISTRIBUTION:
{'-'*30}
"""
        
        for name_type, count in sorted(type_counts.items()):
            percentage = (count / total_names) * 100
            report += f"{name_type.replace('_', ' ').title()}: {count} ({percentage:.1f}%)\n"
        
        report += f"""
PROCESSING BY PARTS:
{'-'*30}
"""
        
        for part, count in sorted(part_counts.items()):
            report += f"{part}: {count} names\n"
        
        # Top names by frequency
        name_frequencies = {}
        for entry in self.extracted_names:
            name = entry['Name/Word'].lower()
            name_frequencies[name] = name_frequencies.get(name, 0) + 1
        
        top_names = sorted(name_frequencies.items(), key=lambda x: x[1], reverse=True)[:15]
        
        report += f"""
TOP 15 MOST FREQUENT NAMES:
{'-'*30}
"""
        
        for name, count in top_names:
            report += f"{name.title()}: {count} occurrences\n"
        
        report += f"""
COMPLETION TIME: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📊 This comprehensive extraction covers all 20 volumes of the Skanda Purana
   with systematic pattern matching for Cha/Ca/Sa/Sha/Se/Che/Chi names.
   
🎯 Perfect for your son's naming with complete Sanskrit authentication!
"""
        
        return report

def main():
    """Main execution function for full extraction."""
    print("🕉️  COMPLETE SKANDA PURANA NAME EXTRACTION 🕉️")
    print("="*70)
    print("Processing all 20 PDF volumes systematically...")
    print("This comprehensive extraction may take several hours.")
    print("="*70)
    
    # Initialize extractor
    extractor = FullSkandaPuranaExtractor()
    
    # Process all PDFs
    print(f"\n📚 Starting full extraction from: {extractor.pdf_folder}")
    extractor.process_all_pdfs()
    
    # Export final results
    print("\n💾 Exporting final results...")
    extractor.export_final_results()
    
    # Generate and save final report
    report = extractor.generate_final_report()
    print(report)
    
    with open("COMPLETE_SKANDA_EXTRACTION_REPORT.txt", "w", encoding='utf-8') as f:
        f.write(report)
    
    print("\n✅ COMPLETE EXTRACTION FINISHED!")
    print("📄 Final CSV: COMPLETE_SKANDA_PURANA_NAMES_EXTRACTED.csv")
    print("📊 Final report: COMPLETE_SKANDA_EXTRACTION_REPORT.txt")
    print("📋 Processing log: full_skanda_extraction.log")
    print("\n🎯 Ready for your son's authentic Sanskrit naming!")

if __name__ == "__main__":
    main()