#!/usr/bin/env python3
"""
Lord Murugan Name Finder

A specialized tool to find and optimize names related to Lord Subramanya Swamy (Murugan)
that start with "Cha" and achieve target Chaldean numerology values.
"""

import sys
import argparse
from typing import List, Dict, Any

from chaldean_numerology import get_name_analysis, calculate_chaldean_sum
from subramanya_names import (
    get_subramanya_names_starting_with_cha, 
    find_target_subramanya_names,
    analyze_subramanya_names,
    get_names_by_chaldean_range
)
from subramanya_tweaker import (
    optimize_subramanya_name_for_target,
    format_subramanya_tweak_result,
    find_closest_subramanya_names
)
from twitter_poster import TwitterPoster

def display_perfect_murugan_names():
    """Display all Murugan names that already have perfect Chaldean values."""
    print("🕉️  PERFECT MURUGAN NAMES (Chaldean 14 or 41) 🕉️")
    print("="*70)
    
    perfect_names = find_target_subramanya_names()
    
    if perfect_names:
        for name_info in perfect_names:
            print(f"\n🌟 {name_info['name']} (Sum: {name_info['chaldean_sum']})")
            print(f"   Meaning: {name_info['meaning']}")
            print(f"   Source: {name_info['source']}")
            print(f"   Significance: {name_info['significance']}")
    else:
        print("No names in database currently have perfect values.")
        print("Use the optimization feature to find tweaked versions!")

def display_all_murugan_names():
    """Display all Murugan names with their Chaldean analysis."""
    print("🕉️  ALL LORD MURUGAN NAMES STARTING WITH 'CHA' 🕉️")
    print("="*80)
    
    names_analysis = analyze_subramanya_names()
    
    # Sort by closeness to target values
    names_analysis.sort(key=lambda x: min(abs(x['chaldean_sum'] - 14), abs(x['chaldean_sum'] - 41)))
    
    for name_info in names_analysis:
        status = "✅ PERFECT" if name_info['is_target'] else f"Distance to 14: {abs(name_info['chaldean_sum'] - 14)}"
        print(f"\n📿 {name_info['name']} (Sum: {name_info['chaldean_sum']}) - {status}")
        print(f"   Meaning: {name_info['meaning']}")
        print(f"   Source: {name_info['source']}")

def find_best_murugan_names_for_optimization():
    """Find the best Murugan names for optimization to target values."""
    print("🔍 BEST MURUGAN NAMES FOR OPTIMIZATION 🔍")
    print("="*60)
    
    closest_names = find_closest_subramanya_names(target_sum=14)
    
    print("\nTop candidates for achieving Chaldean sum of 14:")
    for i, name_info in enumerate(closest_names[:10], 1):
        if name_info['is_target']:
            print(f"{i:2}. 🌟 {name_info['name']} (Sum: {name_info['chaldean_sum']}) - ALREADY PERFECT!")
        else:
            print(f"{i:2}. 📿 {name_info['name']} (Sum: {name_info['chaldean_sum']}) - Need {name_info['distance_to_target']} change")
        print(f"     {name_info['meaning']}")

def optimize_custom_murugan_name(name, max_changes=3):
    """Optimize a custom name for Murugan with Cha prefix."""
    print(f"🕉️  OPTIMIZING '{name}' FOR LORD MURUGAN 🕉️")
    print("="*60)
    
    result = optimize_subramanya_name_for_target(name, max_changes)
    formatted_result = format_subramanya_tweak_result(result)
    print(formatted_result)
    
    return result

