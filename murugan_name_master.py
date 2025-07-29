#!/usr/bin/env python3
"""
Lord Murugan Name Master Tool

Complete solution for finding, analyzing, and optimizing Lord Subramanya Swamy names
starting with "Cha" based on comprehensive research and Chaldean numerology.
"""

import sys
import argparse
from comprehensive_subramanya_database import get_comprehensive_subramanya_names
from comprehensive_murugan_analysis import comprehensive_report, quick_name_lookup
from subramanya_tweaker import optimize_subramanya_name_for_target
from chaldean_numerology import calculate_chaldean_sum
from twitter_poster import TwitterPoster

def chaarvik_specific_analysis():
    """Specific analysis for the name Chaarvik."""
    print("🕉️  CHAARVIK - COMPLETE ANALYSIS FOR LORD MURUGAN 🕉️")
    print("="*70)
    
    original = "Chaarvik"
    chaldean_sum = calculate_chaldean_sum(original)
    
    print(f"👶 Baby Name: {original}")
    print(f"🔢 Current Chaldean Sum: {chaldean_sum} (reduces to {chaldean_sum % 9 if chaldean_sum % 9 != 0 else 9})")
    print(f"🎯 Target: 14 or 41 (both reduce to lucky number 5)")
    
    print(f"\n🕉️  SPIRITUAL CONNECTION TO LORD MURUGAN:")
    print(f"✓ Starts with 'Cha' - Perfect for Revathi nakshatra 3rd pada")
    print(f"✓ 'Chaar' relates to divine movement and grace of Lord Murugan")
    print(f"✓ 'Vik' suggests victory and conquest - Lord's triumph over evil")
    print(f"✓ Complete meaning: 'One who moves with divine grace and achieves victory'")
    
    print(f"\n🎯 NUMEROLOGICAL OPTIMIZATION:")
    print(f"Current sum: {chaldean_sum}")
    print(f"Need to reduce by: {chaldean_sum - 14} to reach 14")
    
    # Show the successful optimizations
    optimizations = [
        {
            'name': 'CHAARAI',
            'sum': 14,
            'changes': 'v→a, k→i (2 changes)',
            'meaning': 'Divine grace and radiance - referring to Lord Murugan\'s luminous aura',
            'pronunciation': 'Chaa-rai (similar to original)'
        },
        {
            'name': 'CHAARII', 
            'sum': 14,
            'changes': 'v→i, k→i (2 changes)',
            'meaning': 'Filled with divine light - multiple sources of illumination',
            'pronunciation': 'Chaa-rii (similar to original)'
        }
    ]
    
    print(f"\n✨ BLESSED OPTIMIZATIONS:")
    print(f"="*40)
    
    for i, opt in enumerate(optimizations, 1):
        print(f"\n🌟 OPTION {i}: {opt['name']}")
        print(f"   Chaldean Sum: {opt['sum']} ✅ (reduces to 5)")
        print(f"   Changes: {opt['changes']}")
        print(f"   Spiritual Meaning: {opt['meaning']}")
        print(f"   Pronunciation: {opt['pronunciation']}")
        print(f"   Maintains 'Cha' prefix: ✅")
    
    print(f"\n🏆 RECOMMENDATION: CHAARAI")
    print(f"="*30)
    print(f"✓ Most phonetically similar to original")
    print(f"✓ 'Ai' ending is highly auspicious in Tamil tradition")
    print(f"✓ Perfect Chaldean numerology (14 → 5)")
    print(f"✓ Strong spiritual connection to Lord Murugan's grace")
    print(f"✓ Easy pronunciation for family and friends")
    
    print(f"\n🙏 SPIRITUAL SIGNIFICANCE OF NUMBER 5:")
    print(f"✓ Adventure and curiosity (perfect for a growing child)")
    print(f"✓ Dynamic energy (Lord Murugan's active divine nature)")
    print(f"✓ Freedom and exploration (both spiritual and worldly)")
    print(f"✓ Communication skills (blessed speech like Murugan)")
    print(f"✓ Adaptability and versatility in life")

