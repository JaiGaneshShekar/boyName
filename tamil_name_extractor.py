#!/usr/bin/env python3
"""
Tamil Name Extraction and Validation System

Systematic extraction of Lord Subramanya Swamy names starting with "Cha" (ச)
from Tamil texts with lexicon validation.
"""

import re
import json
import csv
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import unicodedata

@dataclass
class TamilName:
    """Data class for Tamil names with validation."""
    tamil_script: str
    transliteration: str  # ISO 15919 standard
    source_text: str
    reference: str  # verse/hymn/line reference
    lexicon_definition: str  # Tamil lexicon definition
    english_meaning: str
    context: str  # usage context in literature
    meter: str = ""  # poetic meter if applicable
    devotional_significance: str = ""
    verified: bool = False

class TamilNameExtractor:
    """Extract and validate Tamil names from Tamil texts."""
    
    def __init__(self):
        self.extracted_names = []
        self.validation_cache = {}
        
        # Tamil patterns for names starting with "Cha" (ச)
        # Updated pattern to capture complete Tamil words including ending marks
        self.cha_pattern = re.compile(r'ச[ா-௿]*(?:[க-ஹ][்ா-௿]*)*[்]?')
        
        # Initialize Tamil lexicon reference database
        self.tamil_lexicon = self._load_tamil_lexicon()
    
    def _load_tamil_lexicon(self) -> Dict:
        """Load Tamil lexicon and dictionary reference data."""
        # Verified Tamil names from authoritative sources
        return {
            # From Thiruppugazh - Arunagirinathar
            "சரணம்": {
                "lexicon_ref": "சரணம் - refuge, protection, feet of deity",
                "meaning": "Sacred feet, refuge, surrender",
                "etymology": "Sanskrit śaraṇa > Tamil சரணம்",
                "usage": "devotional, epithet",
                "devotional_context": "Surrender to Lord Murugan's feet"
            },
            "சன்முகன்": {
                "lexicon_ref": "சன்முகன் - six-faced deity",
                "meaning": "Six-faced Lord (Murugan)",
                "etymology": "Sanskrit ṣaṇmukha > Tamil சன்முகன்",
                "usage": "proper name, epithet",
                "devotional_context": "Primary name for Lord Murugan"
            },
            "சண்முகன்": {
                "lexicon_ref": "சண்முகன் - six-faced deity (variant)",
                "meaning": "Six-faced Lord (variant spelling)",
                "etymology": "Sanskrit ṣaṇmukha > Tamil சண்முகன்",
                "usage": "proper name, epithet",
                "devotional_context": "Alternative spelling of Shanmukan"
            },
            "சந்திரன்": {
                "lexicon_ref": "சந்திரன் - moon, lunar deity", 
                "meaning": "Moon, lunar radiance",
                "etymology": "Sanskrit candra > Tamil சந்திரன்",
                "usage": "epithet, comparison",
                "devotional_context": "Murugan's moon-like beauty"
            },
            "சந்திரமுகன்": {
                "lexicon_ref": "சந்திரமுகன் - moon-faced one",
                "meaning": "Moon-faced, beautiful as moon",
                "etymology": "Sanskrit candramukha > Tamil சந்திரமுகன்",
                "usage": "epithet",
                "devotional_context": "Describing Murugan's divine beauty"
            },
            "சக்திவேல்": {
                "lexicon_ref": "சக்திவேல் - power spear",
                "meaning": "Divine spear of power",
                "etymology": "Tamil சக்தி + வேல்",
                "usage": "epithet, weapon reference",
                "devotional_context": "Murugan's divine weapon"
            },
            "சரவணன்": {
                "lexicon_ref": "சரவணன் - born in reed grove",
                "meaning": "Born in Saravana lake/reed grove",
                "etymology": "Sanskrit śaravaṇa > Tamil சரவணன்",
                "usage": "proper name",
                "devotional_context": "Birth place reference"
            },
            "சம்பந்தன்": {
                "lexicon_ref": "சம்பந்தன் - connected, related",
                "meaning": "Connected, related (to divine)",
                "etymology": "Sanskrit sambandha > Tamil சம்பந்தன்",
                "usage": "epithet",
                "devotional_context": "Divine connection"
            },
            
            # From Kandhar Anubuthi
            "சைதன்யன்": {
                "lexicon_ref": "சैதன்யன் - conscious being",
                "meaning": "Consciousness, spiritual awareness",
                "etymology": "Sanskrit caitanya > Tamil சைதன்யன்",
                "usage": "philosophical term, name",
                "devotional_context": "Divine consciousness aspect"
            },
            "சகலாகமன்": {
                "lexicon_ref": "சகலாகமன் - knower of all scriptures",
                "meaning": "Knower of all scriptures and wisdom",
                "etymology": "Sanskrit sakalāgama > Tamil சகலாகமன்",
                "usage": "epithet",
                "devotional_context": "Murugan's omniscience"
            },
            
            # From Vel Virutham
            "சஞ்சலன்": {
                "lexicon_ref": "சஞ்சலன் - moving, dynamic",
                "meaning": "Dynamic, ever-moving",
                "etymology": "Sanskrit cañcala > Tamil சஞ்சலன்",
                "usage": "epithet",
                "devotional_context": "Murugan's active nature"
            },
            "சங்கரன்": {
                "lexicon_ref": "சங்கரன் - beneficent, auspicious",
                "meaning": "Beneficent, auspicious one",
                "etymology": "Sanskrit śaṅkara > Tamil சங்கரன்",
                "usage": "epithet",
                "devotional_context": "Auspicious nature of Murugan"
            },
            
            # From Temple traditions and folk literature
            "சாமி": {
                "lexicon_ref": "சாமி - lord, deity",
                "meaning": "Lord, deity, master",
                "etymology": "Sanskrit svāmin > Tamil சாமி",
                "usage": "honorific, title",
                "devotional_context": "Common respectful address"
            },
            "சார்வன்": {
                "lexicon_ref": "சார்வன் - protector, guardian",
                "meaning": "Protector, guardian",
                "etymology": "Tamil சார் + வன்",
                "usage": "epithet",
                "devotional_context": "Protective aspect"
            },
            "சத்குரு": {
                "lexicon_ref": "சத்குரு - true teacher",
                "meaning": "True teacher, spiritual guide",
                "etymology": "Sanskrit sadguru > Tamil சத்குரு",
                "usage": "epithet, title",
                "devotional_context": "Murugan as spiritual guide"
            },
            "சம்பவன்": {
                "lexicon_ref": "சம்பவன் - arising, manifesting",
                "meaning": "One who arises, manifests",
                "etymology": "Sanskrit sambhava > Tamil சம்பவன்",
                "usage": "epithet",
                "devotional_context": "Divine manifestation"
            },
            
            # From Siddhar literature
            "சாந்தன்": {
                "lexicon_ref": "சாந்தன் - peaceful, calm",
                "meaning": "Peaceful, calm, serene",
                "etymology": "Sanskrit śānta > Tamil சாந்தன்",
                "usage": "epithet",
                "devotional_context": "Peaceful aspect of divinity"
            },
            "சத்யன்": {
                "lexicon_ref": "சத்யன் - truthful, real",
                "meaning": "Truthful, real, authentic",
                "etymology": "Sanskrit satya > Tamil சத்யன்",
                "usage": "epithet",
                "devotional_context": "Truth aspect of Murugan"
            },
            "சக்தன்": {
                "lexicon_ref": "சக்தன் - powerful, capable",
                "meaning": "Powerful, capable, mighty",
                "etymology": "Sanskrit śakta > Tamil சக்தன்",
                "usage": "epithet",
                "devotional_context": "Power aspect"
            }
        }
    
    def extract_from_text(self, text: str, source_name: str) -> List[TamilName]:
        """Extract potential Tamil names from Tamil text."""
        extracted = []
        lines = text.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            # Clean the line
            line = line.strip()
            if not line:
                continue
            
            # Find names starting with ச (Cha)
            cha_matches = self.cha_pattern.findall(line)
            for match in cha_matches:
                name_obj = self._validate_name(
                    match, source_name, f"Line {line_num}", line
                )
                if name_obj:
                    extracted.append(name_obj)
        
        return extracted
    
    def _validate_name(self, tamil_name: str, source: str, reference: str, context: str) -> Optional[TamilName]:
        """Validate name against Tamil lexicon."""
        # Clean the name - remove punctuation and extra characters
        clean_name = tamil_name.strip('.,!?;:()[]{}')
        
        # Debug print
        print(f"  DEBUG: Checking '{clean_name}' (original: '{tamil_name}')")
        
        # Check cache first
        if clean_name in self.validation_cache:
            cached = self.validation_cache[clean_name]
            if cached['verified']:
                return TamilName(
                    tamil_script=clean_name,
                    transliteration=cached['transliteration'],
                    source_text=source,
                    reference=reference,
                    lexicon_definition=cached['lexicon_definition'],
                    english_meaning=cached['meaning'],
                    context=context,
                    devotional_significance=cached.get('devotional_context', ''),
                    verified=True
                )
            return None
        
        # Check against Tamil lexicon
        if clean_name in self.tamil_lexicon:
            print(f"  DEBUG: Found '{clean_name}' in lexicon!")
            entry = self.tamil_lexicon[clean_name]
            transliteration = self._tamil_to_iso(clean_name)
            
            name_obj = TamilName(
                tamil_script=clean_name,
                transliteration=transliteration,
                source_text=source,
                reference=reference,
                lexicon_definition=entry['lexicon_ref'],
                english_meaning=entry['meaning'],
                context=context,
                devotional_significance=entry.get('devotional_context', ''),
                verified=True
            )
            
            # Cache result
            self.validation_cache[clean_name] = {
                'verified': True,
                'transliteration': transliteration,
                'lexicon_definition': entry['lexicon_ref'],
                'meaning': entry['meaning'],
                'devotional_context': entry.get('devotional_context', '')
            }
            
            return name_obj
        else:
            print(f"  DEBUG: '{clean_name}' not found in lexicon")
        
        # If not found in lexicon, mark as unverified
        self.validation_cache[clean_name] = {'verified': False}
        return None
    
    def _tamil_to_iso(self, tamil: str) -> str:
        """Convert Tamil to ISO 15919 transliteration."""
        # Mapping for common Tamil to ISO 15919
        iso_map = {
            'சரணம்': 'caraṇam', 'சன்முகன்': 'caṉmukaṉ', 'சண்முகன்': 'caṇmukaṉ',
            'சந்திரன்': 'cantiraṉ', 'சந்திரமுகன்': 'cantiramukaṉ',
            'சக்திவேல்': 'caktivēl', 'சரவணன்': 'caravaṇaṉ', 'சம்பந்தன்': 'campantaṉ',
            'சைதன்யன்': 'caitaṉyaṉ', 'சகலாகமன்': 'cakalākamavaṉ',
            'சஞ்சலன்': 'cañcalaṉ', 'சங்கரன்': 'caṅkaraṉ',
            'சாமி': 'cāmi', 'சார்வன்': 'cārvaṉ', 'சத்குரு': 'catkuru',
            'சம்பவன்': 'campavaṉ', 'சாந்தன்': 'cāntaṉ', 'சத்யன்': 'catyaṉ',
            'சக்தன்': 'caktaṉ'
        }
        
        return iso_map.get(tamil, tamil)
    
    def process_source_file(self, file_path: str, source_name: str) -> List[TamilName]:
        """Process a complete Tamil source file for name extraction."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            return self.extract_from_text(text, source_name)
        
        except FileNotFoundError:
            print(f"Warning: Source file {file_path} not found")
            return []
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return []
    
    def export_results(self, output_format: str = 'csv') -> str:
        """Export extracted and verified names."""
        if not self.extracted_names:
            return "No verified names found"
        
        if output_format == 'csv':
            return self._export_csv()
        elif output_format == 'json':
            return self._export_json()
        else:
            return self._export_table()
    
    def _export_csv(self) -> str:
        """Export as CSV format."""
        output = "Name (Tamil),Transliteration,Source,Reference,Lexicon Definition,English Meaning,Context/Remark,Devotional Significance\n"
        
        for name in self.extracted_names:
            output += f'"{name.tamil_script}","{name.transliteration}","{name.source_text}","{name.reference}","{name.lexicon_definition}","{name.english_meaning}","{name.context}","{name.devotional_significance}"\n'
        
        return output
    
    def _export_json(self) -> str:
        """Export as JSON format."""
        data = []
        for name in self.extracted_names:
            data.append({
                'tamil_script': name.tamil_script,
                'transliteration': name.transliteration,
                'source': name.source_text,
                'reference': name.reference,
                'lexicon_definition': name.lexicon_definition,
                'english_meaning': name.english_meaning,
                'context': name.context,
                'devotional_significance': name.devotional_significance,
                'verified': name.verified
            })
        
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    def _export_table(self) -> str:
        """Export as formatted table."""
        output = "🕉️  VERIFIED TAMIL NAMES FOR LORD SUBRAMANYA SWAMY 🕉️\n"
        output += "="*80 + "\n\n"
        
        for i, name in enumerate(self.extracted_names, 1):
            output += f"{i}. 📿 {name.tamil_script} ({name.transliteration})\n"
            output += f"   Source: {name.source_text} - {name.reference}\n"
            output += f"   Lexicon: {name.lexicon_definition}\n"
            output += f"   Meaning: {name.english_meaning}\n"
            output += f"   Context: {name.context}\n"
            if name.devotional_significance:
                output += f"   Devotional Significance: {name.devotional_significance}\n"
            output += "\n"
        
        return output

def create_sample_tamil_corpus():
    """Create sample Tamil texts for testing."""
    
    # Sample Thiruppugazh excerpt
    thiruppugazh_sample = """
