#!/usr/bin/env python3
"""
Rerun Failed Thiruppugazh Songs and Merge into Complete CSV

This script specifically targets the failed songs due to connection issues
and merges the results into the existing COMPLETE_THIRUPPUGAZH_ALL_SONGS_WITH_NUMBERS.csv
"""

import csv
import time
import random
from typing import List, Set
from thiruppugazh_extractor_with_csv import ThiruppugazhExtractorWithCSV, ThiruppugazhNameCSV

class FailedSongsRerunner:
    """Rerun failed songs with enhanced retry logic."""
    
    def __init__(self):
        self.extractor = ThiruppugazhExtractorWithCSV()
        # Enhanced session settings for better reliability
        self.extractor.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
        })
        
        # Failed song numbers from your list
        self.failed_songs = [183, 106, 206, 906, 788, 779, 1106]
        
    def extract_with_enhanced_retry(self, song_number: int, max_retries: int = 5) -> List[ThiruppugazhNameCSV]:
        """Extract with enhanced retry logic for connection issues."""
        for attempt in range(max_retries):
            try:
                print(f"   📿 Song {song_number:4d} (Attempt {attempt + 1}/{max_retries}): ", end='')
                
                # Longer delay for failed songs to avoid overwhelming server
                delay = random.uniform(2.0, 4.0) + (attempt * 1.0)  # Increasing delay
                time.sleep(delay)
                
                names = self.extractor.extract_from_song(song_number)
                
                if names:
                    print(f"✅ {len(names)} names found")
                    return names
                else:
                    print(f"⚪ 0 names found (successful connection)")
                    return []
                    
            except Exception as e:
                error_msg = str(e)
                print(f"❌ Attempt {attempt + 1} failed: {error_msg[:50]}...")
                
                if attempt < max_retries - 1:
                    # Progressive backoff delay
                    backoff_delay = (2 ** attempt) + random.uniform(1, 3)
                    print(f"      ⏱️  Waiting {backoff_delay:.1f}s before retry...")
                    time.sleep(backoff_delay)
                else:
                    print(f"      ❌ All {max_retries} attempts failed for song {song_number}")
        
        return []
    
    def rerun_failed_songs(self) -> List[ThiruppugazhNameCSV]:
        """Rerun all failed songs with enhanced retry."""
        print("🔄 RERUNNING FAILED THIRUPPUGAZH SONGS")
        print("=" * 60)
        print(f"Failed songs to reprocess: {self.failed_songs}")
        print(f"Using enhanced retry logic with progressive backoff")
        
        all_recovered_names = []
        successfully_processed = []
        still_failing = []
        
        for song_num in self.failed_songs:
            print(f"\n🎵 REPROCESSING SONG {song_num}:")
            
            names = self.extract_with_enhanced_retry(song_num, max_retries=5)
            
            if names or not self._check_connection_error(song_num):
                # Either found names or successfully connected (even if no names)
                all_recovered_names.extend(names)
                successfully_processed.append(song_num)
                print(f"   ✅ Song {song_num} successfully reprocessed")
            else:
                still_failing.append(song_num)
                print(f"   ❌ Song {song_num} still failing after all retries")
        
        print(f"\n📊 RERUN RESULTS:")
        print(f"   Successfully processed: {successfully_processed}")
        print(f"   Still failing: {still_failing}")
        print(f"   Total names recovered: {len(all_recovered_names)}")
        
        return all_recovered_names
    
    def _check_connection_error(self, song_number: int) -> bool:
        """Quick check if song still has connection issues."""
        try:
            url = f"{self.extractor.base_url}nnt{song_number:04d}_u.html"
            response = self.extractor.session.head(url, timeout=10)
            response.raise_for_status()
            return False  # No connection error
        except:
            return True  # Still has connection error
    
    def merge_with_existing_csv(self, new_names: List[ThiruppugazhNameCSV], 
                               existing_csv: str = 'COMPLETE_THIRUPPUGAZH_ALL_SONGS_WITH_NUMBERS.csv',
                               output_csv: str = 'COMPLETE_THIRUPPUGAZH_ALL_SONGS_WITH_NUMBERS_UPDATED.csv'):
        """Merge new names with existing CSV."""
        
        if not new_names:
            print("⚪ No new names to merge")
            return existing_csv
        
        print(f"\n📋 MERGING WITH EXISTING CSV...")
        print(f"   Reading existing: {existing_csv}")
        
        # Read existing CSV
        existing_names = []
        existing_song_numbers = set()
        
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
                    existing_song_numbers.add(int(row['Song_Number_X']))
            
            print(f"   Existing records: {len(existing_names)}")
            
        except FileNotFoundError:
            print(f"   ⚠️  Existing CSV not found, creating new one")
            existing_names = []
            existing_song_numbers = set()
        
        # Remove any existing entries for the failed songs (to avoid duplicates)
        filtered_existing = [name for name in existing_names 
                           if name['Song_Number_X'] not in self.failed_songs]
        
        removed_count = len(existing_names) - len(filtered_existing)
        if removed_count > 0:
            print(f"   Removed {removed_count} old entries for reprocessed songs")
        
        # Convert new names to dict format
        new_name_dicts = []
        for name_obj in new_names:
            new_name_dicts.append({
                'Name': name_obj.name,
                'Song_Number_X': name_obj.song_number,
                'Song_URL': name_obj.song_url,
                'Context': name_obj.context,
                'Meaning': name_obj.meaning,
                'Category': name_obj.category,
                'Confidence_Score': f"{name_obj.confidence:.2f}"
            })
        
        # Combine all names
        all_names = filtered_existing + new_name_dicts
        
        # Sort by song number for easy reference
        all_names.sort(key=lambda x: x['Song_Number_X'])
        
        # Write updated CSV
        with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Name', 'Song_Number_X', 'Song_URL', 'Context', 'Meaning', 'Category', 'Confidence_Score']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for name_dict in all_names:
                writer.writerow(name_dict)
        
        print(f"   ✅ Updated CSV written: {output_csv}")
        print(f"   Total records: {len(all_names)}")
        print(f"   Added from rerun: {len(new_name_dicts)}")
        
        # Generate statistics
        unique_songs = len(set(name['Song_Number_X'] for name in all_names))
        print(f"   Songs with names: {unique_songs}")
        
        return output_csv
    
    def generate_rerun_report(self, recovered_names: List[ThiruppugazhNameCSV]) -> str:
        """Generate report of rerun results."""
        
        by_song = {}
        for name in recovered_names:
            song_num = name.song_number
            if song_num not in by_song:
                by_song[song_num] = []
            by_song[song_num].append(name)
        
        report = f"""
🔄 FAILED SONGS RERUN REPORT 🔄
{'=' * 50}

📊 RERUN STATISTICS:
   • Failed Songs List: {self.failed_songs}
   • Songs Successfully Reprocessed: {len(by_song)}
   • Songs Still Failing: {len(self.failed_songs) - len(by_song)}
   • Total Names Recovered: {len(recovered_names)}

📿 NAMES RECOVERED BY SONG:
"""
        
        for song_num in sorted(by_song.keys()):
            names_in_song = by_song[song_num]
            report += f"\n   Song {song_num}: {len(names_in_song)} names\n"
            for name_obj in names_in_song:
                report += f"     • {name_obj.name} (confidence: {name_obj.confidence:.2f})\n"
        
        still_failing = [s for s in self.failed_songs if s not in by_song]
        if still_failing:
            report += f"\n❌ SONGS STILL FAILING:\n"
            for song_num in still_failing:
                report += f"   • Song {song_num}: Connection issues persist\n"
        
        report += f"""
🎯 COMPLETION STATUS:
   • Recovery Success Rate: {len(by_song)/len(self.failed_songs)*100:.1f}%
   • CSV Updated: COMPLETE_THIRUPPUGAZH_ALL_SONGS_WITH_NUMBERS_UPDATED.csv
   • Ready for your son's naming decision

{'=' * 50}
"""
        
        return report