def browse_database_by_category():
    """Browse the comprehensive database by different categories."""
    print("📚 BROWSE COMPREHENSIVE MURUGAN NAMES DATABASE")
    print("="*55)
    
    names_db = get_comprehensive_subramanya_names()
    
    # Organize by source categories
    categories = {}
    for name, info in names_db.items():
        source_key = info['source'].split(' - ')[0] if ' - ' in info['source'] else info['source']
        if source_key not in categories:
            categories[source_key] = []
        categories[source_key].append((name, info))
    
    print("Available categories:")
    for i, category in enumerate(sorted(categories.keys()), 1):
        count = len(categories[category])
        print(f"{i:2}. {category} ({count} names)")
    
    try:
        choice = input("\nSelect category number (or press Enter for all): ").strip()
        if choice:
            choice_idx = int(choice) - 1
            selected_category = sorted(categories.keys())[choice_idx]
            
            print(f"\n🏷️  {selected_category.upper()}")
            print("="*50)
            
            for name, info in sorted(categories[selected_category]):
                chaldean_sum = calculate_chaldean_sum(name)
                status = "✅" if chaldean_sum in [14, 41] else f"({chaldean_sum})"
                print(f"\n📿 {name} {status}")
                print(f"   Tamil: {info['tamil']}")
                print(f"   Meaning: {info['meaning']}")
                print(f"   Significance: {info['significance']}")
        else:
            # Show all names briefly
            print(f"\n📖 ALL NAMES IN DATABASE:")
            print("="*30)
            for name, info in sorted(names_db.items()):
                chaldean_sum = calculate_chaldean_sum(name)
                status = "✅" if chaldean_sum in [14, 41] else f"({chaldean_sum})"
                print(f"   {name:20} {status} - {info['meaning'][:40]}")
                
    except (ValueError, IndexError):
        print("Invalid selection.")

