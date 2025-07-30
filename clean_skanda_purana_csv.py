#!/usr/bin/env python3
"""
Clean Skanda Purana CSV by removing non-Sanskrit/Tamil origin English words
Remove rows containing common English words that are not authentic Sanskrit/Tamil names
"""

import pandas as pd
import re

def clean_skanda_purana_csv():
    """Clean the Skanda Purana CSV by removing non-authentic entries."""
    
    print("🧹 CLEANING SKANDA PURANA CSV - REMOVING NON-SANSKRIT/TAMIL ENTRIES")
    print("="*70)
    
    try:
        # Load the CSV
        df = pd.read_csv('AUTHENTIC_SANSKRIT_BABY_NAMES.csv')
        print(f"✅ Loaded original CSV: {len(df)} entries")
        
        # Define common English words that are NOT Sanskrit/Tamil names
        english_words_to_remove = {
            # Common English words the user mentioned
            'someone', 'sexual', 'semen', 'speak',
            
            # Additional common English words that shouldn't be baby names
            'service', 'secret', 'seat', 'seek', 'sent', 'save', 'cast', 'carry',
            'capable', 'separation', 'subjects', 'similarly', 'satisfaction', 
            'special', 'southern', 'sleep', 'sixty', 'storehouse', 'songs',
            'castes', 'choose', 'souls', 'spiritual', 'solar', 'sinless',
            'support', 'similar', 'small', 'scriptures', 'sword', 'stand',
            'soon', 'suddenly', 'characteristics', 'sharp', 'sixteen', 'shrines',
            'skull', 'split', 'source', 'show', 'stars', 'sport', 'camphor',
            'sandal', 'staff', 'single', 'sound', 'sweet', 'sacrifice', 'state',
            'supreme', 'splendour', 'shrine', 'struck', 'still', 'sinful',
            'slayer', 'charitable', 'seventh', 'season', 'speech', 'chiefs',
            'sacrificial', 'serve', 'sole', 'south'
        }
        
        # Convert to lowercase for case-insensitive matching
        english_words_lower = {word.lower() for word in english_words_to_remove}
        
        # Create a function to check if a name is likely an English word
        def is_likely_english_word(name):
            if pd.isna(name):
                return False
            
            name_lower = str(name).lower().strip()
            
            # Direct match with known English words
            if name_lower in english_words_lower:
                return True
            
            # Check for common English word patterns (but preserve authentic Sanskrit)
            # Only flag obvious English words, not Sanskrit words that might look similar
            common_english_patterns = [
                r'^(the|and|but|for|are|all|any|can|had|her|was|one|our|out|day|get|has|him|his|how|man|new|now|old|see|two|way|who|boy|did|its|let|put|say|she|too|use)$',
                r'^(about|after|again|back|could|every|first|from|great|group|hand|help|here|high|just|know|last|left|life|live|long|make|more|most|move|much|name|need|never|next|only|open|over|part|place|right|same|seem|show|small|such|take|than|that|them|they|this|time|very|water|well|were|what|when|where|which|while|work|would|write|year|years|young)$'
            ]
            
            for pattern in common_english_patterns:
                if re.match(pattern, name_lower):
                    return True
            
            return False
        
        # Filter out rows with English words as names
        initial_count = len(df)
        df_filtered = df[~df['Name'].apply(is_likely_english_word)]
        removed_count = initial_count - len(df_filtered)
        
        print(f"🗑️  Removed {removed_count} non-authentic entries")
        print(f"✅ Remaining authentic names: {len(df_filtered)}")
        
        # Show some examples of removed entries
        removed_entries = df[df['Name'].apply(is_likely_english_word)]['Name'].unique()[:10]
        if len(removed_entries) > 0:
            print(f"\n📋 Examples of removed entries: {', '.join(removed_entries)}")
        
        # Save the cleaned CSV
        output_file = 'CLEANED_AUTHENTIC_SANSKRIT_BABY_NAMES.csv'
        df_filtered.to_csv(output_file, index=False)
        print(f"\n💾 Saved cleaned CSV: {output_file}")
        
        # Print statistics
        print(f"\n📊 CLEANING STATISTICS:")
        print(f"   Original entries: {initial_count}")
        print(f"   Removed entries:  {removed_count}")
        print(f"   Clean entries:    {len(df_filtered)}")
        print(f"   Retention rate:   {(len(df_filtered)/initial_count)*100:.1f}%")
        
        # Show pattern distribution in cleaned data
        pattern_counts = df_filtered['Starting_Pattern'].value_counts()
        print(f"\n🔤 PATTERN DISTRIBUTION IN CLEANED DATA:")
        for pattern, count in pattern_counts.items():
            print(f"   {pattern}: {count} names")
        
        return df_filtered
        
    except FileNotFoundError:
        print("❌ AUTHENTIC_SANSKRIT_BABY_NAMES.csv not found!")
        return None
    except Exception as e:
        print(f"❌ Error cleaning CSV: {e}")
        return None

if __name__ == "__main__":
    cleaned_df = clean_skanda_purana_csv()
    if cleaned_df is not None:
        print(f"\n🎉 CLEANING COMPLETE!")
        print(f"📄 Clean file: CLEANED_AUTHENTIC_SANSKRIT_BABY_NAMES.csv")
        print(f"🎯 Ready with {len(cleaned_df)} authentic Sanskrit/Tamil names for your son!")