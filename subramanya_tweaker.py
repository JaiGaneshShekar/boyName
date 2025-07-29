"""
Enhanced Name Tweaker for Lord Subramanya Swamy Names

This module provides specialized tweaking functions that enforce the "Cha" prefix
constraint while finding Chaldean numerology target values for Murugan-related names.
"""

from chaldean_numerology import calculate_chaldean_sum, get_chaldean_value, is_target_value
from name_tweaker import get_letter_substitutions
from subramanya_names import get_subramanya_names_starting_with_cha
from comprehensive_subramanya_database import get_comprehensive_subramanya_names
import itertools

def enforce_cha_prefix(name):
    """
    Ensure a name starts with exactly 'Cha'.
    
    Args:
        name (str): Input name
        
    Returns:
        str: Name with enforced 'Cha' prefix
    """
    name = name.upper()
    if len(name) >= 3 and name[:3] == 'CHA':
        return name
    elif len(name) >= 2 and name[:2] == 'CH':
        return 'CHA' + name[2:]
    elif len(name) >= 1 and name[0] == 'C':
        return 'CHA' + name[1:]
    else:
        return 'CHA' + name

def generate_cha_variations(base_name, max_changes=3):
    """
    Generate variations of a name that must start with 'Cha'.
    
    Args:
        base_name (str): Base name (will be enforced to start with 'Cha')
        max_changes (int): Maximum number of changes after the 'Cha' prefix
        
    Returns:
        list: List of valid variations all starting with 'Cha'
    """
    # Enforce Cha prefix
    name = enforce_cha_prefix(base_name)
    variations = set()
    variations.add(name)
    
    # Only modify letters after position 2 (keep C-H-A intact)
    if len(name) <= 3:
        return [name]
    
    suffix = name[3:]  # Everything after 'CHA'
    
    # Generate single substitutions in the suffix
    for i, letter in enumerate(suffix):
        if letter.isalpha():
            substitutions = get_letter_substitutions(letter)
            for substitute in substitutions:
                if substitute != letter and len(substitute) <= 2:
                    new_suffix = suffix[:i] + substitute + suffix[i+1:]
                    new_name = 'CHA' + new_suffix
                    variations.add(new_name)
    
    # Generate double substitutions if max_changes >= 2
    if max_changes >= 2 and len(suffix) >= 2:
        suffix_variations = list(set([name[3:] for name in variations]))
        for base_suffix in suffix_variations:
            if base_suffix == suffix:  # Skip original
                continue
            for i, letter in enumerate(base_suffix):
                if letter.isalpha():
                    substitutions = get_letter_substitutions(letter)
                    for substitute in substitutions:
                        if substitute != letter and len(substitute) <= 2:
                            new_suffix = base_suffix[:i] + substitute + base_suffix[i+1:]
                            new_name = 'CHA' + new_suffix
                            variations.add(new_name)
    
    # Generate triple substitutions if max_changes >= 3
    if max_changes >= 3 and len(suffix) >= 3:
        # Limit to avoid too many combinations
        current_variations = list(variations)[:20]  # Limit processing
        for base_name_var in current_variations:
            if base_name_var == name:  # Skip original
                continue
            base_suffix = base_name_var[3:]
            for i, letter in enumerate(base_suffix):
                if letter.isalpha():
                    substitutions = get_letter_substitutions(letter)
                    for substitute in substitutions[:3]:  # Limit substitutions
                        if substitute != letter and len(substitute) <= 2:
                            new_suffix = base_suffix[:i] + substitute + base_suffix[i+1:]
                            new_name = 'CHA' + new_suffix
                            variations.add(new_name)
                            if len(variations) > 100:  # Prevent explosion
                                break
                    if len(variations) > 100:
                        break
                if len(variations) > 100:
                    break
    
    return list(variations)