def interactive_master_tool():
    """Interactive master tool for all Murugan name operations."""
    print("🕉️  LORD MURUGAN NAME MASTER TOOL 🕉️")
    print("Complete solution for sacred name selection")
    print("Based on extensive research across Tamil, Sanskrit, and global traditions")
    print()
    
    # Check Twitter integration
    twitter_enabled = False
    try:
        twitter_poster = TwitterPoster()
        test_result = twitter_poster.test_connection()
        if test_result['success']:
            twitter_enabled = True
            print("✅ Twitter integration enabled!")
        else:
            print("⚠️  Twitter integration disabled")
    except:
        print("⚠️  Twitter integration disabled")
    
    while True:
        try:
            print("\n" + "="*60)
            print("MASTER MENU:")
            print("1. 🎯 Analyze 'Chaarvik' specifically (your request)")
            print("2. 📚 Browse comprehensive names database") 
            print("3. 🔍 Search by name/meaning/source")
            print("4. 🛠️  Optimize any custom name")
            print("5. 📊 View complete research report")
            print("6. 🌟 Find names closest to target values")
            print("Type 'quit' to exit")
            print("="*60)
            
            choice = input("\nSelect option (1-6): ").strip()
            
            if choice.lower() in ['quit', 'exit', 'q']:
                print("🙏 Om Saravana Bhava! May Lord Murugan bless your child!")
                break
            
            elif choice == '1':
                chaarvik_specific_analysis()
                
                if twitter_enabled:
                    share = input("\nShare Chaarvik analysis on Twitter? (y/n): ").strip().lower()
                    if share in ['y', 'yes']:
                        tweet_text = "🕉️ Perfect Murugan Name Found! 🕉️\\n\\n"
                        tweet_text += "Chaarvik → CHAARAI\\n"
                        tweet_text += "✓ Chaldean: 14 (Lucky 5)\\n"
                        tweet_text += "✓ Starts with 'Cha' (Revathi 3rd pada)\\n"
                        tweet_text += "✓ Divine grace of Lord Subramanya\\n\\n"
                        tweet_text += "#Murugan #BabyNames #Numerology #Chaarvik"
                        
                        result = twitter_poster.create_tweet(tweet_text)
                        if 'error' in result:
                            print(f"❌ Failed to post: {result['message']}")
                        else:
                            print("✅ Shared successfully!")
            
            elif choice == '2':
                browse_database_by_category()
            
            elif choice == '3':
                search_term = input("Enter search term: ").strip()
                if search_term:
                    names_db = get_comprehensive_subramanya_names()
                    results = []
                    
                    for name, info in names_db.items():
                        if (search_term.lower() in name.lower() or 
                            search_term.lower() in info['meaning'].lower() or
                            search_term.lower() in info['source'].lower()):
                            results.append((name, info))
                    
                    if results:
                        print(f"\n🔍 Found {len(results)} results:")
                        for name, info in results:
                            chaldean_sum = calculate_chaldean_sum(name)
                            print(f"   📿 {name} ({chaldean_sum}) - {info['meaning']}")
                            print(f"      Source: {info['source']}")
                    else:
                        print("❌ No results found.")
            
            elif choice == '4':
                custom_name = input("Enter name to optimize: ").strip()
                if custom_name:
                    max_changes = 3
                    try:
                        max_input = input(f"Max changes (default {max_changes}): ").strip()
                        if max_input:
                            max_changes = int(max_input)
                    except ValueError:
                        pass
                    
                    result = optimize_subramanya_name_for_target(custom_name, max_changes)
                    
                    print(f"\n🕉️ OPTIMIZATION RESULTS FOR '{custom_name}':")
                    print(f"Original: {result['original']}")
                    print(f"Enforced: {result['original_enforced']}")
                    print(f"Sum: {result['original_sum']}")
                    
                    if result['successful_tweaks']:
                        print(f"\n✅ Found {result['total_options']} optimization(s):")
                        best = result['best_tweak']
                        print(f"🌟 Best: {best['tweaked']} (Sum: {best['chaldean_sum']})")
                        print(f"   Changes: {best['num_changes']}")
                        
                        if twitter_enabled:
                            share = input("Share on Twitter? (y/n): ").strip().lower()
                            if share in ['y', 'yes']:
                                tweet_text = f"🕉️ Murugan Name Optimization 🕉️\\n\\n"
                                tweet_text += f"{result['original']} → {best['tweaked']}\\n"
                                tweet_text += f"Chaldean: {best['chaldean_sum']} (Lucky 5)\\n"
                                tweet_text += f"Changes: {best['num_changes']}\\n\\n#Murugan #NameOptimization"
                                
                                post_result = twitter_poster.create_tweet(tweet_text)
                                if 'error' in post_result:
                                    print(f"❌ Failed to post: {post_result['message']}")
                                else:
                                    print("✅ Shared successfully!")
                    else:
                        print("❌ No optimizations found within change limits.")
            
            elif choice == '5':
                comprehensive_report()
            
            elif choice == '6':
                print("🎯 Names closest to target Chaldean value 14:")
                from subramanya_tweaker import find_closest_subramanya_names
                closest = find_closest_subramanya_names()
                
                for i, name_info in enumerate(closest[:10], 1):
                    status = "✅ PERFECT" if name_info['is_target'] else f"Distance: {name_info['distance_to_target']}"
                    print(f"{i:2}. {name_info['name']:20} ({name_info['chaldean_sum']:2}) - {status}")
                    print(f"    {name_info['meaning']}")
            
            else:
                print("Please enter a valid choice (1-6)")
                
        except KeyboardInterrupt:
            print("\\n🙏 Om Saravana Bhava! May Lord Murugan bless your child!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def main():
    """Main entry point with command line options."""
    parser = argparse.ArgumentParser(description="Lord Murugan Name Master Tool")
    parser.add_argument('--chaarvik', action='store_true', help='Analyze Chaarvik specifically')
    parser.add_argument('--report', action='store_true', help='Generate comprehensive report')
    parser.add_argument('--lookup', type=str, help='Look up specific name')
    parser.add_argument('--optimize', type=str, help='Optimize specific name')
    parser.add_argument('-i', '--interactive', action='store_true', help='Interactive mode')
    
    args = parser.parse_args()
    
    if args.chaarvik:
        chaarvik_specific_analysis()
    elif args.report:
        comprehensive_report()
    elif args.lookup:
        quick_name_lookup(args.lookup)
    elif args.optimize:
        result = optimize_subramanya_name_for_target(args.optimize)
        print(f"Optimization result: {result}")
    else:
        interactive_master_tool()

if __name__ == "__main__":
    main()