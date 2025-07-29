#!/usr/bin/env python3
"""
Chaldean Name Optimizer

A program that takes a name as input, calculates its Chaldean numerology value,
and suggests tweaks to achieve a target value of 14 or 41 (which reduce to 5).
Can automatically post successful optimizations to Twitter.
"""

import sys
import argparse
from typing import List, Dict, Any

from chaldean_numerology import get_name_analysis, is_target_value
from name_tweaker import find_target_tweaks, format_tweak_result
from twitter_poster import TwitterPoster


def print_name_analysis(name: str) -> None:
    """Print detailed analysis of a name's Chaldean numerology."""
    analysis = get_name_analysis(name)
    
    print(f"\n{'='*50}")
    print(f"CHALDEAN NUMEROLOGY ANALYSIS")
    print(f"{'='*50}")
    print(f"Name: {analysis['name']}")
    print(f"Clean Name: {analysis['clean_name']}")
    print(f"Total Sum: {analysis['total_sum']}")
    print(f"Reduced Value: {analysis['reduced_value']}")
    print(f"Target Achieved: {'✅ YES' if analysis['is_target'] else '❌ NO'}")
    
    print(f"\nLetter Breakdown:")
    for item in analysis['letter_breakdown']:
        print(f"  {item['letter']}: {item['value']}")
    
    print(f"{'='*50}\n")


def print_tweaks(tweaks: List[Dict[str, Any]]) -> None:
    """Print all found tweaks."""
    if not tweaks:
        print("❌ No valid tweaks found to achieve target values (14 or 41).")
        return
    
    print(f"\n🎯 Found {len(tweaks)} valid tweak(s):\n")
    for i, tweak in enumerate(tweaks, 1):
        print(f"Option {i}:")
        print(format_tweak_result(tweak))
        print("-" * 40)


def interactive_mode():
    """Run the program in interactive mode."""
    print("🌟 Welcome to the Chaldean Name Optimizer! 🌟")
    print("This program helps optimize names to achieve Chaldean numerology values of 14 or 41 (which reduce to 5).")
    print("Type 'quit' to exit.\n")
    
    twitter_poster = None
    twitter_enabled = False
    
    # Check if Twitter integration is available
    try:
        twitter_poster = TwitterPoster()
        test_result = twitter_poster.test_connection()
        if test_result['success']:
            twitter_enabled = True
            print("✅ Twitter integration enabled!")
        else:
            print("⚠️  Twitter integration disabled (check your API credentials)")
    except Exception:
        print("⚠️  Twitter integration disabled (credentials not found)")
    
    print()
    
    while True:
        try:
            name = input("Enter a name to analyze: ").strip()
            
            if name.lower() in ['quit', 'exit', 'q']:
                print("Goodbye! 👋")
                break
            
            if not name:
                print("Please enter a valid name.")
                continue
            
            # Analyze the original name
            print_name_analysis(name)
            
            # If already target, congratulate and optionally tweet
            if is_target_value(name):
                print("🎉 This name already has a perfect Chaldean value!")
                
                if twitter_enabled:
                    post_choice = input("Would you like to post this to Twitter? (y/n): ").strip().lower()
                    if post_choice in ['y', 'yes']:
                        # Create a fake tweak result for perfect names
                        tweak_result = {
                            'original': name,
                            'tweaked': name,
                            'chaldean_sum': get_name_analysis(name)['total_sum'],
                            'changes': [],
                            'num_changes': 0
                        }
                        
                        result = twitter_poster.post_name_optimization(tweak_result)
                        if 'error' in result:
                            print(f"❌ Failed to post to Twitter: {result['message']}")
                        else:
                            print("✅ Posted to Twitter successfully!")
                continue
            
            # Find tweaks
            max_changes = 2
            try:
                max_input = input(f"Maximum changes allowed (default {max_changes}): ").strip()
                if max_input:
                    max_changes = int(max_input)
            except ValueError:
                print(f"Invalid input, using default: {max_changes}")
            
            print(f"\n🔍 Searching for tweaks (max {max_changes} changes)...")
            tweaks = find_target_tweaks(name, max_changes=max_changes)
            
            print_tweaks(tweaks)
            
            # If tweaks found and Twitter enabled, offer to post
            if tweaks and twitter_enabled:
                post_choice = input("Would you like to post the best tweak to Twitter? (y/n): ").strip().lower()
                if post_choice in ['y', 'yes']:
                    result = twitter_poster.post_name_optimization(tweaks[0])
                    if 'error' in result:
                        print(f"❌ Failed to post to Twitter: {result['message']}")
                    else:
                        print("✅ Posted to Twitter successfully!")
            
            print("\n" + "="*50 + "\n")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"❌ An error occurred: {e}")


def command_line_mode(args):
    """Run the program in command-line mode."""
    name = args.name
    max_changes = args.max_changes
    auto_post = args.auto_post
    
    # Analyze the original name
    print_name_analysis(name)
    
    # If already target and auto-post enabled
    if is_target_value(name):
        print("🎉 This name already has a perfect Chaldean value!")
        
        if auto_post:
            try:
                twitter_poster = TwitterPoster()
                tweak_result = {
                    'original': name,
                    'tweaked': name,
                    'chaldean_sum': get_name_analysis(name)['total_sum'],
                    'changes': [],
                    'num_changes': 0
                }
                
                result = twitter_poster.post_name_optimization(tweak_result)
                if 'error' in result:
                    print(f"❌ Failed to post to Twitter: {result['message']}")
                else:
                    print("✅ Posted to Twitter successfully!")
            except Exception as e:
                print(f"❌ Twitter posting failed: {e}")
        return
    
    # Find tweaks
    print(f"\n🔍 Searching for tweaks (max {max_changes} changes)...")
    tweaks = find_target_tweaks(name, max_changes=max_changes)
    
    print_tweaks(tweaks)
    
    # Auto-post if enabled and tweaks found
    if tweaks and auto_post:
        try:
            twitter_poster = TwitterPoster()
            result = twitter_poster.post_name_optimization(tweaks[0])
            if 'error' in result:
                print(f"❌ Failed to post to Twitter: {result['message']}")
            else:
                print("✅ Posted to Twitter successfully!")
        except Exception as e:
            print(f"❌ Twitter posting failed: {e}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Optimize names for Chaldean numerology values of 14 or 41")
    parser.add_argument('name', nargs='?', help='Name to analyze and optimize')
    parser.add_argument('-m', '--max-changes', type=int, default=2, 
                       help='Maximum number of letter changes (default: 2)')
    parser.add_argument('-p', '--auto-post', action='store_true',
                       help='Automatically post successful tweaks to Twitter')
    parser.add_argument('-i', '--interactive', action='store_true',
                       help='Run in interactive mode')
    
    args = parser.parse_args()
    
    if args.interactive or not args.name:
        interactive_mode()
    else:
        command_line_mode(args)


if __name__ == "__main__":
    main()