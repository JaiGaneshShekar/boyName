#!/usr/bin/env python3
"""
Complete Thiruppugazh Extraction Runner

This runs the complete extraction from ALL 1,340 songs and creates the CSV
with song numbers (X) from https://kaumaram.com/thiru/nnt000X_u.html#english
"""

from thiruppugazh_extractor_with_csv import ThiruppugazhExtractorWithCSV
import os
import time

def run_complete_extraction():
    """Run complete extraction from all 1,340 songs."""
    extractor = ThiruppugazhExtractorWithCSV()
    
    print("🕉️ COMPLETE THIRUPPUGAZH EXTRACTION - ALL 1,340 SONGS")
    print("=" * 70)
    print("This will systematically extract from ALL songs as requested")
    print("URL pattern: https://kaumaram.com/thiru/nnt000X_u.html#english")
    print("Where X ranges from 6 to 1340")
    print("Estimated time: 2-3 hours")
    
    proceed = input("\nProceed with complete extraction? (y/n): ").strip().lower()
    if proceed != 'y':
        print("Extraction cancelled.")
        return
    
    print("\n🚀 STARTING COMPLETE EXTRACTION...")
    start_time = time.time()
    
    # Process in batches of 100 for manageable progress tracking
    all_names = []
    batch_size = 100
    
    for batch_start in range(6, 1341, batch_size):
        batch_end = min(batch_start + batch_size - 1, 1340)
        
        print(f"\n🎵 PROCESSING BATCH: Songs {batch_start} to {batch_end}")
        print("-" * 50)
        
        batch_names = extractor.extract_batch(batch_start, batch_end)
        all_names.extend(batch_names)
        
        # Save intermediate progress
        if len(all_names) > 0:
            intermediate_csv = f"thiruppugazh_progress_up_to_{batch_end}.csv"
            extractor.extracted_names = all_names
            extractor.export_to_csv(intermediate_csv)
            print(f"   💾 Intermediate progress saved: {intermediate_csv}")
        
        # Progress report
        elapsed = time.time() - start_time
        print(f"   📊 Progress: {batch_end-5}/{1340-5} songs ({((batch_end-5)/(1340-5)*100):.1f}%)")
        print(f"   ⏱️  Elapsed: {elapsed/60:.1f} minutes")
        print(f"   📿 Names so far: {len(all_names)}")
        
        # Small break between batches
        time.sleep(2)
    
    # Final processing
    extractor.extracted_names = all_names
    
    print(f"\n🏆 COMPLETE EXTRACTION FINISHED!")
    elapsed = time.time() - start_time
    print(f"   ⏱️  Total time: {elapsed/60:.1f} minutes ({elapsed/3600:.1f} hours)")
    print(f"   📿 Total names extracted: {len(all_names)}")
    
    # Export final results
    print(f"\n💾 GENERATING FINAL OUTPUTS...")
    
    # Main CSV with song numbers as requested
    csv_file = extractor.export_to_csv('COMPLETE_THIRUPPUGAZH_ALL_SONGS_WITH_NUMBERS.csv')
    print(f"   ✅ Main CSV: COMPLETE_THIRUPPUGAZH_ALL_SONGS_WITH_NUMBERS.csv")
    
    # Summary report
    summary = extractor.generate_summary()
    with open('COMPLETE_THIRUPPUGAZH_EXTRACTION_REPORT.txt', 'w', encoding='utf-8') as f:
        f.write(summary)
    print(f"   ✅ Summary: COMPLETE_THIRUPPUGAZH_EXTRACTION_REPORT.txt")
    
    print(summary)
    
    print(f"\n🎯 MISSION ACCOMPLISHED!")
    print(f"   From inadequate 20 names to comprehensive extraction from ALL 1,340 songs")
    print(f"   CSV includes exact song number (X) for each name as requested")
    print(f"   Perfect for your son's naming with complete source traceability")

def run_extended_test():
    """Run extended test on more songs."""
    extractor = ThiruppugazhExtractorWithCSV()
    
    print("🧪 EXTENDED TEST EXTRACTION")
    print("=" * 40)
    print("Testing on songs 6-200 for validation...")
    
    names = extractor.extract_batch(6, 200)
    
    if names:
        csv_file = extractor.export_to_csv('EXTENDED_TEST_THIRUPPUGAZH_WITH_NUMBERS.csv')
        summary = extractor.generate_summary()
        
        with open('EXTENDED_TEST_REPORT.txt', 'w', encoding='utf-8') as f:
            f.write(summary)
        
        print(summary)
        
        # Estimate for full extraction
        names_per_song = len(names) / 195  # 195 songs tested
        estimated_total = names_per_song * 1334  # Total songs to process
        
        print(f"\n📊 FULL EXTRACTION ESTIMATE:")
        print(f"   Names per song (avg): {names_per_song:.2f}")
        print(f"   Estimated total names: {estimated_total:.0f}")
        print(f"   This would be a MASSIVE improvement over 20 names!")
        
        proceed = input(f"\nProceed with full extraction? (y/n): ").strip().lower()
        if proceed == 'y':
            run_complete_extraction()
    else:
        print("❌ Extended test failed. Check connectivity.")

def main():
    """Main function with options."""
    print("🕉️ COMPLETE THIRUPPUGAZH EXTRACTION SYSTEM")
    print("=" * 50)
    
    choice = input("""
Select extraction mode:
1. Complete extraction (ALL 1,340 songs) - 2-3 hours
2. Extended test (songs 6-200) - 30 minutes  
3. Quick test (songs 6-50) - 5 minutes

Choice (1/2/3): """).strip()
    
    if choice == '1':
        run_complete_extraction()
    elif choice == '2':
        run_extended_test()
    elif choice == '3':
        extractor = ThiruppugazhExtractorWithCSV()
        names = extractor.extract_batch(6, 50)
        if names:
            extractor.export_to_csv('QUICK_TEST_WITH_NUMBERS.csv')
            print(extractor.generate_summary())
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()