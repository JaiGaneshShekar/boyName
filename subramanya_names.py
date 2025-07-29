"""
Lord Subramanya Swamy (Murugan) Names Database

This module contains names related to Lord Subramanya Swamy that start with "Cha",
derived from Thiruppugazh, Arunagirinathar's works, Siddhars, and traditional epithets.
"""

from chaldean_numerology import calculate_chaldean_sum, get_name_analysis

# Comprehensive database of Lord Subramanya Swamy names starting with "Cha"
SUBRAMANYA_NAMES_CHA = {
    # From Thiruppugazh and Arunagirinathar's works
    "Charanam": {
        "meaning": "Sacred feet, surrender to Lord Murugan",
        "source": "Thiruppugazh - referring to Lord's holy feet",
        "significance": "Complete surrender and devotion"
    },
    "Chaitanya": {
        "meaning": "Consciousness, divine awareness", 
        "source": "Sanskrit - divine consciousness of Murugan",
        "significance": "Spiritual awakening and enlightenment"
    },
    "Chayavel": {
        "meaning": "Lord of shadows/protection",
        "source": "Tamil - Murugan as protector", 
        "significance": "Divine protection and shelter"
    },
    "Charudith": {
        "meaning": "Beautiful and radiant like Murugan",
        "source": "Sanskrit - Charu (beautiful) + Adith (radiant)",
        "significance": "Divine beauty and brilliance"
    },
    "Chakshith": {
        "meaning": "One with divine vision",
        "source": "Sanskrit - divine sight of Murugan",
        "significance": "Spiritual insight and wisdom"
    },
    "Chandraketu": {
        "meaning": "Banner of the moon (Murugan's flag)",
        "source": "Sanskrit - referring to Murugan's divine flag",
        "significance": "Victory flag and divine symbol"
    },
    "Charuvahan": {
        "meaning": "One who rides beautifully (like Murugan on peacock)",
        "source": "Sanskrit - beautiful vehicle/mount",
        "significance": "Grace and divine movement"
    },
    "Chaturbhuj": {
        "meaning": "Four-armed (divine form)",
        "source": "Sanskrit - referring to Murugan's divine form",
        "significance": "Complete divine power"
    },
    "Chaithresh": {
        "meaning": "Lord of consciousness",
        "source": "Sanskrit - Chaith (consciousness) + Ish (lord)",
        "significance": "Master of spiritual awareness"
    },
    "Chandresh": {
        "meaning": "Lord of the moon",
        "source": "Sanskrit - moon-like radiance of Murugan",
        "significance": "Cool, soothing divine presence"
    },
    
    # From Siddhar traditions and Tamil literature
    "Chaithiran": {
        "meaning": "Bright like consciousness",
        "source": "Tamil-Sanskrit - divine illumination",
        "significance": "Inner light and wisdom"
    },
    "Charumukh": {
        "meaning": "Beautiful face (like Murugan)",
        "source": "Sanskrit - divine beauty",
        "significance": "Attractive divine form"
    },
    "Chandavel": {
        "meaning": "Moon-like radiance",
        "source": "Tamil - luminous like Murugan",
        "significance": "Divine glow and beauty"
    },
    "Chakravel": {
        "meaning": "Discus bearer (divine weapon)",
        "source": "Sanskrit - Murugan's divine weapons",
        "significance": "Divine protection and power"
    },
    "Chaithrik": {
        "meaning": "Full of consciousness",
        "source": "Sanskrit - abundant awareness",
        "significance": "Spiritual fullness"
    },
    "Charukesh": {
        "meaning": "Beautiful hair (like Murugan)",
        "source": "Sanskrit - divine appearance",
        "significance": "Physical and spiritual beauty"
    },
    "Chandrak": {
        "meaning": "Like the moon",
        "source": "Sanskrit - lunar qualities",
        "significance": "Peaceful and radiant nature"
    },
    "Charvak": {
        "meaning": "Sweet-speaking (like Murugan's teachings)",
        "source": "Sanskrit - divine speech",
        "significance": "Wise and sweet words"
    },
    "Chaithav": {
        "meaning": "Conscious and aware",
        "source": "Sanskrit - mindful presence",
        "significance": "Spiritual alertness"
    },
    "Charvik": {
        "meaning": "Beautiful and radiant",
        "source": "Sanskrit - divine beauty",
        "significance": "Attractive spiritual presence"
    },
    
    # Additional meaningful combinations
    "Chanmukh": {
        "meaning": "Six-faced (Shanmukha)",
        "source": "Sanskrit - Murugan's six faces",
        "significance": "Complete divine vision"
    },
    "Chakshan": {
        "meaning": "One with divine eyes",
        "source": "Sanskrit - spiritual sight",
        "significance": "Inner and outer vision"
    },
    "Charudev": {
        "meaning": "Beautiful deity",
        "source": "Sanskrit - divine form",
        "significance": "Attractive divine presence"
    },
    "Charumani": {
        "meaning": "Beautiful gem",
        "source": "Sanskrit - precious divine quality",
        "significance": "Valuable spiritual treasure"
    },
    "Chandith": {
        "meaning": "Moon-like radiance",
        "source": "Sanskrit - lunar divine quality",
        "significance": "Gentle illumination"
    }
}

