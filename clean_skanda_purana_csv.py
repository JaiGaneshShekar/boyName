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
            'someone', 'sexual', 'semen', 'speak', 'sports', 'search', 'stage', 'separate', 'seventy', 'species',
            
            # Additional English words found in data
            'slowly', 'sand', 'suns', 'carefully', 'seasons', 'sunday', 'sundays', 'seems', 'salute', 'sacrifices',
            'subtle', 'spirit', 'scrupulously', 'swan', 'surely', 'succinctly', 'swans', 'salt', 'sire', 'sandals',
            'characteristic', 'slain', 'smoke', 'slave', 'capital', 'supernatural', 'star', 'simultaneously',
            'science', 'somehow', 'skulls', 'slay', 'sanctify', 'seventeen', 'showers', 'swords', 'saturn',
            'spear', 'chapters', 'shadow', 'sanctifier', 'seer', 'scholars', 'stupid', 'smilingly', 'sands',
            'snow', 'signs', 'sapphire', 'chastiser', 'saturday', 'slumber', 'submarine', 'studies', 'subdue',
            'sphere', 'seers', 'chap',
            
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
            'sacrificial', 'serve', 'sole', 'south',
            
            # More comprehensive English words
            'against', 'always', 'among', 'around', 'became', 'become', 'before',
            'began', 'being', 'below', 'between', 'both', 'called', 'came',
            'cannot', 'change', 'come', 'could', 'course', 'during', 'each',
            'early', 'found', 'give', 'given', 'going', 'good', 'great',
            'group', 'hand', 'head', 'help', 'here', 'high', 'home', 'house',
            'however', 'important', 'including', 'information', 'into', 'itself',
            'keep', 'kind', 'know', 'known', 'large', 'last', 'late', 'later',
            'learn', 'leave', 'left', 'less', 'level', 'line', 'little', 'live',
            'living', 'local', 'long', 'look', 'made', 'make', 'making', 'many',
            'may', 'mean', 'members', 'might', 'mind', 'money', 'more', 'most',
            'move', 'much', 'must', 'near', 'need', 'never', 'next', 'night',
            'nothing', 'now', 'number', 'often', 'old', 'only', 'open', 'order',
            'other', 'others', 'over', 'own', 'part', 'people', 'person', 'place',
            'point', 'possible', 'present', 'problem', 'program', 'provide',
            'public', 'put', 'quite', 'real', 'really', 'result', 'right',
            'room', 'said', 'same', 'school', 'second', 'see', 'seem', 'seen',
            'several', 'short', 'since', 'small', 'social', 'some', 'something',
            'state', 'still', 'such', 'system', 'take', 'than', 'that', 'their',
            'them', 'then', 'there', 'these', 'they', 'thing', 'think', 'this',
            'those', 'though', 'three', 'through', 'time', 'today', 'together',
            'under', 'until', 'upon', 'used', 'using', 'very', 'want', 'water',
            'way', 'ways', 'well', 'were', 'what', 'when', 'where', 'which',
            'while', 'white', 'will', 'with', 'within', 'without', 'work',
            'would', 'year', 'years', 'young',
            
            # Additional terms that appeared in the data
            'above', 'across', 'after', 'again', 'along', 'already', 'also',
            'although', 'another', 'any', 'anyone', 'anything', 'appear',
            'area', 'ask', 'asked', 'asking', 'asks', 'away', 'back', 'bad',
            'based', 'basic', 'beautiful', 'began', 'begin', 'behind', 'best',
            'better', 'big', 'black', 'body', 'book', 'bring', 'building',
            'business', 'call', 'can', 'care', 'carry', 'case', 'certain',
            'check', 'child', 'children', 'city', 'clear', 'close', 'college',
            'color', 'community', 'company', 'complete', 'consider', 'continue',
            'control', 'cost', 'country', 'couple', 'create', 'current', 'cut',
            'data', 'day', 'days', 'decide', 'development', 'did', 'die',
            'different', 'difficult', 'do', 'does', 'done', 'door', 'down',
            'drive', 'eat', 'economic', 'education', 'effect', 'end', 'enough',
            'entire', 'even', 'evening', 'ever', 'every', 'everyone', 'everything',
            'example', 'experience', 'explain', 'eye', 'eyes', 'face', 'fact',
            'family', 'far', 'feel', 'few', 'field', 'fight', 'figure', 'fill',
            'final', 'finally', 'find', 'fine', 'fire', 'first', 'five', 'focus',
            'follow', 'food', 'foot', 'for', 'force', 'form', 'former', 'four',
            'free', 'friend', 'friends', 'from', 'front', 'full', 'future',
            'game', 'general', 'get', 'girl', 'glass', 'go', 'goal', 'god',
            'goes', 'gone', 'got', 'government', 'ground', 'grow', 'growth',
            'guy', 'had', 'hair', 'half', 'hand', 'happen', 'hard', 'has',
            'have', 'he', 'hear', 'heart', 'heavy', 'her', 'herself', 'him',
            'himself', 'his', 'history', 'hit', 'hold', 'hope', 'hour', 'hours',
            'how', 'human', 'hundred', 'idea', 'identify', 'if', 'image',
            'imagine', 'immediately', 'impact', 'increase', 'indeed', 'industry',
            'inside', 'instead', 'interest', 'international', 'investment',
            'involve', 'issue', 'issues', 'it', 'its', 'job', 'just', 'key',
            'kill', 'kind', 'kitchen', 'land', 'language', 'law', 'lay', 'lead',
            'leader', 'learn', 'least', 'led', 'legal', 'let', 'letter', 'lie',
            'life', 'light', 'like', 'likely', 'limited', 'list', 'listen',
            'look', 'lose', 'loss', 'lot', 'love', 'low', 'machine', 'main',
            'maintain', 'major', 'man', 'manage', 'management', 'manager',
            'market', 'marriage', 'material', 'matter', 'maybe', 'me', 'mean',
            'measure', 'media', 'medical', 'meet', 'meeting', 'member', 'memory',
            'method', 'middle', 'military', 'million', 'minute', 'miss', 'model',
            'modern', 'moment', 'month', 'months', 'morning', 'mother', 'mouth',
            'movement', 'movie', 'music', 'my', 'myself', 'name', 'nation',
            'national', 'natural', 'nature', 'necessary', 'net', 'network',
            'new', 'news', 'nice', 'no', 'none', 'nor', 'north', 'not', 'note',
            'now', 'object', 'occur', 'of', 'off', 'offer', 'office', 'officer',
            'official', 'oh', 'oil', 'ok', 'on', 'once', 'one', 'online', 'only',
            'onto', 'opportunity', 'option', 'or', 'organization', 'original',
            'other', 'our', 'out', 'outside', 'over', 'own', 'page', 'paper',
            'parent', 'parents', 'part', 'particular', 'particularly', 'partner',
            'party', 'pass', 'past', 'pay', 'peace', 'performance', 'perhaps',
            'period', 'person', 'personal', 'phone', 'physical', 'pick',
            'picture', 'piece', 'plan', 'plant', 'play', 'player', 'pm',
            'policy', 'political', 'politics', 'poor', 'popular', 'population',
            'position', 'positive', 'power', 'practice', 'prepare', 'president',
            'pressure', 'pretty', 'prevent', 'price', 'private', 'probably',
            'process', 'produce', 'product', 'production', 'professional',
            'property', 'protect', 'prove', 'purpose', 'push', 'quality',
            'question', 'quickly', 'quite', 'race', 'radio', 'raise', 'range',
            'rate', 'rather', 'reach', 'read', 'ready', 'reason', 'receive',
            'recent', 'recognize', 'record', 'red', 'reduce', 'reflect',
            'region', 'relationship', 'religious', 'remain', 'remember',
            'remove', 'report', 'represent', 'republican', 'require', 'research',
            'resource', 'respond', 'response', 'responsibility', 'rest',
            'return', 'reveal', 'rich', 'rise', 'risk', 'road', 'rock', 'role',
            'rule', 'run', 'safe', 'save', 'say', 'scene', 'section', 'security',
            'sell', 'send', 'senior', 'sense', 'series', 'serious', 'service',
            'set', 'seven', 'shake', 'share', 'she', 'shoot', 'should', 'side',
            'significant', 'simple', 'simply', 'sing', 'single', 'sister', 'sit',
            'site', 'situation', 'six', 'size', 'skill', 'skin', 'something',
            'sometimes', 'son', 'song', 'soon', 'sort', 'sound', 'source',
            'space', 'speak', 'special', 'specific', 'spend', 'spent', 'staff',
            'stage', 'standard', 'start', 'station', 'stay', 'step', 'stock',
            'stop', 'store', 'story', 'strategy', 'street', 'strong', 'structure',
            'student', 'study', 'stuff', 'style', 'subject', 'success',
            'successful', 'suddenly', 'suggest', 'summer', 'support', 'sure',
            'surface', 'table', 'talk', 'task', 'tax', 'teach', 'teacher',
            'team', 'technology', 'television', 'tell', 'ten', 'term', 'test',
            'text', 'thank', 'thanks', 'the', 'their', 'themselves', 'theory',
            'they', 'think', 'third', 'thirty', 'though', 'thought', 'thousand',
            'threat', 'throughout', 'throw', 'thus', 'til', 'to', 'today',
            'together', 'tonight', 'too', 'top', 'total', 'tough', 'toward',
            'towards', 'town', 'trade', 'traditional', 'training', 'travel',
            'treat', 'treatment', 'tree', 'trial', 'trip', 'trouble', 'true',
            'truth', 'try', 'turn', 'tv', 'twenty', 'two', 'type', 'understand',
            'union', 'unit', 'united', 'university', 'up', 'upon', 'us', 'use',
            'usually', 'value', 'various', 'visit', 'voice', 'vote', 'wait',
            'walk', 'wall', 'war', 'watch', 'we', 'weapon', 'wear', 'week',
            'weeks', 'weight', 'welcome', 'west', 'western', 'whatever', 'whether',
            'who', 'whole', 'whose', 'why', 'wide', 'wife', 'win', 'window',
            'wish', 'woman', 'women', 'word', 'words', 'worker', 'working',
            'world', 'worry', 'worth', 'write', 'writer', 'writing', 'written',
            'wrong', 'yard', 'yeah', 'yes', 'yet', 'you', 'young', 'your',
            'yourself'
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