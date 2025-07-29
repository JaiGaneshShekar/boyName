"""
Name Tweaker Module

This module provides functions to tweak names by substituting letters
to achieve target Chaldean numerology values while preserving meaning and sound.
"""

from chaldean_numerology import calculate_chaldean_sum, get_chaldean_value, is_target_value
import itertools


# Phonetically similar letter substitutions
# Grouped by similar sounds and pronunciation
VOWEL_SUBSTITUTIONS = {
    'A': ['A', 'AA', 'E'],  # A can become AA (elongated) or E
    'E': ['E', 'EE', 'A', 'I'],  # E can become EE, A, or I
    'I': ['I', 'II', 'E', 'Y'],  # I can become II, E, or Y
    'O': ['O', 'OO', 'U'],  # O can become OO or U
    'U': ['U', 'UU', 'O'],  # U can become UU or O
    'Y': ['Y', 'I']  # Y can become I
}

CONSONANT_SUBSTITUTIONS = {
    'B': ['B', 'P'],  # Similar sounds
    'C': ['C', 'K', 'S'],  # Hard C to K, soft C to S
    'D': ['D', 'T'],  # Similar sounds
    'F': ['F', 'PH', 'V'],  # Similar sounds
    'G': ['G', 'J'],  # Soft G to J
    'H': ['H'],  # Usually keep H as is
    'J': ['J', 'G'],  # J to soft G
    'K': ['K', 'C'],  # K to hard C
    'L': ['L', 'LL'],  # L can be elongated
    'M': ['M', 'MM'],  # M can be elongated
    'N': ['N', 'NN'],  # N can be elongated
    'P': ['P', 'B'],  # Similar sounds
    'Q': ['Q', 'K'],  # Q sound like K
    'R': ['R', 'RR'],  # R can be elongated
    'S': ['S', 'C', 'Z'],  # S to soft C or Z
    'T': ['T', 'D'],  # Similar sounds
    'V': ['V', 'F'],  # Similar sounds
    'W': ['W'],  # Usually keep W as is
    'X': ['X', 'KS'],  # X sound
    'Z': ['Z', 'S']  # Similar sounds
}


def get_letter_substitutions(letter):
    """
    Get possible substitutions for a letter.
    
    Args:
        letter (str): The letter to find substitutions for
        
    Returns:
        list: List of possible substitutions
    """
    letter = letter.upper()
    
    if letter in VOWEL_SUBSTITUTIONS:
        return VOWEL_SUBSTITUTIONS[letter]
    elif letter in CONSONANT_SUBSTITUTIONS:
        return CONSONANT_SUBSTITUTIONS[letter]
    else:
        return [letter]


def generate_name_variations(name, max_changes=2):
    """
    Generate variations of a name by substituting letters.
    
    Args:
        name (str): Original name
        max_changes (int): Maximum number of letters to change
        
    Returns:
        list: List of name variations
    """
    name = name.upper()
    variations = set()
    variations.add(name)  # Include original
    
    # Generate single-letter substitutions
    for i, letter in enumerate(name):
        if letter.isalpha():
            substitutions = get_letter_substitutions(letter)
            for substitute in substitutions:
                if substitute != letter and len(substitute) <= 2:  # Limit elongations
                    new_name = name[:i] + substitute + name[i+1:]
                    variations.add(new_name)
    
    # Generate two-letter substitutions if max_changes >= 2
    if max_changes >= 2:
        base_variations = list(variations)
        for base_name in base_variations:
            if base_name == name:  # Only apply second change to original
                continue
            for i, letter in enumerate(base_name):
                if letter.isalpha():
                    substitutions = get_letter_substitutions(letter)
                    for substitute in substitutions:
                        if substitute != letter and len(substitute) <= 2:
                            new_name = base_name[:i] + substitute + base_name[i+1:]
                            if new_name != base_name:
                                variations.add(new_name)
    
    return list(variations)


def find_target_tweaks(name, target_values=[14, 41], max_changes=2):
    """
    Find name tweaks that achieve target Chaldean values.
    
    Args:
        name (str): Original name
        target_values (list): Target Chaldean sums
        max_changes (int): Maximum number of letter changes
        
    Returns:
        list: List of successful tweaks with their analysis
    """
    variations = generate_name_variations(name, max_changes)
    successful_tweaks = []
    
    for variation in variations:
        chaldean_sum = calculate_chaldean_sum(variation)
        if chaldean_sum in target_values:
            # Calculate what changed
            changes = []
            original_clean = ''.join(c for c in name.upper() if c.isalpha())
            variation_clean = ''.join(c for c in variation if c.isalpha())
            
            # Count simple substitutions
            if original_clean != variation_clean:
                if len(original_clean) == len(variation_clean):
                    # Same length - count character differences
                    for i, (orig_char, var_char) in enumerate(zip(original_clean, variation_clean)):
                        if orig_char != var_char:
                            changes.append({
                                'position': i,
                                'from': orig_char,
                                'to': var_char
                            })
                else:
                    # Different lengths - count as one change for elongations
                    changes.append({
                        'position': 0,
                        'from': original_clean,
                        'to': variation_clean
                    })
            
            successful_tweaks.append({
                'original': name,
                'tweaked': variation,
                'chaldean_sum': chaldean_sum,
                'changes': changes,
                'num_changes': len(changes)
            })
    
    # Sort by fewest changes first
    successful_tweaks.sort(key=lambda x: x['num_changes'])
    return successful_tweaks


def format_tweak_result(tweak):
    """
    Format a tweak result for display.
    
    Args:
        tweak (dict): Tweak result from find_target_tweaks
        
    Returns:
        str: Formatted string
    """
    changes_str = []
    for change in tweak['changes']:
        if change['from'] == '':
            changes_str.append(f"Added '{change['to']}' at position {change['position']}")
        else:
            changes_str.append(f"Changed '{change['from']}' to '{change['to']}' at position {change['position']}")
    
    return f"""
Original: {tweak['original']}
Tweaked:  {tweak['tweaked']}
Chaldean Sum: {tweak['chaldean_sum']}
Changes ({tweak['num_changes']}): {'; '.join(changes_str)}
"""