#!/usr/bin/env python3
"""
Extract Only Unique Names from Skanda Purana CSV
Remove duplicates and create clean unique names database
"""

import pandas as pd
import csv
from collections import Counter
from datetime import datetime

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
        return
    
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
            try:
                # Extract confidence from Notes column
                notes = str(row['Notes'])
                if 'Confidence:' in notes:
                    conf_str = notes.split('Confidence:')[1].strip().split(',')[0].strip()
                    confidence = float(conf_str)
                else:
                    confidence = 0.5  # Default
                confidences.append((confidence, idx))
            except:
                confidences.append((0.5, idx))
        
        # Get the entry with highest confidence
        best_confidence, best_idx = max(confidences)
        best_entry = group.loc[best_idx].copy()
        
        # Add frequency information
        best_entry['Frequency'] = len(group)
        unique_entries.append(best_entry)
    
    # Create unique dataframe
    unique_df = pd.DataFrame(unique_entries)
    unique_df = unique_df.drop('name_lower', axis=1)
    
    print(f"✅ Unique names extracted: {len(unique_df)}")
    print(f"📉 Duplicates removed: {len(df) - len(unique_df)}")
    
    # Sort by frequency (most common first), then by confidence
    unique_df['confidence_score'] = 0.5
    for idx, row in unique_df.iterrows():
        try:
            notes = str(row['Notes'])
            if 'Confidence:' in notes:
                conf_str = notes.split('Confidence:')[1].strip().split(',')[0].strip()
                unique_df.at[idx, 'confidence_score'] = float(conf_str)
        except:
            pass
    
    # Sort by frequency and confidence
    unique_df = unique_df.sort_values(['Frequency', 'confidence_score'], ascending=[False, False])
    
    # Add columns in desired order
    column_order = [
        'Name/Word', 'Script Type', 'Found Form', 'Language',
        'Monier Williams Meaning', 'Etymology', 'Frequency',
        'Page#', 'Part#', 'Context/Line#', 
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
    top_names = unique_df.head(20)
    print("🏆 TOP 20 MOST FREQUENT UNIQUE NAMES:")
    for idx, row in top_names.iterrows():
        name = row['Name/Word']
        freq = row['Frequency']
        conf = row['confidence_score']
        print(f"   {name}: {freq} occurrences (confidence: {conf:.1f})")
    
    # Statistics by type
    print(f"\n📈 DISTRIBUTION BY TYPE:")
    type_counts = unique_df['Proper Noun/Epithet/Place'].value_counts()
    for name_type, count in type_counts.items():
        percentage = (count / len(unique_df)) * 100
        print(f"   {name_type.replace('_', ' ').title()}: {count} ({percentage:.1f}%)")
    
    # High confidence names
    high_conf = unique_df[unique_df['confidence_score'] >= 0.8]
    print(f"\n🎯 HIGH CONFIDENCE NAMES (≥0.8): {len(high_conf)}")
    
    # Important Skanda-related names
    important_keywords = ['skanda', 'siva', 'karttikeya', 'subrahmanya', 'shanmukha', 'kumara']
    important_names = unique_df[unique_df['Name/Word'].str.lower().isin(important_keywords)]
    print(f"🕉️  CORE SKANDA NAMES FOUND: {len(important_names)}")
    
    if len(important_names) > 0:
        print("   Core names:")
        for idx, row in important_names.iterrows():
            print(f"   - {row['Name/Word']}: {row['Frequency']} occurrences")
    
    # Generate summary report
    report = f"""
🕉️ UNIQUE SKANDA PURANA NAMES EXTRACTION REPORT 🕉️
{'='*60}

SUMMARY:
Original Entries: {len(df):,}
Unique Names: {len(unique_df):,}
Duplicates Removed: {len(df) - len(unique_df):,}
Reduction: {((len(df) - len(unique_df)) / len(df) * 100):.1f}%

HIGH VALUE NAMES:
High Confidence (≥0.8): {len(high_conf)}
Core Skanda Names: {len(important_names)}

TOP 10 MOST FREQUENT NAMES:
"""
    
    for idx, row in unique_df.head(10).iterrows():
        report += f"{row['Name/Word']}: {row['Frequency']} occurrences\n"
    
    report += f"""
EXTRACTION COMPLETED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📄 Output File: {output_file}
🎯 Ready for authentic Sanskrit baby naming!
"""
    
    # Save report
    with open('UNIQUE_SKANDA_NAMES_REPORT.txt', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("\n✅ UNIQUE EXTRACTION COMPLETE!")
    print(f"📄 Unique CSV: {output_file}")
    print("📊 Report: UNIQUE_SKANDA_NAMES_REPORT.txt")
    
    return unique_df

def create_filtered_by_pattern():
    """Create additional filtered versions by starting pattern."""
    
    print("\n🔍 Creating pattern-specific unique files...")
    
    try:
        df = pd.read_csv('UNIQUE_SKANDA_PURANA_NAMES.csv')
    except:
        print("❌ Unique CSV not found. Run main extraction first.")
        return
    
    patterns = {
        'Cha_Ca_Names': r'^[Cc][haā]',
        'Sa_Names': r'^[Ss][aā]?',
        'Sha_Names': r'^[ŚśSs]h[aā]',
        'Se_Names': r'^[Ss]e',
        'Che_Names': r'^[Cc]he',
        'Chi_Names': r'^[Cc]hi'
    }
    
    for pattern_name, pattern in patterns.items():
        filtered_df = df[df['Name/Word'].str.contains(pattern, case=False, na=False)]
        
        if len(filtered_df) > 0:
            output_file = f"UNIQUE_SKANDA_{pattern_name.upper()}.csv"
            filtered_df.to_csv(output_file, index=False, encoding='utf-8')
            print(f"📄 {pattern_name}: {len(filtered_df)} names -> {output_file}")

if __name__ == "__main__":
    # Extract unique names
    unique_df = extract_unique_names()
    
    if unique_df is not None:
        # Create pattern-specific files
        create_filtered_by_pattern()
        
        print("\n🎉 ALL UNIQUE EXTRACTIONS COMPLETE!")
        print("=" * 60)