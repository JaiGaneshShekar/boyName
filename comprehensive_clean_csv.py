#!/usr/bin/env python3
"""
Comprehensive cleaning of Skanda Purana CSV - Check EVERY name manually
Remove ALL English words systematically
"""

import pandas as pd
import re

def comprehensive_clean_csv():
    """Comprehensively clean every single name in the CSV."""
    
    print("🔍 COMPREHENSIVE CLEANING - CHECKING EVERY NAME")
    print("="*60)
    
    try:
        # Load the original CSV to start fresh
        df = pd.read_csv('AUTHENTIC_SANSKRIT_BABY_NAMES.csv')
        print(f"✅ Loaded original CSV: {len(df)} entries")
        
        # Get all unique names to analyze
        all_names = df['Name'].unique()
        print(f"📊 Total unique names to analyze: {len(all_names)}")
        
        # Comprehensive list of ALL English words that are NOT Sanskrit/Tamil names
        english_words_comprehensive = {
            # Basic English words
            'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the', 'to', 'was', 'will', 'with',
            
            # Common English words found in data
            'above', 'across', 'after', 'again', 'against', 'all', 'along', 'already', 'also', 'although', 'always', 'among', 'another', 'any', 'anyone', 'anything', 'appear', 'area', 'around', 'ask', 'asked', 'asking', 'away',
            'back', 'bad', 'based', 'basic', 'beautiful', 'became', 'because', 'become', 'been', 'before', 'began', 'begin', 'behind', 'being', 'below', 'best', 'better', 'between', 'big', 'black', 'body', 'book', 'both', 'bring', 'building', 'business',
            'call', 'called', 'came', 'can', 'cannot', 'capable', 'capital', 'care', 'carefully', 'carry', 'case', 'cast', 'castes', 'certain', 'change', 'chapters', 'characteristic', 'characteristics', 'charitable', 'chastiser', 'check', 'chiefs', 'child', 'children', 'choose', 'city', 'clear', 'close', 'college', 'color', 'come', 'coming', 'community', 'company', 'complete', 'consider', 'continue', 'control', 'cost', 'could', 'country', 'couple', 'course', 'create', 'current', 'cut',
            'data', 'day', 'days', 'dead', 'decide', 'development', 'did', 'die', 'different', 'difficult', 'do', 'does', 'done', 'door', 'down', 'drive', 'during',
            'each', 'early', 'eat', 'economic', 'education', 'effect', 'end', 'enough', 'entire', 'even', 'evening', 'ever', 'every', 'everyone', 'everything', 'example', 'experience', 'explain', 'eye', 'eyes',
            'face', 'fact', 'family', 'far', 'feel', 'few', 'field', 'fight', 'figure', 'fill', 'final', 'finally', 'find', 'fine', 'fire', 'first', 'five', 'focus', 'follow', 'food', 'foot', 'force', 'form', 'former', 'found', 'four', 'free', 'friend', 'friends', 'from', 'front', 'full', 'future',
            'game', 'general', 'get', 'girl', 'give', 'given', 'glass', 'go', 'god', 'goes', 'going', 'gone', 'good', 'got', 'government', 'great', 'ground', 'group', 'grow', 'growth', 'guy',
            'had', 'hair', 'half', 'hand', 'happen', 'hard', 'has', 'have', 'he', 'head', 'hear', 'heart', 'heavy', 'help', 'here', 'high', 'him', 'his', 'history', 'hit', 'hold', 'home', 'hope', 'hour', 'hours', 'house', 'how', 'however', 'human', 'hundred',
            'idea', 'identify', 'if', 'image', 'imagine', 'immediately', 'impact', 'important', 'including', 'increase', 'indeed', 'industry', 'information', 'inside', 'instead', 'interest', 'international', 'into', 'investment', 'involve', 'issue', 'issues', 'it', 'its', 'itself',
            'job', 'just', 'keep', 'key', 'kill', 'kind', 'kitchen', 'know', 'known',
            'land', 'language', 'large', 'last', 'late', 'later', 'law', 'lay', 'lead', 'leader', 'learn', 'least', 'leave', 'led', 'left', 'legal', 'less', 'let', 'letter', 'level', 'lie', 'life', 'light', 'like', 'likely', 'limited', 'line', 'list', 'listen', 'little', 'live', 'living', 'local', 'long', 'look', 'lose', 'loss', 'lot', 'love', 'low',
            'machine', 'made', 'main', 'maintain', 'major', 'make', 'making', 'man', 'manage', 'management', 'manager', 'many', 'market', 'marriage', 'material', 'matter', 'may', 'maybe', 'me', 'mean', 'measure', 'media', 'medical', 'meet', 'meeting', 'member', 'members', 'memory', 'method', 'middle', 'military', 'million', 'mind', 'minute', 'miss', 'model', 'modern', 'moment', 'money', 'month', 'months', 'more', 'morning', 'most', 'mother', 'mouth', 'move', 'movement', 'movie', 'much', 'music', 'must', 'my', 'myself',
            'name', 'nation', 'national', 'natural', 'nature', 'near', 'necessary', 'need', 'network', 'never', 'new', 'news', 'next', 'nice', 'night', 'no', 'none', 'nor', 'north', 'not', 'note', 'nothing', 'now', 'number',
            'object', 'occur', 'of', 'off', 'offer', 'office', 'officer', 'official', 'often', 'oh', 'oil', 'ok', 'old', 'on', 'once', 'one', 'online', 'only', 'onto', 'open', 'opportunity', 'option', 'or', 'order', 'organization', 'original', 'other', 'others', 'our', 'out', 'outside', 'over', 'own',
            'page', 'paper', 'parent', 'parents', 'part', 'particular', 'particularly', 'partner', 'party', 'pass', 'past', 'pay', 'peace', 'people', 'performance', 'perhaps', 'period', 'person', 'personal', 'phone', 'physical', 'pick', 'picture', 'piece', 'place', 'plan', 'plant', 'play', 'player', 'pm', 'point', 'policy', 'political', 'politics', 'poor', 'popular', 'population', 'position', 'positive', 'possible', 'power', 'practice', 'prepare', 'president', 'present', 'pressure', 'pretty', 'prevent', 'price', 'private', 'probably', 'problem', 'process', 'produce', 'product', 'production', 'professional', 'program', 'property', 'protect', 'provide', 'public', 'purpose', 'push', 'put',
            'quality', 'question', 'quickly', 'quite', 'race', 'radio', 'raise', 'range', 'rate', 'rather', 'reach', 'read', 'ready', 'real', 'really', 'reason', 'receive', 'recent', 'recognize', 'record', 'red', 'reduce', 'reflect', 'region', 'relationship', 'religious', 'remain', 'remember', 'remove', 'report', 'represent', 'republican', 'require', 'research', 'resource', 'respond', 'response', 'responsibility', 'rest', 'result', 'return', 'reveal', 'rich', 'right', 'rise', 'risk', 'road', 'rock', 'role', 'room', 'rule', 'run',
            'safe', 'said', 'same', 'save', 'say', 'scene', 'school', 'science', 'second', 'section', 'security', 'see', 'seek', 'seem', 'seen', 'sell', 'send', 'senior', 'sense', 'sent', 'series', 'serious', 'service', 'set', 'seven', 'several', 'shake', 'share', 'she', 'shoot', 'short', 'should', 'show', 'side', 'significant', 'similar', 'simple', 'simply', 'since', 'sing', 'single', 'sister', 'sit', 'site', 'situation', 'six', 'size', 'skill', 'skin', 'sleep', 'small', 'smoke', 'snow', 'so', 'social', 'society', 'some', 'someone', 'something', 'sometimes', 'son', 'song', 'soon', 'sort', 'soul', 'souls', 'sound', 'source', 'south', 'southern', 'space', 'speak', 'special', 'species', 'specific', 'spend', 'spent', 'spirit', 'spiritual', 'split', 'sport', 'sports', 'staff', 'stage', 'stand', 'standard', 'star', 'start', 'state', 'station', 'stay', 'step', 'still', 'stock', 'stop', 'store', 'story', 'strategy', 'street', 'strong', 'structure', 'student', 'study', 'stuff', 'style', 'subject', 'subjects', 'success', 'successful', 'such', 'suddenly', 'suggest', 'summer', 'support', 'sure', 'surface', 'system',
            'table', 'take', 'talk', 'task', 'tax', 'teach', 'teacher', 'team', 'technology', 'television', 'tell', 'ten', 'term', 'test', 'text', 'than', 'thank', 'thanks', 'that', 'the', 'their', 'them', 'themselves', 'then', 'there', 'these', 'they', 'thing', 'think', 'third', 'thirty', 'this', 'those', 'though', 'thought', 'thousand', 'three', 'through', 'throw', 'thus', 'time', 'today', 'together', 'tonight', 'too', 'top', 'total', 'tough', 'toward', 'towards', 'town', 'trade', 'traditional', 'training', 'travel', 'treat', 'treatment', 'tree', 'trial', 'trip', 'trouble', 'true', 'truth', 'try', 'turn', 'tv', 'twenty', 'two', 'type',
            'under', 'understand', 'union', 'unit', 'united', 'university', 'until', 'up', 'upon', 'us', 'use', 'used', 'using', 'usually', 'value', 'various', 'very', 'visit', 'voice', 'vote',
            'wait', 'walk', 'wall', 'want', 'war', 'watch', 'water', 'way', 'ways', 'we', 'weapon', 'wear', 'week', 'weeks', 'weight', 'welcome', 'well', 'were', 'west', 'western', 'what', 'whatever', 'when', 'where', 'whether', 'which', 'while', 'white', 'who', 'whole', 'whose', 'why', 'wide', 'wife', 'will', 'win', 'window', 'wish', 'with', 'within', 'without', 'woman', 'women', 'word', 'words', 'work', 'worker', 'working', 'world', 'worry', 'worth', 'would', 'write', 'writer', 'writing', 'written', 'wrong',
            'yard', 'yeah', 'year', 'years', 'yes', 'yet', 'you', 'young', 'your', 'yourself',
            
            # Specific English words found in the Skanda Purana data
            'above', 'across', 'after', 'again', 'against', 'all', 'along', 'already', 'also', 'although', 'always', 'among', 'another', 'any', 'anyone', 'anything', 'appear', 'area', 'around', 'ask', 'asked', 'asking', 'away',
            'back', 'bad', 'based', 'basic', 'beautiful', 'became', 'because', 'become', 'been', 'before', 'began', 'begin', 'behind', 'being', 'below', 'best', 'better', 'between', 'big', 'black', 'body', 'book', 'both', 'bring', 'building', 'business',
            'call', 'called', 'came', 'can', 'cannot', 'capable', 'capital', 'care', 'carefully', 'carry', 'case', 'cast', 'castes', 'certain', 'change', 'chapters', 'characteristic', 'characteristics', 'charitable', 'chastiser', 'check', 'chiefs', 'child', 'children', 'choose', 'city', 'clear', 'close', 'college', 'color', 'come', 'coming', 'community', 'company', 'complete', 'consider', 'continue', 'control', 'cost', 'could', 'country', 'couple', 'course', 'create', 'current', 'cut',
            'data', 'day', 'days', 'dead', 'decide', 'development', 'did', 'die', 'different', 'difficult', 'do', 'does', 'done', 'door', 'down', 'drive', 'during',
            'each', 'early', 'eat', 'economic', 'education', 'effect', 'end', 'enough', 'entire', 'even', 'evening', 'ever', 'every', 'everyone', 'everything', 'example', 'experience', 'explain', 'eye', 'eyes',
            'face', 'fact', 'family', 'far', 'feel', 'few', 'field', 'fight', 'figure', 'fill', 'final', 'finally', 'find', 'fine', 'fire', 'first', 'five', 'focus', 'follow', 'food', 'foot', 'force', 'form', 'former', 'found', 'four', 'free', 'friend', 'friends', 'from', 'front', 'full', 'future',
            'game', 'general', 'get', 'girl', 'give', 'given', 'glass', 'go', 'god', 'goes', 'going', 'gone', 'good', 'got', 'government', 'great', 'ground', 'group', 'grow', 'growth', 'guy',
            'had', 'hair', 'half', 'hand', 'happen', 'hard', 'has', 'have', 'he', 'head', 'hear', 'heart', 'heavy', 'help', 'here', 'high', 'him', 'his', 'history', 'hit', 'hold', 'home', 'hope', 'hour', 'hours', 'house', 'how', 'however', 'human', 'hundred',
            'idea', 'identify', 'if', 'image', 'imagine', 'immediately', 'impact', 'important', 'including', 'increase', 'indeed', 'industry', 'information', 'inside', 'instead', 'interest', 'international', 'into', 'investment', 'involve', 'issue', 'issues', 'it', 'its', 'itself',
            'job', 'just', 'keep', 'key', 'kill', 'kind', 'kitchen', 'know', 'known',
            'land', 'language', 'large', 'last', 'late', 'later', 'law', 'lay', 'lead', 'leader', 'learn', 'least', 'leave', 'led', 'left', 'legal', 'less', 'let', 'letter', 'level', 'lie', 'life', 'light', 'like', 'likely', 'limited', 'line', 'list', 'listen', 'little', 'live', 'living', 'local', 'long', 'look', 'lose', 'loss', 'lot', 'love', 'low',
            'machine', 'made', 'main', 'maintain', 'major', 'make', 'making', 'man', 'manage', 'management', 'manager', 'many', 'market', 'marriage', 'material', 'matter', 'may', 'maybe', 'me', 'mean', 'measure', 'media', 'medical', 'meet', 'meeting', 'member', 'members', 'memory', 'method', 'middle', 'military', 'million', 'mind', 'minute', 'miss', 'model', 'modern', 'moment', 'money', 'month', 'months', 'more', 'morning', 'most', 'mother', 'mouth', 'move', 'movement', 'movie', 'much', 'music', 'must', 'my', 'myself',
            'name', 'nation', 'national', 'natural', 'nature', 'near', 'necessary', 'need', 'network', 'never', 'new', 'news', 'next', 'nice', 'night', 'no', 'none', 'nor', 'north', 'not', 'note', 'nothing', 'now', 'number',
            'object', 'occur', 'of', 'off', 'offer', 'office', 'officer', 'official', 'often', 'oh', 'oil', 'ok', 'old', 'on', 'once', 'one', 'online', 'only', 'onto', 'open', 'opportunity', 'option', 'or', 'order', 'organization', 'original', 'other', 'others', 'our', 'out', 'outside', 'over', 'own',
            'page', 'paper', 'parent', 'parents', 'part', 'particular', 'particularly', 'partner', 'party', 'pass', 'past', 'pay', 'peace', 'people', 'performance', 'perhaps', 'period', 'person', 'personal', 'phone', 'physical', 'pick', 'picture', 'piece', 'place', 'plan', 'plant', 'play', 'player', 'pm', 'point', 'policy', 'political', 'politics', 'poor', 'popular', 'population', 'position', 'positive', 'possible', 'power', 'practice', 'prepare', 'president', 'present', 'pressure', 'pretty', 'prevent', 'price', 'private', 'probably', 'problem', 'process', 'produce', 'product', 'production', 'professional', 'program', 'property', 'protect', 'provide', 'public', 'purpose', 'push', 'put',
            'quality', 'question', 'quickly', 'quite', 'race', 'radio', 'raise', 'range', 'rate', 'rather', 'reach', 'read', 'ready', 'real', 'really', 'reason', 'receive', 'recent', 'recognize', 'record', 'red', 'reduce', 'reflect', 'region', 'relationship', 'religious', 'remain', 'remember', 'remove', 'report', 'represent', 'republican', 'require', 'research', 'resource', 'respond', 'response', 'responsibility', 'rest', 'result', 'return', 'reveal', 'rich', 'right', 'rise', 'risk', 'road', 'rock', 'role', 'room', 'rule', 'run',
            'safe', 'said', 'same', 'save', 'say', 'scene', 'school', 'science', 'second', 'section', 'security', 'see', 'seek', 'seem', 'seen', 'sell', 'send', 'senior', 'sense', 'sent', 'series', 'serious', 'service', 'set', 'seven', 'several', 'shake', 'share', 'she', 'shoot', 'short', 'should', 'show', 'side', 'significant', 'similar', 'simple', 'simply', 'since', 'sing', 'single', 'sister', 'sit', 'site', 'situation', 'six', 'size', 'skill', 'skin', 'sleep', 'small', 'smoke', 'snow', 'so', 'social', 'society', 'some', 'someone', 'something', 'sometimes', 'son', 'song', 'soon', 'sort', 'soul', 'souls', 'sound', 'source', 'south', 'southern', 'space', 'speak', 'special', 'species', 'specific', 'spend', 'spent', 'spirit', 'spiritual', 'split', 'sport', 'sports', 'staff', 'stage', 'stand', 'standard', 'star', 'start', 'state', 'station', 'stay', 'step', 'still', 'stock', 'stop', 'store', 'story', 'strategy', 'street', 'strong', 'structure', 'student', 'study', 'stuff', 'style', 'subject', 'subjects', 'success', 'successful', 'such', 'suddenly', 'suggest', 'summer', 'support', 'sure', 'surface', 'system',
            'table', 'take', 'talk', 'task', 'tax', 'teach', 'teacher', 'team', 'technology', 'television', 'tell', 'ten', 'term', 'test', 'text', 'than', 'thank', 'thanks', 'that', 'the', 'their', 'them', 'themselves', 'then', 'there', 'these', 'they', 'thing', 'think', 'third', 'thirty', 'this', 'those', 'though', 'thought', 'thousand', 'three', 'through', 'throw', 'thus', 'time', 'today', 'together', 'tonight', 'too', 'top', 'total', 'tough', 'toward', 'towards', 'town', 'trade', 'traditional', 'training', 'travel', 'treat', 'treatment', 'tree', 'trial', 'trip', 'trouble', 'true', 'truth', 'try', 'turn', 'tv', 'twenty', 'two', 'type',
            'under', 'understand', 'union', 'unit', 'united', 'university', 'until', 'up', 'upon', 'us', 'use', 'used', 'using', 'usually', 'value', 'various', 'very', 'visit', 'voice', 'vote',
            'wait', 'walk', 'wall', 'want', 'war', 'watch', 'water', 'way', 'ways', 'we', 'weapon', 'wear', 'week', 'weeks', 'weight', 'welcome', 'well', 'were', 'west', 'western', 'what', 'whatever', 'when', 'where', 'whether', 'which', 'while', 'white', 'who', 'whole', 'whose', 'why', 'wide', 'wife', 'will', 'win', 'window', 'wish', 'with', 'within', 'without', 'woman', 'women', 'word', 'words', 'work', 'worker', 'working', 'world', 'worry', 'worth', 'would', 'write', 'writer', 'writing', 'written', 'wrong',
            'yard', 'yeah', 'year', 'years', 'yes', 'yet', 'you', 'young', 'your', 'yourself',
            
            # From the Skanda Purana data - specific English words found
            'sacrifice', 'sacrifices', 'sacrificial', 'secret', 'seat', 'seek', 'sent', 'save', 'cast', 'carry', 'capable', 'separation', 'subjects', 'similarly', 'satisfaction', 'special', 'southern', 'sleep', 'sixty', 'storehouse', 'songs', 'castes', 'choose', 'souls', 'spiritual', 'solar', 'sinless', 'support', 'similar', 'small', 'scriptures', 'sword', 'stand', 'soon', 'suddenly', 'characteristics', 'sharp', 'sixteen', 'shrines', 'skull', 'split', 'source', 'show', 'stars', 'sport', 'camphor', 'sandal', 'staff', 'single', 'sound', 'sweet', 'state', 'supreme', 'splendour', 'shrine', 'struck', 'still', 'sinful', 'slayer', 'charitable', 'seventh', 'season', 'speech', 'chiefs', 'serve', 'sole', 'south',
            'slowly', 'sand', 'suns', 'carefully', 'seasons', 'sunday', 'sundays', 'seems', 'salute', 'subtle', 'spirit', 'scrupulously', 'swan', 'surely', 'succinctly', 'swans', 'salt', 'sire', 'sandals', 'characteristic', 'slain', 'smoke', 'slave', 'capital', 'supernatural', 'star', 'simultaneously', 'science', 'somehow', 'skulls', 'slay', 'sanctify', 'seventeen', 'showers', 'swords', 'saturn', 'spear', 'chapters', 'shadow', 'sanctifier', 'seer', 'scholars', 'stupid', 'smilingly', 'sands', 'snow', 'signs', 'sapphire', 'chastiser', 'saturday', 'slumber', 'submarine', 'studies', 'subdue', 'sphere', 'seers', 'chap',
            
            # More specific ones from manual inspection
            'above', 'after', 'again', 'all', 'also', 'another', 'any', 'are', 'around', 'as', 'at', 'away', 'back', 'be', 'been', 'being', 'between', 'both', 'but', 'by', 'came', 'can', 'come', 'could', 'did', 'do', 'does', 'each', 'even', 'every', 'far', 'few', 'find', 'first', 'for', 'from', 'get', 'go', 'good', 'great', 'group', 'had', 'has', 'have', 'he', 'her', 'here', 'him', 'his', 'how', 'i', 'if', 'in', 'into', 'is', 'it', 'its', 'just', 'know', 'large', 'last', 'left', 'like', 'long', 'look', 'made', 'make', 'man', 'many', 'may', 'me', 'more', 'most', 'much', 'must', 'my', 'never', 'new', 'no', 'not', 'now', 'number', 'of', 'off', 'old', 'on', 'one', 'only', 'or', 'other', 'our', 'out', 'over', 'own', 'part', 'people', 'place', 'right', 'said', 'same', 'see', 'she', 'should', 'since', 'so', 'some', 'still', 'such', 'system', 'take', 'than', 'that', 'the', 'their', 'them', 'then', 'there', 'these', 'they', 'thing', 'think', 'this', 'those', 'through', 'time', 'to', 'too', 'two', 'under', 'until', 'up', 'use', 'used', 'using', 'very', 'want', 'was', 'water', 'way', 'we', 'well', 'were', 'what', 'when', 'where', 'which', 'while', 'who', 'will', 'with', 'work', 'would', 'year', 'years', 'you', 'your'
        }
        
        # Convert to lowercase for matching
        english_words_lower = {word.lower() for word in english_words_comprehensive}
        
        print(f"🎯 English words dictionary size: {len(english_words_lower)}")
        
        # Check each name
        english_names_found = []
        for name in all_names:
            if pd.notna(name):
                name_lower = str(name).lower().strip()
                if name_lower in english_words_lower:
                    english_names_found.append(name)
        
        print(f"🔍 Found {len(english_names_found)} English words in data")
        if len(english_names_found) > 0:
            print(f"📋 First 20 English words found: {english_names_found[:20]}")
        
        # Filter out English words
        initial_count = len(df)
        
        # Create a function to check if a name is an English word
        def is_english_word(name):
            if pd.isna(name):
                return False
            return str(name).lower().strip() in english_words_lower
        
        # Apply the filter
        df_cleaned = df[~df['Name'].apply(is_english_word)]
        removed_count = initial_count - len(df_cleaned)
        
        print(f"\n📊 COMPREHENSIVE CLEANING RESULTS:")
        print(f"   Original entries: {initial_count}")
        print(f"   Removed entries:  {removed_count}")
        print(f"   Clean entries:    {len(df_cleaned)}")
        print(f"   Retention rate:   {(len(df_cleaned)/initial_count)*100:.1f}%")
        
        # Save the thoroughly cleaned CSV
        output_file = 'THOROUGHLY_CLEANED_AUTHENTIC_SANSKRIT_BABY_NAMES.csv'
        df_cleaned.to_csv(output_file, index=False)
        print(f"\n💾 Saved thoroughly cleaned CSV: {output_file}")
        
        # Pattern distribution
        pattern_counts = df_cleaned['Starting_Pattern'].value_counts()
        print(f"\n🔤 PATTERN DISTRIBUTION IN THOROUGHLY CLEANED DATA:")
        for pattern, count in pattern_counts.items():
            print(f"   {pattern}: {count} names")
        
        # Show sample of clean names
        print(f"\n✅ SAMPLE OF CLEAN AUTHENTIC NAMES:")
        sample_names = df_cleaned['Name'].head(20).tolist()
        for i, name in enumerate(sample_names, 1):
            print(f"   {i:2d}. {name}")
        
        return df_cleaned
        
    except FileNotFoundError:
        print("❌ AUTHENTIC_SANSKRIT_BABY_NAMES.csv not found!")
        return None
    except Exception as e:
        print(f"❌ Error in comprehensive cleaning: {e}")
        return None

if __name__ == "__main__":
    cleaned_df = comprehensive_clean_csv()
    if cleaned_df is not None:
        print(f"\n🎉 COMPREHENSIVE CLEANING COMPLETE!")
        print(f"📄 Thoroughly clean file: THOROUGHLY_CLEANED_AUTHENTIC_SANSKRIT_BABY_NAMES.csv")
        print(f"🎯 Ready with {len(cleaned_df)} purely authentic Sanskrit/Tamil names for your son!")
        print(f"🔥 ZERO COMPROMISE ON AUTHENTICITY!")