#!/usr/bin/env python3
"""
Extract Only Unique Names from Skanda Purana CSV - Fixed Version
Remove duplicates and create clean unique names database
"""

import pandas as pd
import csv
import re
from collections import Counter
from datetime import datetime

def extract_confidence_from_notes(notes_str):
    """Extract confidence score from Notes column."""
    try:
        if 'Confidence:' in str(notes_str):
            conf_str = str(notes_str).split('Confidence:')[1].strip().split(',')[0].strip()
            return float(conf_str)
        else:
            return 0.5  # Default confidence
    except:
        return 0.5

def extract_unique_names():
    """Extract unique names from the complete Skanda Purana extraction."""
    
    print("🔍 EXTRACTING UNIQUE NAMES FROM SKANDA PURANA DATABASE")
    print("="*60)
    
    # Read the complete CSV
    try:
        df = pd.read_csv('COMPLETE_SKANDA_PURANA_NAMES_EXTRACTED.csv')
        print(f"✅ Loaded complete database: {len(df)} total entries")
    except FileNotFoundError:
        print("❌ Complete CSV file not found!")
        return None
    
    print(f"📊 Original database contains: {len(df)} entries")
    
    # Remove duplicates based on Name/Word (case-insensitive)
    print("\n🧹 Removing duplicates...")
    
    # Convert names to lowercase for comparison but keep original case
    df['name_lower'] = df['Name/Word'].str.lower()
    
    # For each unique name (case-insensitive), keep the entry with highest confidence
    unique_entries = []
    
    # Group by lowercase name
    grouped = df.groupby('name_lower')
    
    for name_lower, group in grouped:
        # Extract confidence scores from Notes column
        confidences = []
        for idx, row in group.iterrows():
            confidence = extract_confidence_from_notes(row['Notes'])
            confidences.append((confidence, idx))
        
        # Get the entry with highest confidence
        best_confidence, best_idx = max(confidences)
        best_entry = group.loc[best_idx].copy()
        
        # Add frequency information
        best_entry['Frequency'] = len(group)
        best_entry['Confidence_Score'] = best_confidence
        unique_entries.append(best_entry)
    
    # Create unique dataframe
    unique_df = pd.DataFrame(unique_entries)
    unique_df = unique_df.drop('name_lower', axis=1)
    
    print(f"✅ Unique names extracted: {len(unique_df)}")
    print(f"📉 Duplicates removed: {len(df) - len(unique_df)}")
    
    # Sort by frequency (most common first), then by confidence
    unique_df = unique_df.sort_values(['Frequency', 'Confidence_Score'], ascending=[False, False])
    
    # Reorder columns
    column_order = [
        'Name/Word', 'Frequency', 'Confidence_Score', 'Script Type', 'Found Form', 'Language',
        'Monier Williams Meaning', 'Etymology', 'Page#', 'Part#', 'Context/Line#', 
        'Proper Noun/Epithet/Place', 'Notes'
    ]
    
    unique_df = unique_df[column_order]
    
    # Export unique names CSV
    output_file = 'UNIQUE_SKANDA_PURANA_NAMES.csv'
    unique_df.to_csv(output_file, index=False, encoding='utf-8')
    
    print(f"📄 Exported unique names to: {output_file}")
    
    # Generate statistics
    print("\n📊 UNIQUE NAMES STATISTICS:")
    print("-" * 40)
    
    # Most frequent names
    top_names = unique_df.head(25)
    print("🏆 TOP 25 MOST FREQUENT UNIQUE NAMES:")
    for idx, row in top_names.iterrows():
        name = row['Name/Word']
        freq = row['Frequency']
        conf = row['Confidence_Score']
        name_type = row['Proper Noun/Epithet/Place'][:15] + "..." if len(row['Proper Noun/Epithet/Place']) > 15 else row['Proper Noun/Epithet/Place']
        print(f"   {name:15} : {freq:4d} occurrences (conf: {conf:.1f}) [{name_type}]")
    
    # Statistics by type
    print(f"\n📈 DISTRIBUTION BY TYPE:")
    type_counts = unique_df['Proper Noun/Epithet/Place'].value_counts()
    for name_type, count in type_counts.items():
        percentage = (count / len(unique_df)) * 100
        print(f"   {name_type.replace('_', ' ').title():20}: {count:4d} ({percentage:.1f}%)")
    
    # High confidence names
    high_conf = unique_df[unique_df['Confidence_Score'] >= 0.8]
    print(f"\n🎯 HIGH CONFIDENCE NAMES (≥0.8): {len(high_conf)}")
    
    # Very high frequency names (for baby naming)
    high_freq = unique_df[unique_df['Frequency'] >= 20]
    print(f"🔥 HIGH FREQUENCY NAMES (≥20 occurrences): {len(high_freq)}")
    
    # Important Skanda-related names
    important_keywords = ['skanda', 'siva', 'karttikeya', 'subrahmanya', 'shanmukha', 'kumara', 'sarva', 'saravana']
    important_names = unique_df[unique_df['Name/Word'].str.lower().isin(important_keywords)]
    print(f"🕉️  CORE SKANDA NAMES FOUND: {len(important_names)}")
    
    if len(important_names) > 0:
        print("   Core names:")
        for idx, row in important_names.iterrows():
            print(f"   - {row['Name/Word']:12}: {row['Frequency']:4d} occurrences (conf: {row['Confidence_Score']:.1f})")
    
    # Best names for baby naming (high frequency + high confidence)
    best_names = unique_df[
        (unique_df['Frequency'] >= 10) & 
        (unique_df['Confidence_Score'] >= 0.7) &
        (unique_df['Name/Word'].str.len() >= 4) &
        (unique_df['Name/Word'].str.len() <= 15)
    ].head(50)
    
    print(f"\n👶 BEST NAMES FOR BABY NAMING: {len(best_names)}")
    print("   (High frequency ≥10, High confidence ≥0.7, Reasonable length)")
    
    # Generate summary report
    report = f"""
🕉️ UNIQUE SKANDA PURANA NAMES EXTRACTION REPORT 🕉️
{'='*70}

SUMMARY:
Original Entries: {len(df):,}
Unique Names: {len(unique_df):,}
Duplicates Removed: {len(df) - len(unique_df):,}
Reduction: {((len(df) - len(unique_df)) / len(df) * 100):.1f}%

QUALITY METRICS:
High Confidence (≥0.8): {len(high_conf):,}
High Frequency (≥20): {len(high_freq):,}
Core Skanda Names: {len(important_names)}
Best Baby Names: {len(best_names)}

TOP 15 MOST FREQUENT NAMES:
{'-'*40}
"""
    
    for idx, row in unique_df.head(15).iterrows():
        report += f"{row['Name/Word']:15}: {row['Frequency']:4d} occurrences (conf: {row['Confidence_Score']:.1f})\n"
    
    if len(important_names) > 0:
        report += f"\nCORE SKANDA NAMES FOUND:\n{'-'*25}\n"
        for idx, row in important_names.iterrows():
            report += f"{row['Name/Word']:12}: {row['Frequency']:4d} occurrences\n"
    
    if len(best_names) > 0:
        report += f"\nTOP 20 BEST BABY NAMES:\n{'-'*25}\n"
        for idx, row in best_names.head(20).iterrows():
            report += f"{row['Name/Word']:15}: {row['Frequency']:3d} freq, {row['Confidence_Score']:.1f} conf\n"
    
    report += f"""
EXTRACTION COMPLETED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📄 Output File: {output_file}
🎯 Ready for authentic Sanskrit baby naming with {len(unique_df):,} unique names!
"""
    
    # Save report
    with open('UNIQUE_SKANDA_NAMES_REPORT.txt', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(report)
    
    return unique_df

def create_baby_naming_csv(unique_df):
    """Create a special CSV focused on baby naming."""
    if unique_df is None:
        return
    
    print("\n👶 Creating baby naming focused CSV...")
    
    # Filter for best baby names
    baby_names = unique_df[
        (unique_df['Frequency'] >= 5) & 
        (unique_df['Confidence_Score'] >= 0.6) &
        (unique_df['Name/Word'].str.len() >= 3) &
        (unique_df['Name/Word'].str.len() <= 20) &
        (~unique_df['Name/Word'].str.lower().isin(['seen', 'seven', 'same', 'self', 'sins', 'spot']))  # Remove common words
    ]
    
    # Create simplified columns for baby naming
    baby_df = baby_names[['Name/Word', 'Frequency', 'Confidence_Score', 'Monier Williams Meaning', 'Proper Noun/Epithet/Place']].copy()
    baby_df = baby_df.rename(columns={
        'Name/Word': 'Name',
        'Proper Noun/Epithet/Place': 'Type',
        'Monier Williams Meaning': 'Meaning'
    })
    
    # Sort by a combination of frequency and confidence
    baby_df['Score'] = baby_df['Frequency'] * baby_df['Confidence_Score']
    baby_df = baby_df.sort_values('Score', ascending=False)
    
    baby_df.to_csv('SKANDA_BABY_NAMES.csv', index=False, encoding='utf-8')
    
    print(f"👶 Baby naming CSV created: SKANDA_BABY_NAMES.csv ({len(baby_df)} names)")
    
    return baby_df

if __name__ == "__main__":
    # Extract unique names
    unique_df = extract_unique_names()
    
    if unique_df is not None:
        # Create baby naming focused CSV
        baby_df = create_baby_naming_csv(unique_df)
        
        print("\n🎉 ALL UNIQUE EXTRACTIONS COMPLETE!")
        print("=" * 60)
        print("📄 Files created:")
        print("   - UNIQUE_SKANDA_PURANA_NAMES.csv (complete unique database)")
        print("   - SKANDA_BABY_NAMES.csv (baby naming focused)")
        print("   - UNIQUE_SKANDA_NAMES_REPORT.txt (detailed report)")
        print(f"\n🎯 Ready for your son's authentic Sanskrit naming from {len(unique_df):,} unique names!")