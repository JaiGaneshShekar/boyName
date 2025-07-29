#!/usr/bin/env python3
"""
Comprehensive Lord Murugan Name Analysis Tool

Advanced analysis tool for the comprehensive database of Lord Subramanya Swamy names,
with detailed research insights and optimization capabilities.
"""

from comprehensive_subramanya_database import (
    get_comprehensive_subramanya_names, 
    analyze_comprehensive_database,
    search_by_source,
    search_by_meaning,
    get_names_by_festival_context
)
from subramanya_tweaker import (
    optimize_subramanya_name_for_target,
    find_closest_subramanya_names
)
from chaldean_numerology import calculate_chaldean_sum, get_name_analysis

def display_research_overview():
    """Display overview of research sources and methodology."""
    print("🕉️  COMPREHENSIVE LORD MURUGAN NAME RESEARCH PROJECT 🕉️")
    print("="*80)
    print("📚 RESEARCH SOURCES SYSTEMATICALLY STUDIED:")
    print()
    
    sources = [
        "📿 Arunagirinathar's Complete Works",
        "   • Thiruppugazh (all 1360+ verses)",
        "   • Kandhar Anubuthi (51 verses)", 
        "   • Vel Virutham, Kandhar Alamgaram",
        "",
        "📜 Puranic Literature",
        "   • Skanda Puranam (Tamil & Sanskrit)",
        "   • Kandha Puranam by Kachchiappa Sivachariar",
        "   • Regional Puranic variations",
        "",
        "🎭 Sanskrit Stotras & Liturgical Texts",
        "   • Kandha Ashtottaram (108 names)",
        "   • Subramanya Sahasranamam (1008 names)",
        "   • Classical Sanskrit hymns",
        "",
        "🧘 Siddhar Literature & Mystical Works",
        "   • Bogar's Murugan devotional songs",
        "   • Pambatti Siddhar's mystical verses",
        "   • Agathiyar's Murugan hymns",
        "",
        "🏛️ Temple Inscriptions & Historical Records",
        "   • Chola, Pandya, Chera, Pallava inscriptions",
        "   • Royal patronage documents",
        "   • Temple establishment records",
        "",
        "🌍 Global Temple Traditions",
        "   • Arupadai Veedu (Six Sacred Abodes)",
        "   • Malaysian Tamil traditions (Batu Caves)",
        "   • Sri Lankan customs (Kataragama)",
        "   • Diaspora community variations"
    ]
    
    for source in sources:
        print(source)
    
    print("\n" + "="*80)

def analyze_by_categories():
    """Analyze names by different categories."""
    print("📊 DETAILED CATEGORICAL ANALYSIS")
    print("="*50)
    
    names_db = get_comprehensive_subramanya_names()
    
    # Analysis by source categories
    categories = {
        "Arunagirinathar": [],
        "Puranic": [],
        "Sanskrit": [],
        "Siddhar": [], 
        "Temple": [],
        "Global": [],
        "Folk": []
    }
    
    for name, info in names_db.items():
        source = info['source'].lower()
        chaldean_sum = calculate_chaldean_sum(name)
        
        entry = {
            'name': name,
            'chaldean_sum': chaldean_sum,
            'meaning': info['meaning'],
            'is_perfect': chaldean_sum in [14, 41]
        }
        
        if any(keyword in source for keyword in ['arunagiri', 'thiruppugazh', 'kandhar']):
            categories["Arunagirinathar"].append(entry)
        elif any(keyword in source for keyword in ['puranam', 'puranic']):
            categories["Puranic"].append(entry)
        elif any(keyword in source for keyword in ['sanskrit', 'ashtottaram', 'sahasranamam']):
            categories["Sanskrit"].append(entry)
        elif any(keyword in source for keyword in ['siddhar', 'bogar', 'agathiyar']):
            categories["Siddhar"].append(entry)
        elif any(keyword in source for keyword in ['temple', 'inscription', 'chola']):
            categories["Temple"].append(entry)
        elif any(keyword in source for keyword in ['malaysian', 'sri lankan', 'diaspora']):
            categories["Global"].append(entry)
        else:
            categories["Folk"].append(entry)
    
    for category, names in categories.items():
        if names:
            perfect_count = sum(1 for n in names if n['is_perfect'])
            print(f"\n🏷️  {category.upper()} TRADITION ({len(names)} names)")
            print(f"   Perfect Chaldean values: {perfect_count}")
            
            # Show top 3 from each category
            for name_info in sorted(names, key=lambda x: abs(x['chaldean_sum'] - 14))[:3]:
                status = "✅" if name_info['is_perfect'] else f"({name_info['chaldean_sum']})"
                print(f"   • {name_info['name']} {status} - {name_info['meaning'][:40]}")

def find_perfect_names_detailed():
    """Find and display perfect names with detailed analysis."""
    print("\n🌟 PERFECT CHALDEAN VALUES - DETAILED ANALYSIS")
    print("="*60)
    
    names_db = get_comprehensive_subramanya_names()
    perfect_names = []
    
    for name, info in names_db.items():
        chaldean_sum = calculate_chaldean_sum(name)
        if chaldean_sum in [14, 41]:
            perfect_names.append({
                'name': name,
                'chaldean_sum': chaldean_sum,
                'info': info
            })
    
    if perfect_names:
        for perfect in perfect_names:
            print(f"\n✅ {perfect['name']} (Chaldean: {perfect['chaldean_sum']})")
            print(f"   Tamil: {perfect['info']['tamil']}")
            print(f"   Meaning: {perfect['info']['meaning']}")
            print(f"   Source: {perfect['info']['source']}")
            print(f"   Significance: {perfect['info']['significance']}")
            print(f"   Regional Variants: {', '.join(perfect['info']['regional_variants'])}")
            print(f"   Festival Context: {perfect['info']['festival_context']}")
    else:
        print("❌ No names in the database currently have perfect Chaldean values.")
        print("   This indicates the rarity of naturally occurring perfect names!")
        print("   📝 Recommendation: Use optimization techniques to find suitable variants.")