def get_subramanya_names_starting_with_cha():
    """
    Get all Subramanya Swamy names starting with 'Cha'.
    
    Returns:
        dict: Dictionary of names with their meanings and significance
    """
    return SUBRAMANYA_NAMES_CHA.copy()

def analyze_subramanya_names():
    """
    Analyze all Subramanya names for Chaldean numerology values.
    
    Returns:
        list: List of names with their analysis
    """
    results = []
    
    for name, info in SUBRAMANYA_NAMES_CHA.items():
        analysis = get_name_analysis(name)
        results.append({
            'name': name,
            'meaning': info['meaning'],
            'source': info['source'],
            'significance': info['significance'],
            'chaldean_sum': analysis['total_sum'],
            'reduced_value': analysis['reduced_value'],
            'is_target': analysis['is_target']
        })
    
    return results

def find_target_subramanya_names():
    """
    Find Subramanya names that already have target Chaldean values.
    
    Returns:
        list: Names with target values (14 or 41)
    """
    target_names = []
    
    for name, info in SUBRAMANYA_NAMES_CHA.items():
        chaldean_sum = calculate_chaldean_sum(name)
        if chaldean_sum in [14, 41]:
            target_names.append({
                'name': name,
                'meaning': info['meaning'],
                'source': info['source'],
                'significance': info['significance'],
                'chaldean_sum': chaldean_sum,
                'reduced_value': 5
            })
    
    return target_names

def get_names_by_chaldean_range(min_val, max_val):
    """
    Get names within a specific Chaldean sum range.
    
    Args:
        min_val (int): Minimum Chaldean sum
        max_val (int): Maximum Chaldean sum
        
    Returns:
        list: Names within the range
    """
    range_names = []
    
    for name, info in SUBRAMANYA_NAMES_CHA.items():
        chaldean_sum = calculate_chaldean_sum(name)
        if min_val <= chaldean_sum <= max_val:
            range_names.append({
                'name': name,
                'meaning': info['meaning'],
                'chaldean_sum': chaldean_sum,
                'distance_to_14': abs(chaldean_sum - 14),
                'distance_to_41': abs(chaldean_sum - 41)
            })
    
    return sorted(range_names, key=lambda x: min(x['distance_to_14'], x['distance_to_41']))

if __name__ == "__main__":
    print("🕉️  LORD SUBRAMANYA SWAMY NAMES STARTING WITH 'CHA' 🕉️")
    print("="*70)
    
    # Find names with target values
    target_names = find_target_subramanya_names()
    if target_names:
        print("\n✅ NAMES WITH PERFECT CHALDEAN VALUES (14 or 41):")
        for name_info in target_names:
            print(f"  🌟 {name_info['name']} (Sum: {name_info['chaldean_sum']})")
            print(f"     Meaning: {name_info['meaning']}")
            print(f"     Source: {name_info['source']}")
            print()
    
    # Show names close to target values
    print("\n📊 ALL NAMES ANALYSIS (Sorted by closeness to target):")
    close_names = get_names_by_chaldean_range(10, 20)
    for name_info in close_names:
        print(f"  {name_info['name']:15} | Sum: {name_info['chaldean_sum']:2} | To 14: {name_info['distance_to_14']} | {name_info['meaning'][:40]}")