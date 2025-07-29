#!/usr/bin/env python3
"""
Thiruppugazh Extractor with CSV Export including Song Numbers

This creates a CSV with the specific song number (X) from the URL pattern:
https://kaumaram.com/thiru/nnt000X_u.html#english where X is 6 to 1340
"""

import requests
import re
import time
import json
import csv
from typing import List, Dict
from dataclasses import dataclass, asdict
from bs4 import BeautifulSoup
import random
from datetime import datetime

@dataclass
class ThiruppugazhNameCSV:
    """Name structure for CSV export with song number."""
    name: str
    song_number: int  # This is the X from nnt000X_u.html
    song_url: str
    context: str
    meaning: str
    category: str
    confidence: float

class ThiruppugazhExtractorWithCSV:
    """Extractor with proper CSV export including song numbers."""
    
    def __init__(self):
        self.base_url = "https://kaumaram.com/thiru/"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Key patterns for Sa/Cha/Sha names
        self.patterns = [
            r'\b[Ss]aravana[a-z]*\b',
            r'\b[Ss]haravan[a-z]*\b', 
            r'\b[Ss]aktivel[a-z]*\b',
            r'\b[Ss]haktivel[a-z]*\b',
            r'\b[Ss]hanmukh[a-z]*\b',
            r'\b[Cc]hanmukh[a-z]*\b',
            r'\b[Ss]iva[a-z]*\b',
            r'\b[Ss]hiva[a-z]*\b',
            r'\b[Ss]ami[a-z]*\b',
            r'\b[Ss]wami[a-z]*\b',
            r'\b[Cc]handra[a-z]*\b',
            r'\b[Ss]handra[a-z]*\b',
            r'\b[Ss]ubramany[a-z]*\b',
            r'\b[Ss]ubrahmany[a-z]*\b',
            r'\b[Ss]aran[a-z]*\b',
            r'\b[Cc]haran[a-z]*\b',
            r'\b[Ss]hambhu[a-z]*\b',
            r'\b[Cc]haitany[a-z]*\b'
        ]
        
        self.divine_indicators = [
            'lord', 'god', 'murugan', 'divine', 'deity', 'worship', 'prayer',
            'blessing', 'grace', 'temple', 'sacred', 'holy'
        ]
        
        self.extracted_names = []
    
    def extract_from_song(self, song_number: int) -> List[ThiruppugazhNameCSV]:
        """Extract names from single song with song number tracking."""
        url = f"{self.base_url}nnt{song_number:04d}_u.html"
        
        try:
            time.sleep(random.uniform(0.5, 1.0))
            
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            page_text = soup.get_text()
            
            # Extract English sections
            english_content = self._extract_english_text(page_text)
            
            names_found = []
            for pattern in self.patterns:
                matches = re.finditer(pattern, english_content, re.IGNORECASE)
                
                for match in matches:
                    name = match.group().strip()
                    if len(name) < 4:
                        continue
                    
                    # Get context
                    start = max(0, match.start() - 100)
                    end = min(len(english_content), match.end() + 100)
                    context = english_content[start:end]
                    
                    # Validate divine context
                    confidence = self._calculate_confidence(name, context)
                    if confidence >= 0.3:
                        names_found.append(ThiruppugazhNameCSV(
                            name=name.title(),
                            song_number=song_number,  # This is the X from the URL
                            song_url=url,
                            context=context.replace('\n', ' ').strip()[:200],
                            meaning=self._extract_meaning(name, context),
                            category=self._categorize_name(name, context),
                            confidence=confidence
                        ))
            
            return self._deduplicate_names(names_found)
            
        except Exception as e:
            print(f"   ❌ Error processing song {song_number}: {e}")
            return []
    
    def _extract_english_text(self, page_text: str) -> str:
        """Extract English text from page."""
        lines = page_text.split('\n')
        english_lines = []
        
        for line in lines:
            line = line.strip()
            if self._is_english_line(line):
                english_lines.append(line)
        
        return ' '.join(english_lines)
    
    def _is_english_line(self, line: str) -> bool:
        """Check if line is primarily English."""
        if not line or len(line) < 10:
            return False
        
        english_chars = sum(1 for c in line if c.isascii() and c.isalpha())
        total_chars = sum(1 for c in line if c.isalpha())
        
        if total_chars == 0:
            return False
        
        return (english_chars / total_chars) > 0.7
    
    def _calculate_confidence(self, name: str, context: str) -> float:
        """Calculate confidence score."""
        confidence = 0.3  # Base confidence
        
        name_lower = name.lower()
        context_lower = context.lower()
        
        # High-value names
        premium_names = {
            'saravana': 0.4,
            'shanmukha': 0.4, 
            'subrahmanya': 0.5,
            'shaktivel': 0.4,
            'siva': 0.2
        }
        
        for premium, bonus in premium_names.items():
            if premium in name_lower:
                confidence += bonus
                break
        
        # Context validation
        divine_count = sum(1 for indicator in self.divine_indicators 
                          if indicator in context_lower)
        confidence += min(0.3, divine_count * 0.1)
        
        return min(1.0, confidence)
    
    def _categorize_name(self, name: str, context: str) -> str:
        """Categorize the name."""
        name_lower = name.lower()
        context_lower = context.lower()
        
        if any(dn in name_lower for dn in ['saravana', 'shanmukha', 'subrahmanya']):
            return 'primary_divine_name'
        elif any(dn in name_lower for dn in ['siva', 'sami', 'swami']):
            return 'secondary_divine_name'
        elif any(word in context_lower for word in ['spear', 'weapon', 'power']):
            return 'divine_attribute'
        else:
            return 'divine_epithet'
    
    def _extract_meaning(self, name: str, context: str) -> str:
        """Extract meaning from context."""
        sentences = re.split(r'[.!?]', context)
        for sentence in sentences:
            if name.lower() in sentence.lower():
                clean = sentence.strip()
                if len(clean) > 20:
                    return clean[:100] + "..." if len(clean) > 100 else clean
        
        return context[:100] + "..." if len(context) > 100 else context
    
    def _deduplicate_names(self, names: List[ThiruppugazhNameCSV]) -> List[ThiruppugazhNameCSV]:
        """Remove duplicates within song."""
        seen = {}
        for name_obj in names:
            key = name_obj.name.lower()
            if key not in seen or name_obj.confidence > seen[key].confidence:
                seen[key] = name_obj
        return list(seen.values())
    
    def extract_batch(self, start_song: int, end_song: int) -> List[ThiruppugazhNameCSV]:
        """Extract from batch of songs."""
        print(f"🎵 EXTRACTING BATCH: Songs {start_song} to {end_song}")
        print("=" * 60)
        
        all_names = []
        for song_num in range(start_song, end_song + 1):
            print(f"   📿 Song {song_num:4d}: ", end='')
            names = self.extract_from_song(song_num)
            all_names.extend(names)
            print(f"{len(names)} names found")
        
        self.extracted_names = all_names
        print(f"\n✅ BATCH COMPLETE: {len(all_names)} total names extracted")
        return all_names
    
    def export_to_csv(self, filename: str = 'thiruppugazh_names_with_song_numbers.csv'):
        """Export to CSV with song numbers as requested."""
        if not self.extracted_names:
            print("❌ No names to export")
            return
        
        # Global deduplication
        unique_names = {}
        for name_obj in self.extracted_names:
            key = name_obj.name.lower()
            if key not in unique_names or name_obj.confidence > unique_names[key].confidence:
                unique_names[key] = name_obj
        
        final_names = list(unique_names.values())
        
        # Sort by song number for easy reference
        final_names.sort(key=lambda x: x.song_number)
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'Name', 
                'Song_Number_X',  # This is the X from nnt000X_u.html
                'Song_URL', 
                'Context', 
                'Meaning', 
                'Category', 
                'Confidence_Score'
            ]
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for name_obj in final_names:
                writer.writerow({
                    'Name': name_obj.name,
                    'Song_Number_X': name_obj.song_number,  # The specific X value
                    'Song_URL': name_obj.song_url,
                    'Context': name_obj.context,
                    'Meaning': name_obj.meaning,
                    'Category': name_obj.category,
                    'Confidence_Score': f"{name_obj.confidence:.2f}"
                })
        
        print(f"✅ CSV exported: {filename}")
        print(f"   Unique names: {len(final_names)}")
        print(f"   Song number range: {min(n.song_number for n in final_names)} to {max(n.song_number for n in final_names)}")
        
        return filename
    
    def generate_summary(self) -> str:
        """Generate extraction summary."""
        if not self.extracted_names:
            return "No names extracted."
        
        unique_names = {}
        for name_obj in self.extracted_names:
            key = name_obj.name.lower()
            if key not in unique_names or name_obj.confidence > unique_names[key].confidence:
                unique_names[key] = name_obj
        
        final_names = list(unique_names.values())
        high_conf = [n for n in final_names if n.confidence >= 0.7]
        
        by_category = {}
        for name in final_names:
            by_category[name.category] = by_category.get(name.category, 0) + 1
        
        songs_covered = set(n.song_number for n in final_names)
        
        summary = f"""
🕉️ THIRUPPUGAZH EXTRACTION WITH SONG NUMBERS - SUMMARY 🕉️
{'=' * 70}

📊 EXTRACTION STATISTICS:
   • Total Names Extracted: {len(self.extracted_names)}
   • Unique Names: {len(final_names)}
   • High Confidence Names (≥0.7): {len(high_conf)}
   • Songs with Names Found: {len(songs_covered)}
   • Song Number Range: {min(songs_covered) if songs_covered else 'N/A'} to {max(songs_covered) if songs_covered else 'N/A'}

📚 NAME CATEGORIES:
"""
        
        for category, count in sorted(by_category.items(), key=lambda x: x[1], reverse=True):
            summary += f"   • {category.replace('_', ' ').title()}: {count}\n"
        
        summary += f"""
📿 TOP NAMES WITH SONG NUMBERS:
"""
        
        top_names = sorted(final_names, key=lambda x: x.confidence, reverse=True)[:10]
        for i, name in enumerate(top_names, 1):
            summary += f"   {i:2d}. {name.name} (Song {name.song_number}, Confidence: {name.confidence:.2f})\n"
        
        summary += f"""
🎯 CSV EXPORT READY:
   CSV file includes the specific song number (X) from the URL pattern:
   https://kaumaram.com/thiru/nnt000X_u.html#english
   
   This allows you to trace each name back to its exact source song.

{'=' * 70}
"""
        
        return summary