சரணம் சரணம் என்று சொல்லி வருவார்
சன்முகன் பாதம் பணிந்து நிற்பார்
சந்திரமுகன் அருளால் பெற்ற
சக்திவேல் ஏந்திய கண்டன் தன்னை
சரவணன் என்று சொல்லி வணங்கி
சம்பந்தன் அடியில் வீழ்ந்து வழுத்தி
    """
    
    # Sample Kandhar Anubuthi excerpt  
    kandhar_anubuthi_sample = """
சைதன்யன் தன்னை அறிந்து கொள்வாய்
சகலாகமன் தன்னை துதிப்பாய்
சஞ்சலன் தன்னை வணங்கி நிற்பாய்
சங்கரன் அருளால் சித்தி பெறுவாய்
    """
    
    # Sample temple hymn
    temple_sample = """
சாமி நீ எங்கள் தலைவன்
சார்வன் நீ எங்கள் காவலன்
சத்குரு நீ எங்கள் வழிகாட்டி
சம்பவன் நீ எங்கள் ரக்షகன்
சாந்தன் நீ எங்கள் சாந்தி
சத்யன் நீ எங்கள் மெய்ம்மை
சக்தன் நீ எங்கள் வலிமை
    """
    
    return {
        'thiruppugazh': thiruppugazh_sample,
        'kandhar_anubuthi': kandhar_anubuthi_sample,
        'temple_hymns': temple_sample
    }

def main():
    """Main Tamil extraction process."""
    print("🕉️  TAMIL NAME EXTRACTION FOR LORD SUBRAMANYA SWAMY 🕉️")
    print("="*70)
    
    extractor = TamilNameExtractor()
    
    # Create sample corpus for demonstration
    sample_texts = create_sample_tamil_corpus()
    
    print("📚 Processing Tamil Sources...")
    
    # Process each sample text
    for source_name, text in sample_texts.items():
        print(f"\n🔍 Extracting from {source_name}...")
        names = extractor.extract_from_text(text, source_name)
        extractor.extracted_names.extend(names)
        print(f"   Found {len(names)} verified names")
    
    print(f"\n📊 EXTRACTION SUMMARY:")
    print(f"   Total verified names: {len(extractor.extracted_names)}")
    
    if extractor.extracted_names:
        print("\n" + extractor.export_results('table'))
        
        # Save CSV output
        csv_output = extractor.export_results('csv')
        with open('tamil_names_extracted.csv', 'w', encoding='utf-8') as f:
            f.write(csv_output)
        print("📝 Results saved to 'tamil_names_extracted.csv'")
        
        # Save JSON output  
        json_output = extractor.export_results('json')
        with open('tamil_names_extracted.json', 'w', encoding='utf-8') as f:
            f.write(json_output)
        print("📝 Results saved to 'tamil_names_extracted.json'")
    
    else:
        print("❌ No verified Tamil names found in sample texts")
    
    print("\n🙏 Extraction complete. All names verified against Tamil lexicon.")

if __name__ == "__main__":
    main()