def interactive_murugan_name_finder():
    """Interactive mode for finding perfect Murugan names."""
    print("🕉️  WELCOME TO LORD MURUGAN NAME FINDER 🕉️")
    print("Find perfect names for your baby boy related to Lord Subramanya Swamy!")
    print("All names will start with 'Cha' as per Revathi nakshatra 3rd pada.")
    print("Type 'quit' to exit.\n")
    
    # Check Twitter integration
    twitter_poster = None
    twitter_enabled = False
    try:
        twitter_poster = TwitterPoster()
        test_result = twitter_poster.test_connection()
        if test_result['success']:
            twitter_enabled = True
            print("✅ Twitter integration enabled for sharing blessed names!")
        else:
            print("⚠️  Twitter integration disabled")
    except Exception:
        print("⚠️  Twitter integration disabled")
    
    while True:
        try:
            print("\n" + "="*50)
            print("MENU OPTIONS:")
            print("1. View all perfect Murugan names (Chaldean 14/41)")
            print("2. View all Murugan names with analysis")
            print("3. Find best names for optimization")
            print("4. Optimize a custom name")
            print("5. Optimize 'Chaarvik' specifically")
            print("Type 'quit' to exit")
            print("="*50)
            
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice.lower() in ['quit', 'exit', 'q']:
                print("🙏 Om Muruga! May Lord Subramanya bless your child! 🙏")
                break
            
            elif choice == '1':
                display_perfect_murugan_names()
                
                if twitter_enabled:
                    perfect_names = find_target_subramanya_names()
                    if perfect_names:
                        post_choice = input("\nPost a perfect name to Twitter? (y/n): ").strip().lower()
                        if post_choice in ['y', 'yes']:
                            # Post the first perfect name
                            name_to_post = perfect_names[0]
                            tweet_text = f"🕉️ Perfect Murugan Name 🕉️\n\n"
                            tweet_text += f"Name: {name_to_post['name']}\n"
                            tweet_text += f"Meaning: {name_to_post['meaning']}\n"
                            tweet_text += f"Chaldean: {name_to_post['chaldean_sum']} (Lucky 5)\n\n"
                            tweet_text += "#Murugan #Subramanya #BabyNames #Numerology"
                            
                            result = twitter_poster.create_tweet(tweet_text)
                            if 'error' in result:
                                print(f"❌ Failed to post: {result['message']}")
                            else:
                                print("✅ Posted to Twitter successfully!")
            
            elif choice == '2':
                display_all_murugan_names()
            
            elif choice == '3':
                find_best_murugan_names_for_optimization()
            
            elif choice == '4':
                custom_name = input("Enter name to optimize (will enforce 'Cha' prefix): ").strip()
                if custom_name:
                    max_changes = 3
                    try:
                        max_input = input(f"Max changes allowed (default {max_changes}): ").strip()
                        if max_input:
                            max_changes = int(max_input)
                    except ValueError:
                        print(f"Using default: {max_changes}")
                    
                    result = optimize_custom_murugan_name(custom_name, max_changes)
                    
                    # Offer to tweet successful optimization
                    if twitter_enabled and result['successful_tweaks']:
                        post_choice = input("Post optimization to Twitter? (y/n): ").strip().lower()
                        if post_choice in ['y', 'yes']:
                            best_tweak = result['best_tweak']
                            tweet_text = f"🕉️ Murugan Name Optimization 🕉️\n\n"
                            tweet_text += f"Original: {result['original']}\n"
                            tweet_text += f"Optimized: {best_tweak['tweaked']}\n"
                            tweet_text += f"Chaldean: {best_tweak['chaldean_sum']} (Lucky 5)\n"
                            tweet_text += f"Changes: {best_tweak['num_changes']}\n\n"
                            tweet_text += "#Murugan #NameOptimization #Numerology"
                            
                            result_post = twitter_poster.create_tweet(tweet_text)
                            if 'error' in result_post:
                                print(f"❌ Failed to post: {result_post['message']}")
                            else:
                                print("✅ Posted to Twitter successfully!")
            
            elif choice == '5':
                print("🔸 Optimizing 'Chaarvik' for Lord Murugan...")
                result = optimize_custom_murugan_name('Chaarvik', 3)
                
                if twitter_enabled and result['successful_tweaks']:
                    post_choice = input("Share Chaarvik optimization on Twitter? (y/n): ").strip().lower()
                    if post_choice in ['y', 'yes']:
                        best_tweak = result['best_tweak']
                        tweet_text = f"🕉️ Chaarvik → Murugan Blessed Name 🕉️\n\n"
                        tweet_text += f"Optimized: {best_tweak['tweaked']}\n"
                        tweet_text += f"Chaldean: {best_tweak['chaldean_sum']} (Lucky 5)\n"
                        tweet_text += f"Perfect for Lord Subramanya devotion!\n\n"
                        tweet_text += "#Chaarvik #Murugan #BabyNames"
                        
                        result_post = twitter_poster.create_tweet(tweet_text)
                        if 'error' in result_post:
                            print(f"❌ Failed to post: {result_post['message']}")
                        else:
                            print("✅ Posted blessed name to Twitter!")
            
            else:
                print("Please enter a valid choice (1-5)")
                
        except KeyboardInterrupt:
            print("\n🙏 Om Muruga! May Lord Subramanya bless your child! 🙏")
            break
        except Exception as e:
            print(f"❌ An error occurred: {e}")

def command_line_mode(args):
    """Command line mode for Murugan name finder."""
    if args.list_perfect:
        display_perfect_murugan_names()
    elif args.list_all:
        display_all_murugan_names()
    elif args.find_best:
        find_best_murugan_names_for_optimization()
    elif args.optimize:
        result = optimize_custom_murugan_name(args.optimize, args.max_changes)
        
        # Auto-post if enabled and successful
        if args.auto_post and result['successful_tweaks']:
            try:
                twitter_poster = TwitterPoster()
                best_tweak = result['best_tweak']
                tweet_text = f"🕉️ Murugan Name Optimization 🕉️\n\n"
                tweet_text += f"Original: {result['original']}\n"
                tweet_text += f"Optimized: {best_tweak['tweaked']}\n"
                tweet_text += f"Chaldean: {best_tweak['chaldean_sum']} (Lucky 5)\n\n"
                tweet_text += "#Murugan #BabyNames #Numerology"
                
                result_post = twitter_poster.create_tweet(tweet_text)
                if 'error' in result_post:
                    print(f"❌ Failed to post: {result_post['message']}")
                else:
                    print("✅ Posted to Twitter successfully!")
            except Exception as e:
                print(f"❌ Twitter posting failed: {e}")

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Find and optimize Murugan names starting with 'Cha'")
    parser.add_argument('--list-perfect', action='store_true',
                       help='List all perfect Murugan names (Chaldean 14/41)')
    parser.add_argument('--list-all', action='store_true',
                       help='List all Murugan names with analysis')
    parser.add_argument('--find-best', action='store_true',
                       help='Find best names for optimization')
    parser.add_argument('--optimize', type=str,
                       help='Optimize a specific name')
    parser.add_argument('-m', '--max-changes', type=int, default=3,
                       help='Maximum changes for optimization (default: 3)')
    parser.add_argument('-p', '--auto-post', action='store_true',
                       help='Auto-post successful optimizations to Twitter')
    parser.add_argument('-i', '--interactive', action='store_true',
                       help='Run in interactive mode')
    
    args = parser.parse_args()
    
    if args.interactive or not any([args.list_perfect, args.list_all, args.find_best, args.optimize]):
        interactive_murugan_name_finder()
    else:
        command_line_mode(args)

if __name__ == "__main__":
    main()