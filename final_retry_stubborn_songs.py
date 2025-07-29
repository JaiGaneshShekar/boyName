#!/usr/bin/env python3
"""
Final Retry for Stubborn Songs with Ultra-Conservative Approach

Songs 183, 906, 788 still having connection issues.
Using ultra-conservative retry with maximum delays.
"""

import csv
import time
import random
import requests
from bs4 import BeautifulSoup
from typing import List
from thiruppugazh_extractor_with_csv import ThiruppugazhNameCSV

class UltraConservativeRetry:
    """Ultra-conservative retry for stubborn songs."""
    
    def __init__(self):
        self.stubborn_songs = [183, 906, 788]
        self.base_url = "https://kaumaram.com/thiru/"
        
        # Ultra-conservative session
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'identity',  # No compression to avoid issues
            'Connection': 'close',  # Close connection after each request
            'Cache-Control': 'no-cache',
            'DNT': '1'
        })
        
        # Patterns for name extraction
        self.patterns = [
            r'\b[Ss]aravana[a-z]*\b',
            r'\b[Ss]haravan[a-z]*\b', 
            r'\b[Ss]aktivel[a-z]*\b',
            r'\b[Ss]hanmukh[a-z]*\b',
            r'\b[Cc]hanmukh[a-z]*\b',
            r'\b[Ss]iva[a-z]*\b',
            r'\b[Ss]ami[a-z]*\b',
            r'\b[Ss]wami[a-z]*\b',
            r'\b[Cc]handra[a-z]*\b',
            r'\b[Ss]ubramany[a-z]*\b',
            r'\b[Ss]aran[a-z]*\b',
            r'\b[Cc]haran[a-z]*\b'
        ]
    
    def ultra_conservative_extract(self, song_number: int) -> List[ThiruppugazhNameCSV]:
        """Ultra-conservative extraction with maximum delays."""
        url = f"{self.base_url}nnt{song_number:04d}_u.html"
        
        for attempt in range(10):  # Maximum 10 attempts
            try:
                print(f"   🐌 Song {song_number} - Ultra-conservative attempt {attempt + 1}/10")
                
                # Ultra-long delay with randomization
                delay = 5.0 + (attempt * 2.0) + random.uniform(0, 3.0)
                print(f"      ⏱️  Waiting {delay:.1f}s...")
                time.sleep(delay)
                
                # Create fresh session for each attempt
                if attempt > 0:
                    self.session.close()
                    self.session = requests.Session()
                    self.session.headers.update({
                        'User-Agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Connection': 'close'
                    })
                
                # Ultra-conservative request
                response = self.session.get(url, timeout=30, stream=True)
                response.raise_for_status()
                
                # Read content in chunks to avoid connection issues
                content = b''
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        content += chunk
                
                response.close()
                
                # Parse content
                soup = BeautifulSoup(content, 'html.parser')
                page_text = soup.get_text()
                
                # Extract English sections (simplified)
                english_text = self._extract_simple_english(page_text)
                
                # Find names
                names_found = []
                import re
                
                for pattern in self.patterns:
                    matches = re.finditer(pattern, english_text, re.IGNORECASE)
                    
                    for match in matches:
                        name = match.group().strip()
                        if len(name) >= 4:
                            # Simple context extraction
                            start = max(0, match.start() - 80)
                            end = min(len(english_text), match.end() + 80)
                            context = english_text[start:end].replace('\n', ' ').strip()
                            
                            names_found.append(ThiruppugazhNameCSV(
                                name=name.title(),
                                song_number=song_number,
                                song_url=url,
                                context=context[:200],
                                meaning=context[:100] + "...",
                                category='divine_name',
                                confidence=0.5
                            ))
                
                # Deduplicate
                unique_names = {}
                for name_obj in names_found:
                    key = name_obj.name.lower()
                    if key not in unique_names:
                        unique_names[key] = name_obj
                
                final_names = list(unique_names.values())
                
                print(f"      ✅ Success! Found {len(final_names)} names")
                return final_names
                
            except Exception as e:
                error_str = str(e)[:100]
                print(f"      ❌ Attempt {attempt + 1} failed: {error_str}")
                
                if attempt < 9:
                    # Progressive backoff
                    backoff = (2 ** min(attempt, 6)) + random.uniform(1, 5)
                    print(f"      ⏳ Backing off {backoff:.1f}s...")
                    time.sleep(backoff)
                else:
                    print(f"      💔 All attempts exhausted for song {song_number}")
        
        return []
    
    def _extract_simple_english(self, page_text: str) -> str:
        """Simple English text extraction."""
        lines = page_text.split('\n')
        english_lines = []
        
        for line in lines:
            line = line.strip()
            if len(line) > 10:
                # Check if line is primarily English
                english_chars = sum(1 for c in line if c.isascii() and c.isalpha())
                total_chars = sum(1 for c in line if c.isalpha())
                
                if total_chars > 0 and (english_chars / total_chars) > 0.6:
                    english_lines.append(line)
        
        return ' '.join(english_lines)
    
    def run_ultra_conservative_retry(self):
        """Run ultra-conservative retry on stubborn songs."""
        print("🐌 ULTRA-CONSERVATIVE RETRY FOR STUBBORN SONGS")
        print("=" * 60)
        print(f"Stubborn songs: {self.stubborn_songs}")
        print("Using maximum delays and conservative approach")
        
        all_recovered = []
        
        for song_num in self.stubborn_songs:
            print(f"\n🎵 ULTRA-CONSERVATIVE PROCESSING OF SONG {song_num}:")
            names = self.ultra_conservative_extract(song_num)
            all_recovered.extend(names)
            
            if names:
                print(f"   🎉 SUCCESS: Recovered {len(names)} names from song {song_num}")
                for name in names:
                    print(f"      • {name.name}")
            else:
                print(f"   😞 Song {song_num} still inaccessible")
            
            # Long pause between songs
            if song_num != self.stubborn_songs[-1]:
                print("   ⏸️  Long pause before next song...")
                time.sleep(10)
        
        return all_recovered
    
    def update_csv_with_final_names(self, new_names: List[ThiruppugazhNameCSV]):
        """Update CSV with final recovered names."""
        if not new_names:
            print("⚪ No additional names recovered")
            return
        
        print(f"\n📋 UPDATING CSV WITH FINAL RECOVERED NAMES...")
        
        # Read existing updated CSV
        existing_csv = 'COMPLETE_THIRUPPUGAZH_ALL_SONGS_WITH_NUMBERS_UPDATED.csv'
        final_csv = 'COMPLETE_THIRUPPUGAZH_ALL_SONGS_WITH_NUMBERS_FINAL.csv'
        
        existing_names = []
        try:
            with open(existing_csv, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    existing_names.append({
                        'Name': row['Name'],
                        'Song_Number_X': int(row['Song_Number_X']),
                        'Song_URL': row['Song_URL'],
                        'Context': row['Context'],
                        'Meaning': row['Meaning'],
                        'Category': row['Category'],
                        'Confidence_Score': row['Confidence_Score']
                    })
        except FileNotFoundError:
            print("   ⚠️  Updated CSV not found")
            return
        
        # Remove entries for stubborn songs to avoid duplicates
        filtered_existing = [name for name in existing_names 
                           if name['Song_Number_X'] not in self.stubborn_songs]
        
        # Add new names
        for name_obj in new_names:
            filtered_existing.append({
                'Name': name_obj.name,
                'Song_Number_X': name_obj.song_number,
                'Song_URL': name_obj.song_url,
                'Context': name_obj.context,
                'Meaning': name_obj.meaning,
                'Category': name_obj.category,
                'Confidence_Score': f"{name_obj.confidence:.2f}"
            })
        
        # Sort by song number
        filtered_existing.sort(key=lambda x: x['Song_Number_X'])
        
        # Write final CSV
        with open(final_csv, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Name', 'Song_Number_X', 'Song_URL', 'Context', 'Meaning', 'Category', 'Confidence_Score']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for name_dict in filtered_existing:
                writer.writerow(name_dict)
        
        print(f"   ✅ Final CSV written: {final_csv}")
        print(f"   Total records: {len(filtered_existing)}")
        print(f"   Additional names from stubborn songs: {len(new_names)}")

def main():
    """Main ultra-conservative retry."""
    retrier = UltraConservativeRetry()
    
    print("🐌 ULTRA-CONSERVATIVE RETRY SYSTEM")
    print("=" * 50)
    print("Final attempt at stubborn songs 183, 906, 788")
    print("Using maximum delays and conservative approach")
    
    proceed = input("\nProceed with ultra-conservative retry? (y/n): ").strip().lower()
    if proceed != 'y':
        print("Ultra-conservative retry cancelled.")
        return
    
    # Run ultra-conservative retry
    recovered_names = retrier.run_ultra_conservative_retry()
    
    # Update CSV
    retrier.update_csv_with_final_names(recovered_names)
    
    print(f"\n🏆 ULTRA-CONSERVATIVE RETRY COMPLETE!")
    print(f"   Additional names recovered: {len(recovered_names)}")
    print(f"   Final CSV ready: COMPLETE_THIRUPPUGAZH_ALL_SONGS_WITH_NUMBERS_FINAL.csv")

if __name__ == "__main__":
    main()