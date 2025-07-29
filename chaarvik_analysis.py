#!/usr/bin/env python3
"""
Comprehensive Analysis for Chaarvik - Lord Murugan Name Optimization

Special analysis for the name "Chaarvik" with Lord Subramanya Swamy significance.
"""

from chaldean_numerology import get_name_analysis, calculate_chaldean_sum
from subramanya_tweaker import optimize_subramanya_name_for_target

def analyze_chaarvik_comprehensive():
    """Comprehensive analysis of Chaarvik and its optimizations."""
    
    print("🕉️  COMPREHENSIVE CHAARVIK ANALYSIS FOR LORD MURUGAN 🕉️")
    print("="*70)
    
    original_name = "Chaarvik"
    analysis = get_name_analysis(original_name)
    
    print(f"👶 Baby Name: {original_name}")
    print(f"🔢 Chaldean Sum: {analysis['total_sum']} (reduces to {analysis['reduced_value']})")
    print(f"🎯 Target Status: {'✅ Perfect!' if analysis['is_target'] else '❌ Needs optimization'}")
    
    print(f"\n📝 Letter Breakdown:")
    for item in analysis['letter_breakdown']:
        print(f"   {item['letter']}: {item['value']}")
    
    print(f"\n🕉️  LORD MURUGAN CONNECTION:")
    print(f"   • Name starts with 'Cha' - Perfect for Revathi nakshatra 3rd pada")
    print(f"   • 'Char' relates to divine movement/grace of Lord Murugan")
    print(f"   • 'Vik' suggests victory/conquest - Lord's triumph over evil")
    print(f"   • Overall meaning: 'One who moves with divine grace and victory'")
    
    print(f"\n🎯 OPTIMIZATION ANALYSIS:")
    print(f"   Current sum: {analysis['total_sum']}")
    print(f"   Need to reduce by: {analysis['total_sum'] - 14} to reach 14")
    print(f"   Need to increase by: {41 - analysis['total_sum']} to reach 41")
    
    # Manual optimizations found
    optimizations = [
        {
            'name': 'CHAARAI',
            'changes': 'V(6)→A(1), K(2)→I(1) = saves 6 points',
            'meaning': 'Divine grace and radiance - referring to Lord Murugan\'s luminous form'
        },
        {
            'name': 'CHAARII', 
            'changes': 'V(6)→I(1), K(2)→I(1) = saves 6 points',
            'meaning': 'Filled with divine light - multiple sources of Murugan\'s illumination'
        }
    ]
    
    print(f"\n✨ BLESSED OPTIMIZATIONS FOR LORD MURUGAN:")
    print(f"="*50)
    
    for i, opt in enumerate(optimizations, 1):
        opt_analysis = get_name_analysis(opt['name'])
        print(f"\n🌟 Option {i}: {opt['name']}")
        print(f"   Chaldean Sum: {opt_analysis['total_sum']} ✅ (reduces to {opt_analysis['reduced_value']})")
        print(f"   Changes: {opt['changes']}")
        print(f"   Spiritual Meaning: {opt['meaning']}")
        print(f"   Pronunciation: Similar to original, maintains 'Chaar' sound")
    
    print(f"\n🙏 SPIRITUAL SIGNIFICANCE:")
    print(f"="*30)
    print(f"   • Number 5 (reduced value) represents:")
    print(f"     - Adventure and curiosity (perfect for a growing child)")
    print(f"     - Dynamic energy (Lord Murugan's active divine nature)")
    print(f"     - Freedom and exploration (spiritual and worldly journey)")
    print(f"     - Communication skills (blessed speech like Murugan)")
    
    print(f"\n📿 RECOMMENDATION:")
    print(f"="*20)
    print(f"   🌟 CHAARAI - Best choice because:")
    print(f"   • Maintains the beautiful 'Chaar' core sound")
    print(f"   • Ending 'ai' is auspicious in Tamil tradition")
    print(f"   • Minimal changes preserve original name's essence")
    print(f"   • Perfect Chaldean numerology (14 → 5)")
    print(f"   • Strong connection to Lord Murugan's divine grace")
    
    print(f"\n🕉️ Om Saravana Bhava! May Lord Murugan bless this child! 🕉️")

def quick_chaarvik_optimization():
    """Quick optimization display for Chaarvik."""
    print("⚡ QUICK CHAARVIK OPTIMIZATION ⚡")
    print("="*40)
    print("Original: Chaarvik (Sum: 21)")
    print("✅ Optimized: CHAARAI (Sum: 14 → Lucky 5)")
    print("Changes: v→a, k→i (2 minimal changes)")
    print("🕉️ Perfect for Lord Murugan devotion!")

if __name__ == "__main__":
    analyze_chaarvik_comprehensive()
    print("\n" + "="*70)
    quick_chaarvik_optimization()