def main():
    """Main extraction with CSV export."""
    extractor = ThiruppugazhExtractorWithCSV()
    
    print("🕉️ THIRUPPUGAZH EXTRACTOR WITH CSV SONG NUMBERS")
    print("=" * 60)
    print("This will extract names and create CSV with song numbers (X) as requested")
    
    # Test extraction
    print("\n🧪 Running test extraction on songs 6-50...")
    names = extractor.extract_batch(6, 50)
    
    if names:
        # Export to CSV
        csv_file = extractor.export_to_csv('THIRUPPUGAZH_NAMES_WITH_SONG_NUMBERS.csv')
        
        # Generate summary
        summary = extractor.generate_summary()
        with open('THIRUPPUGAZH_EXTRACTION_SUMMARY.txt', 'w', encoding='utf-8') as f:
            f.write(summary)
        
        print(summary)
        
        print("📁 FILES GENERATED:")
        print("   ✅ THIRUPPUGAZH_NAMES_WITH_SONG_NUMBERS.csv")
        print("   ✅ THIRUPPUGAZH_EXTRACTION_SUMMARY.txt")
        
        # Show what the CSV looks like
        print(f"\n📋 CSV STRUCTURE:")
        print("Name | Song_Number_X | Song_URL | Context | Meaning | Category | Confidence_Score")
        print("Each row shows exactly which song (X) the name came from!")
        
    else:
        print("❌ No names extracted in test. Check connectivity.")

if __name__ == "__main__":
    main()