def find_cha_target_tweaks(base_name, target_values=[14, 41], max_changes=3):
    """
    Find name tweaks for Cha-starting names that achieve target Chaldean values.
    
    Args:
        base_name (str): Base name (will be enforced to start with 'Cha')
        target_values (list): Target Chaldean sums
        max_changes (int): Maximum number of changes after 'Cha' prefix
        
    Returns:
        list: List of successful tweaks with analysis
    """
    original_name = enforce_cha_prefix(base_name)
    variations = generate_cha_variations(original_name, max_changes)
    successful_tweaks = []
    
    for variation in variations:
        chaldean_sum = calculate_chaldean_sum(variation)
        if chaldean_sum in target_values:
            # Calculate changes (only in suffix after 'CHA')
            changes = []
            original_suffix = original_name[3:]
            variation_suffix = variation[3:]
            
            if original_suffix != variation_suffix:
                if len(original_suffix) == len(variation_suffix):
                    # Same length - count character differences
                    for i, (orig_char, var_char) in enumerate(zip(original_suffix, variation_suffix)):
                        if orig_char != var_char:
                            changes.append({
                                'position': i + 3,  # Adjust for 'CHA' prefix
                                'from': orig_char,
                                'to': var_char
                            })
                else:
                    # Different lengths - count as structural change
                    changes.append({
                        'position': 3,
                        'from': original_suffix,
                        'to': variation_suffix
                    })
            
            successful_tweaks.append({
                'original': base_name,
                'original_enforced': original_name, 
                'tweaked': variation,
                'chaldean_sum': chaldean_sum,
                'changes': changes,
                'num_changes': len(changes),
                'prefix_preserved': True
            })
    
    # Sort by fewest changes first
    successful_tweaks.sort(key=lambda x: x['num_changes'])
    return successful_tweaks

def find_closest_subramanya_names(target_sum=14):
    """
    Find Subramanya names closest to the target Chaldean sum.
    
    Args:
        target_sum (int): Target Chaldean sum (default 14)
        
    Returns:
        list: Names sorted by distance to target
    """
    # Use comprehensive database
    names_db = get_comprehensive_subramanya_names()
    results = []
    
    for name, info in names_db.items():
        chaldean_sum = calculate_chaldean_sum(name)
        distance = abs(chaldean_sum - target_sum)
        
        results.append({
            'name': name,
            'meaning': info['meaning'],
            'source': info['source'],
            'significance': info['significance'],
            'chaldean_sum': chaldean_sum,
            'distance_to_target': distance,
            'is_target': chaldean_sum in [14, 41]
        })
    
    return sorted(results, key=lambda x: x['distance_to_target'])

def optimize_subramanya_name_for_target(base_name, max_changes=3):
    """
    Comprehensive optimization for Subramanya names.
    
    Args:
        base_name (str): Base name to optimize
        max_changes (int): Maximum changes allowed
        
    Returns:
        dict: Complete optimization results
    """
    # Ensure Cha prefix
    original_name = enforce_cha_prefix(base_name)
    original_sum = calculate_chaldean_sum(original_name)
    
    # Check if already perfect
    if original_sum in [14, 41]:
        return {
            'original': base_name,
            'optimized_name': original_name,
            'already_perfect': True,
            'chaldean_sum': original_sum,
            'reduced_value': 5,
            'tweaks_needed': []
        }
    
    # Find tweaks
    tweaks = find_cha_target_tweaks(original_name, max_changes=max_changes)
    
    # Get database info if available from comprehensive database
    names_db = get_comprehensive_subramanya_names()
    db_info = names_db.get(original_name, {
        'meaning': 'Custom name related to Lord Subramanya',
        'source': 'User provided',
        'significance': 'Devotion to Lord Murugan'
    })
    
    return {
        'original': base_name,
        'original_enforced': original_name,
        'original_sum': original_sum,
        'database_info': db_info,
        'already_perfect': False,
        'successful_tweaks': tweaks,
        'best_tweak': tweaks[0] if tweaks else None,
        'total_options': len(tweaks)
    }

def format_subramanya_tweak_result(result):
    """
    Format optimization results for display.
    
    Args:
        result (dict): Result from optimize_subramanya_name_for_target
        
    Returns:
        str: Formatted display string
    """
    if result['already_perfect']:
        return f"""
🕉️  PERFECT SUBRAMANYA NAME 🕉️
Original: {result['original']}
Optimized: {result['optimized_name']}
Chaldean Sum: {result['chaldean_sum']} ✅ (reduces to 5)
Status: Already perfect for Lord Murugan! 🌟
"""
    
    output = f"""
🕉️  SUBRAMANYA NAME OPTIMIZATION 🕉️
Original: {result['original']}
Enforced: {result['original_enforced']} (with Cha prefix)
Original Sum: {result['original_sum']}
Database Info: {result['database_info']['meaning']}
Source: {result['database_info']['source']}

"""
    
    if result['successful_tweaks']:
        output += f"✅ Found {result['total_options']} optimization(s):\n\n"
        best = result['best_tweak']
        output += f"🌟 BEST OPTION:\n"
        output += f"   {best['tweaked']}\n"
        output += f"   Chaldean Sum: {best['chaldean_sum']} (reduces to 5)\n"
        output += f"   Changes: {best['num_changes']}\n"
        output += f"   Prefix 'Cha' preserved: ✅\n"
    else:
        output += "❌ No valid optimizations found within change limit.\n"
    
    return output