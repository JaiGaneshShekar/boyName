"""
Chaldean Numerology Calculator

This module provides functions to calculate Chaldean numerology values for names.
In Chaldean numerology, letters are assigned values 1-8 (9 is not used).
"""

def get_chaldean_value(letter):
    """
    Get the Chaldean numerology value for a single letter.
    
    Args:
        letter (str): A single letter
        
    Returns:
        int: The Chaldean value (1-8)
    """
    letter = letter.upper()
    
    chaldean_map = {
        'A': 1, 'I': 1, 'J': 1, 'Q': 1, 'Y': 1,
        'B': 2, 'K': 2, 'R': 2,
        'C': 3, 'G': 3, 'L': 3, 'S': 3,
        'D': 4, 'M': 4, 'T': 4,
        'E': 5, 'H': 5, 'N': 5, 'X': 5,
        'U': 6, 'V': 6, 'W': 6,
        'O': 7, 'Z': 7,
        'F': 8, 'P': 8
    }
    
    return chaldean_map.get(letter, 0)


def calculate_chaldean_sum(name):
    """
    Calculate the total Chaldean numerology value for a name.
    
    Args:
        name (str): The name to calculate
        
    Returns:
        int: The total Chaldean sum
    """
    total = 0
    for letter in name:
        if letter.isalpha():
            total += get_chaldean_value(letter)
    return total


def reduce_to_single_digit(number):
    """
    Reduce a number to a single digit by repeatedly adding its digits.
    
    Args:
        number (int): The number to reduce
        
    Returns:
        int: The reduced single digit
    """
    while number > 9:
        number = sum(int(digit) for digit in str(number))
    return number


def get_name_analysis(name):
    """
    Get complete Chaldean numerology analysis for a name.
    
    Args:
        name (str): The name to analyze
        
    Returns:
        dict: Analysis containing total sum, reduced value, and letter breakdown
    """
    name_clean = ''.join(letter for letter in name if letter.isalpha())
    total_sum = calculate_chaldean_sum(name_clean)
    reduced_value = reduce_to_single_digit(total_sum)
    
    letter_breakdown = []
    for letter in name_clean:
        letter_breakdown.append({
            'letter': letter,
            'value': get_chaldean_value(letter)
        })
    
    return {
        'name': name,
        'clean_name': name_clean,
        'total_sum': total_sum,
        'reduced_value': reduced_value,
        'letter_breakdown': letter_breakdown,
        'is_target': total_sum in [14, 41]  # Both reduce to 5
    }


def is_target_value(name):
    """
    Check if a name has the target Chaldean value (14 or 41).
    
    Args:
        name (str): The name to check
        
    Returns:
        bool: True if the name has target value
    """
    total = calculate_chaldean_sum(name)
    return total in [14, 41]