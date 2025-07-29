#!/usr/bin/env python3
"""
Test Examples for Chaldean Name Optimizer

This script demonstrates the system with various example names.
"""

from chaldean_numerology import get_name_analysis, calculate_chaldean_sum
from name_tweaker import find_target_tweaks, format_tweak_result

def test_name(name, max_changes=2):
    """Test a single name and show results."""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"{'='*60}")
    
    # Get analysis
    analysis = get_name_analysis(name)
    print(f"Chaldean Sum: {analysis['total_sum']} (reduces to {analysis['reduced_value']})")
    print(f"Target Achieved: {'✅ YES' if analysis['is_target'] else '❌ NO'}")
    
    if analysis['is_target']:
        print("🎉 This name already has perfect numerology!")
        return
    
    # Find tweaks
    print(f"\n🔍 Searching for tweaks (max {max_changes} changes)...")
    tweaks = find_target_tweaks(name, max_changes=max_changes)
    
    if tweaks:
        print(f"🎯 Found {len(tweaks)} valid tweak(s):")
        for i, tweak in enumerate(tweaks[:3], 1):  # Show top 3
            print(f"\nOption {i}:")
            print(f"  {tweak['original']} → {tweak['tweaked']}")
            print(f"  Chaldean Sum: {tweak['chaldean_sum']}")
            print(f"  Changes: {tweak['num_changes']}")
    else:
        print("❌ No valid tweaks found.")

def main():
    """Run example tests."""
    print("🌟 Chaldean Name Optimizer - Test Examples 🌟")
    print("Testing various names to demonstrate the system...")
    
    # Test names with different characteristics
    test_names = [
        "John",     # Common name, needs tweaking
        "Mike",     # Short name, should find tweaks
        "Fan",      # Already has target value 14
        "David",    # Longer name
        "Alex",     # Medium name
    ]
    
    for name in test_names:
        test_name(name)
    
    print(f"\n{'='*60}")
    print("Test complete! Try running: python3 main.py [name]")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()