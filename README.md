# Chaldean Name Optimizer

A Python program that analyzes names using Chaldean numerology and suggests tweaks to achieve target values of 14 or 41 (which reduce to the lucky number 5). Can automatically post successful optimizations to Twitter.

## Features

- **Chaldean Numerology Calculation**: Accurately calculates Chaldean numerology values for any name
- **Smart Name Tweaking**: Uses phonetically similar letter substitutions to preserve meaning and sound
- **Target Value Optimization**: Specifically targets values of 14 and 41 (both reduce to 5)
- **Twitter Integration**: Automatically posts successful name optimizations
- **Interactive & Command-Line Modes**: Flexible usage options

## Installation

1. Clone or download this repository
2. Install required packages:
```bash
pip install -r requirements.txt
```

3. (Optional) Set up Twitter API credentials:
   - Copy `.env.sample` to `.env`
   - Get Twitter API credentials from https://developer.twitter.com/
   - Fill in your credentials in the `.env` file

## Usage

### Interactive Mode
```bash
python main.py
```
or
```bash
python main.py -i
```

### Command Line Mode
```bash
# Analyze a specific name
python main.py "John"

# Limit maximum changes
python main.py "John" --max-changes 1

# Auto-post to Twitter if successful
python main.py "John" --auto-post
```

### Command Line Options
- `-m, --max-changes`: Maximum number of letter changes (default: 2)
- `-p, --auto-post`: Automatically post successful tweaks to Twitter
- `-i, --interactive`: Run in interactive mode

## How It Works

### Chaldean Numerology
In Chaldean numerology, letters are assigned values 1-8 (9 is not used):
- A, I, J, Q, Y = 1
- B, K, R = 2
- C, G, L, S = 3
- D, M, T = 4
- E, H, N, X = 5
- U, V, W = 6
- O, Z = 7
- F, P = 8

### Target Values
The program targets sums of 14 or 41 because:
- 14 reduces to 5 (1+4=5)
- 41 reduces to 5 (4+1=5)
- 5 is considered a lucky number in numerology

### Name Tweaking Strategy
The program uses minimal, phonetically similar substitutions:

**Vowel Substitutions:**
- A ↔ E, AA (elongation)
- E ↔ A, I, EE (elongation)
- I ↔ E, Y, II (elongation)
- O ↔ U, OO (elongation)
- U ↔ O, UU (elongation)

**Consonant Substitutions:**
- B ↔ P (similar sounds)
- C ↔ K, S (hard/soft C)
- D ↔ T (similar sounds)
- F ↔ PH, V (similar sounds)
- And more...

## Example Output

```
==================================================
CHALDEAN NUMEROLOGY ANALYSIS
==================================================
Name: John
Clean Name: JOHN
Total Sum: 20
Reduced Value: 2
Target Achieved: ❌ NO

Letter Breakdown:
  J: 1
  O: 7
  H: 5
  N: 5
==================================================

🔍 Searching for tweaks (max 2 changes)...

🎯 Found 3 valid tweak(s):

Option 1:

Original: John
Tweaked:  JAHN
Chaldean Sum: 14
Changes (1): Changed 'O' to 'A' at position 1

Option 2:

Original: John
Tweaked:  JOAN
Chaldean Sum: 14
Changes (1): Changed 'H' to 'A' at position 2
```

## Twitter Integration

When Twitter credentials are configured, the program can automatically post successful name optimizations. Example tweet:

```
✨ Name Optimization ✨

Original: John
Optimized: Jahn
Chaldean Value: 14 (reduces to 5)
Changes: 1

#Numerology #NameOptimization #ChaldeanNumerology
```

## Files Structure

- `main.py`: Main program interface
- `chaldean_numerology.py`: Core numerology calculations
- `name_tweaker.py`: Name modification algorithms
- `twitter_poster.py`: Twitter API integration
- `requirements.txt`: Python dependencies
- `.env.sample`: Template for environment variables

## Requirements

- Python 3.6+
- requests library
- python-dotenv library (optional, for environment variables)
- Twitter API credentials (optional, for posting)

## Notes

- The program prioritizes minimal changes to preserve the original name's meaning
- Vowel elongations (AA, EE, etc.) are considered single changes
- Results are sorted by fewest changes first
- Twitter posting is optional and requires API credentials