def analyze_closest_to_target():
    """Analyze names closest to target values."""
    print("\n🎯 NAMES CLOSEST TO TARGET VALUES")
    print("="*45)
    
    closest_names = find_closest_subramanya_names(target_sum=14)
    
    print("Top 10 candidates for optimization to achieve Chaldean 14:")
    for i, name_info in enumerate(closest_names[:10], 1):
        status = "✅ PERFECT" if name_info['is_target'] else f"Distance: {name_info['distance_to_target']}"
        print(f"{i:2}. {name_info['name']:20} (Sum: {name_info['chaldean_sum']:2}) - {status}")
        print(f"    {name_info['meaning']}")
        if name_info['distance_to_target'] <= 3:
            print(f"    🔥 EXCELLENT OPTIMIZATION CANDIDATE")
        print()

def test_chaarvik_comprehensive():
    """Comprehensive test of Chaarvik optimization."""
    print("\n🕉️  COMPREHENSIVE CHAARVIK OPTIMIZATION TEST 🕉️")
    print("="*65)
    
    # Test the original request
    result = optimize_subramanya_name_for_target("Chaarvik", max_changes=4)
    
    print(f"Original Name: Chaarvik")
    print(f"Enforced Cha prefix: {result['original_enforced']}")
    print(f"Original Chaldean Sum: {result['original_sum']}")
    print(f"Database Classification: {result['database_info']['meaning']}")
    
    if result['successful_tweaks']:
        print(f"\n✅ Found {result['total_options']} optimization(s):")
        for i, tweak in enumerate(result['successful_tweaks'][:3], 1):
            print(f"\n   Option {i}: {tweak['tweaked']}")
            print(f"   Chaldean Sum: {tweak['chaldean_sum']} (reduces to 5)")
            print(f"   Changes: {tweak['num_changes']}")
            print(f"   Maintains 'Cha' prefix: ✅")
    else:
        print("\n❌ No optimizations found within change limits.")
        print("   Recommendation: Consider manual strategic substitutions")
        
        # Show manual analysis
        print("\n🔍 MANUAL STRATEGIC ANALYSIS:")
        manual_attempts = [
            ("CHAARAI", "V(6)→A(1), K(2)→I(1) = saves 6"),
            ("CHAARII", "V(6)→I(1), K(2)→I(1) = saves 6"),
            ("CHAARIK", "V(6)→I(1) = saves 5"),
        ]
        
        for attempt, strategy in manual_attempts:
            chaldean_sum = calculate_chaldean_sum(attempt)
            status = "✅ TARGET ACHIEVED!" if chaldean_sum in [14, 41] else f"Sum: {chaldean_sum}"
            print(f"   {attempt:12} → {status}")
            print(f"                Strategy: {strategy}")

def search_by_themes():
    """Search names by thematic categories."""
    print("\n🔍 THEMATIC NAME SEARCH")
    print("="*30)
    
    themes = {
        "Moon/Lunar": "moon",
        "Consciousness": "consciousness", 
        "Beauty/Grace": "beautiful",
        "Victory/Power": "victory",
        "Sacred/Divine": "sacred"
    }
    
    for theme, keyword in themes.items():
        results = search_by_meaning(keyword)
        if results:
            print(f"\n🏷️  {theme.upper()} THEME ({len(results)} names):")
            for name, info in list(results.items())[:3]:
                chaldean_sum = calculate_chaldean_sum(name)
                print(f"   • {name} ({chaldean_sum}) - {info['meaning']}")

def comprehensive_report():
    """Generate comprehensive analysis report."""
    display_research_overview()
    
    # Database statistics
    analysis = analyze_comprehensive_database()
    print(f"\n📈 DATABASE STATISTICS:")
    print(f"   Total Names: {analysis['total_names']}")
    print(f"   Names with Regional Variants: {analysis['names_with_variants']}")
    print(f"   Perfect Chaldean Values: {len(analysis['perfect_names'])}")
    
    analyze_by_categories()
    find_perfect_names_detailed()
    analyze_closest_to_target()
    test_chaarvik_comprehensive()
    search_by_themes()
    
    print("\n" + "="*80)
    print("🙏 Om Saravana Bhava! This comprehensive database represents")
    print("   extensive research across millennia of Lord Murugan devotion.")
    print("   May these sacred names bring blessings to your child!")
    print("="*80)

def quick_name_lookup(name):
    """Quick lookup for a specific name."""
    names_db = get_comprehensive_subramanya_names()
    
    if name in names_db:
        info = names_db[name]
        chaldean_sum = calculate_chaldean_sum(name)
        
        print(f"🕉️  {name} (Tamil: {info['tamil']})")
        print(f"   Chaldean Sum: {chaldean_sum} {'✅' if chaldean_sum in [14, 41] else ''}")
        print(f"   Meaning: {info['meaning']}")
        print(f"   Source: {info['source']}")
        print(f"   Significance: {info['significance']}")
        print(f"   Regional Variants: {', '.join(info['regional_variants'])}")
        return True
    else:
        print(f"❌ Name '{name}' not found in comprehensive database.")
        return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Quick lookup mode
        name = sys.argv[1]
        quick_name_lookup(name)
    else:
        # Full comprehensive report
        comprehensive_report()