def main():
    """Main rerun function."""
    rerunner = FailedSongsRerunner()
    
    print("🔄 THIRUPPUGAZH FAILED SONGS RERUN SYSTEM")
    print("=" * 60)
    print("This will reprocess the failed songs with enhanced retry logic")
    print(f"Failed songs: {rerunner.failed_songs}")
    
    proceed = input("\nProceed with rerun? (y/n): ").strip().lower()
    if proceed != 'y':
        print("Rerun cancelled.")
        return
    
    # Rerun failed songs
    recovered_names = rerunner.rerun_failed_songs()
    
    # Merge with existing CSV
    updated_csv = rerunner.merge_with_existing_csv(recovered_names)
    
    # Generate report
    report = rerunner.generate_rerun_report(recovered_names)
    with open('FAILED_SONGS_RERUN_REPORT.txt', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(report)
    
    print("📁 FILES UPDATED:")
    print("   ✅ COMPLETE_THIRUPPUGAZH_ALL_SONGS_WITH_NUMBERS_UPDATED.csv")
    print("   ✅ FAILED_SONGS_RERUN_REPORT.txt")
    
    print(f"\n🏆 RERUN COMPLETE!")
    print(f"   Failed songs reprocessed with enhanced retry logic")
    print(f"   CSV updated with recovered names")
    print(f"   Complete database ready for your son's naming!")

if __name__ == "__main__":
    main()