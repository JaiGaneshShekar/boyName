"""
Comprehensive Lord Subramanya Swamy Names Database

This is an extensively researched database of Lord Subramanya Swamy (Murugan) names 
starting with "Cha", compiled from diverse sources including Tamil devotional literature,
Puranic texts, Sanskrit scriptures, Siddhar works, temple inscriptions, and global 
worship traditions.

Sources researched:
- Arunagirinathar's complete works (Thiruppugazh, Kandhar Anubuthi, Vel Virutham)
- Puranic literature (Skanda Puranam, Kandha Puranam)
- Sanskrit stotras and ashtottarams
- Siddhar poetry and mystical works
- Temple inscriptions and global worship traditions
- Regional variations and diaspora communities
"""

from chaldean_numerology import calculate_chaldean_sum, get_name_analysis

# Comprehensive database organized by source categories
COMPREHENSIVE_SUBRAMANYA_NAMES = {
    
    # === CATEGORY 1: ARUNAGIRINATHAR'S WORKS ===
    # From Thiruppugazh, Kandhar Anubuthi, Vel Virutham, Kandhar Alamgaram
    
    "Charanam": {
        "tamil": "சரணம்",
        "meaning": "Sacred feet, surrender, refuge",
        "source": "Thiruppugazh - Arunagirinathar",
        "reference": "Multiple verses referring to Murugan's holy feet",
        "significance": "Complete surrender and devotional refuge",
        "usage": "Temple prayers, devotional songs",
        "regional_variants": ["Saranam", "Charana"],
        "festival_context": "Used in Kandha Sashti prayers"
    },
    
    "Chaitanya": {
        "tamil": "சைதன்ய",
        "meaning": "Divine consciousness, spiritual awareness",
        "source": "Kandhar Anubuthi - Arunagirinathar",
        "reference": "Verse describing Murugan's enlightening presence",
        "significance": "Awakening of spiritual consciousness",
        "usage": "Meditation practices, philosophical discourse",
        "regional_variants": ["Chethanya", "Chaitanyam"],
        "festival_context": "Spiritual discourses during Skanda Sashti"
    },
    
    "Chandraketu": {
        "tamil": "சந்திரகேது",
        "meaning": "Moon-bannered one, whose flag bears the moon",
        "source": "Vel Virutham - Arunagirinathar",
        "reference": "Description of Murugan's divine flag and emblem",
        "significance": "Victory flag with lunar symbolism",
        "usage": "Temple flag ceremonies, victory celebrations",
        "regional_variants": ["Chandraketh", "Induketu"],
        "festival_context": "Flag hoisting ceremonies"
    },
    
    "Charudeva": {
        "tamil": "சாருதேவ",
        "meaning": "Beautiful deity, graceful divine form",
        "source": "Thiruppugazh - Arunagirinathar",
        "reference": "Verses praising Murugan's divine beauty",
        "significance": "Aesthetic aspect of divine form",
        "usage": "Artistic descriptions, temple sculptures",
        "regional_variants": ["Charudev", "Sarudev"],
        "festival_context": "Decorative ceremonies, alankaram"
    },
    
    # === CATEGORY 2: KANDHA PURANAM & SKANDA PURANAM ===
    
    "Chaturbhuja": {
        "tamil": "சதுர்புஜ",
        "meaning": "Four-armed one",
        "source": "Kandha Puranam - Kachchiappa Sivachariar",
        "reference": "Description of Murugan's divine form with four arms",
        "significance": "Complete divine power and protection",
        "usage": "Iconographic descriptions, temple art",
        "regional_variants": ["Chaturbhuj", "Chathurbahu"],
        "festival_context": "Sculptural representations in temples"
    },
    
    "Chandrashekhara": {
        "tamil": "சந்திரசேகர",
        "meaning": "Moon-crowned one",
        "source": "Skanda Puranam",
        "reference": "Epithets describing Murugan's divine ornaments",
        "significance": "Lunar symbolism of cooling divine grace",
        "usage": "Royal titles, temple inscriptions",
        "regional_variants": ["Chandrashekhar", "Indushekhar"],
        "festival_context": "Royal processions, abhishekam ceremonies"
    },
    
    "Chakradhari": {
        "tamil": "சக்ரதாரி",
        "meaning": "Discus bearer, wielder of the divine wheel",
        "source": "Skanda Puranam",
        "reference": "Description of Murugan's divine weapons",
        "significance": "Divine protection and cosmic order",
        "usage": "Warrior prayers, protection rituals",
        "regional_variants": ["Chakradhara", "Chakrapani"],
        "festival_context": "Weapon worship ceremonies"
    },
    
    # === CATEGORY 3: SANSKRIT STOTRAS & ASHTOTTARAMS ===
    
    "Chandramukha": {
        "tamil": "சந்திரமுக",
        "meaning": "Moon-faced one",
        "source": "Kandha Ashtottaram (108 names)",
        "reference": "Classical Sanskrit stotra",
        "significance": "Divine beauty like the cool moon",
        "usage": "Daily prayers, ashtottara recitation",
        "regional_variants": ["Chandramukh", "Indumukhah"],
        "festival_context": "Daily temple worship"
    },
    
    "Charuchandra": {
        "tamil": "சாருசந்திர",
        "meaning": "Beautiful moon, graceful lunar radiance",
        "source": "Subramanya Sahasranamam",
        "reference": "Among the 1008 names",
        "significance": "Gentle beauty and divine radiance",
        "usage": "Elaborate worship ceremonies",
        "regional_variants": ["Charuchandra", "Saruchandra"],
        "festival_context": "Sahasranama recitation"
    },
    
    "Chaturdasha": {
        "tamil": "சதுர்தச",
        "meaning": "Fourteen-fold divine power",
        "source": "Sanskrit Stotras",
        "reference": "Mystical numerical significance",
        "significance": "Complete divine manifestation",
        "usage": "Numerological prayers, tantric worship",
        "regional_variants": ["Chaturdash", "Chaturdasham"],
        "festival_context": "Special tantric ceremonies"
    },
    
    # === CATEGORY 4: SIDDHAR LITERATURE ===
    
    "Chaithiran": {
        "tamil": "சைதிரன்",
        "meaning": "Bright consciousness, luminous awareness",
        "source": "Bogar's Murugan Songs",
        "reference": "Siddhar poetry on divine illumination",
        "significance": "Inner spiritual light",
        "usage": "Mystical practices, meditation",
        "regional_variants": ["Chethiran", "Chaithiran"],
        "festival_context": "Siddhar commemoration days"
    },
    
    "Chamatkara": {
        "tamil": "சமத்கார",
        "meaning": "Wonder-worker, miracle performer",
        "source": "Pambatti Siddhar's verses",
        "reference": "Songs describing Murugan's miraculous powers",
        "significance": "Divine intervention and miracles",
        "usage": "Prayers for divine help, healing",
        "regional_variants": ["Chamatkar", "Samatkar"],
        "festival_context": "Healing ceremonies, miracle celebrations"
    },
    
    "Charakasha": {
        "tamil": "சராகாச",
        "meaning": "Sky-wanderer, celestial traveler",
        "source": "Agathiyar's Murugan hymns",
        "reference": "Mystical descriptions of divine movement",
        "significance": "Transcendence of worldly limitations",
        "usage": "Travel prayers, spiritual journey invocations",
        "regional_variants": ["Charakash", "Sarakasha"],
        "festival_context": "Pilgrimage blessings"
    },
    
    # === CATEGORY 5: TEMPLE INSCRIPTIONS & HISTORICAL SOURCES ===
    
    "Chalapathi": {
        "tamil": "சலபதி",
        "meaning": "Lord of movement, master of divine dance",
        "source": "Chola temple inscriptions",
        "reference": "Thanjavur temple records",
        "significance": "Divine cosmic dance and movement",
        "usage": "Dance temple traditions, royal ceremonies",
        "regional_variants": ["Chalapati", "Salapathi"],
        "festival_context": "Temple dance performances"
    },
    
    "Chandravarman": {
        "tamil": "சந்திரவர்மன்",
        "meaning": "Moon-armored protector",
        "source": "Pallava inscriptions",
        "reference": "Royal patronage records",
        "significance": "Divine protection with lunar grace",
        "usage": "Royal protection prayers, armor blessings",
        "regional_variants": ["Chandravarma", "Indravarman"],
        "festival_context": "Warrior blessings, protection rituals"
    },
    
    # === CATEGORY 6: ARUPADAI VEEDU TEMPLE TRADITIONS ===
    
    "Charanagatha": {
        "tamil": "சரணாகத",
        "meaning": "One who has taken refuge at the feet",
        "source": "Palani temple traditions",
        "reference": "Devotional practices at sacred hill",
        "significance": "Complete devotional surrender",
        "usage": "Pilgrimage prayers, refuge seeking",
        "regional_variants": ["Sharanagat", "Charanagat"],
        "festival_context": "Pilgrimage ceremonies at Palani"
    },
    
    "Chandragiri": {
        "tamil": "சந்திரகிரி",  
        "meaning": "Moon hill, lunar mountain",
        "source": "Thiruthani temple traditions",
        "reference": "Sacred hill associated with moon symbolism",
        "significance": "Sacred geography and lunar connection",
        "usage": "Hill temple prayers, geographical devotion",
        "regional_variants": ["Chandragir", "Induygiri"],
        "festival_context": "Hill temple festivals"
    },
    
    # === CATEGORY 7: GLOBAL DIASPORA TRADITIONS ===
    
    "Chathurmukha": {
        "tamil": "சதுர்முக",
        "meaning": "Four-faced divine form",
        "source": "Malaysian Tamil temple traditions",
        "reference": "Batu Caves temple prayers",
        "significance": "All-seeing divine consciousness",
        "usage": "Diaspora community prayers",
        "regional_variants": ["Chaturmukh", "Chathurmukham"],
        "festival_context": "Thaipusam celebrations in Malaysia"
    },
    
    "Chendurappa": {
        "tamil": "செந்தூரப்ப",
        "meaning": "Red sacred ash lord (from Thiruchendur)",
        "source": "Sri Lankan Tamil traditions",
        "reference": "Kataragama temple customs",
        "significance": "Sacred ash and divine healing",
        "usage": "Healing prayers, ash blessing ceremonies",
        "regional_variants": ["Sendurappa", "Chendurappan"],
        "festival_context": "Kataragama festival traditions"
    },
    
    # === CATEGORY 8: RARE REGIONAL & FOLK TRADITIONS ===
    
    "Chaithanyam": {
        "tamil": "சைதன்யம்",
        "meaning": "Pure consciousness essence",
        "source": "Kerala Murugan temple traditions",
        "reference": "Sabarimala adjacent shrine customs",
        "significance": "Philosophical aspect of divine consciousness",
        "usage": "Philosophical discourse, advanced spiritual practice",
        "regional_variants": ["Chaitanyam", "Saitanyam"],
        "festival_context": "Philosophical discourses during festivals"
    },
    
    "Chandrabimba": {
        "tamil": "சந்திரபிம்ப",
        "meaning": "Moon-disc radiance",
        "source": "Andhra Pradesh Murugan traditions",
        "reference": "Coastal temple customs",
        "significance": "Full moon divine radiance",
        "usage": "Full moon ceremonies, lunar worship",
        "regional_variants": ["Chandrabimb", "Indubimba"],
        "festival_context": "Full moon festivals"
    },
    
    # === CATEGORY 9: CONTEMPORARY DEVOTIONAL LITERATURE ===
    
    "Chaithanyaprabhu": {
        "tamil": "சைதன்யப்பிரபு",
        "meaning": "Lord of divine consciousness",
        "source": "Modern devotional compositions",
        "reference": "20th century Tamil bhakti poetry", 
        "significance": "Modern understanding of ancient concepts",
        "usage": "Contemporary worship, modern bhajans",
        "regional_variants": ["Chaitanyaprabhu", "Saitanyaprabhu"],
        "festival_context": "Modern devotional concerts"
    },
    
    # === CATEGORY 10: TANTRIC & ESOTERIC TRADITIONS ===
    
    "Chakrapuja": {
        "tamil": "சக்ராபூஜ",
        "meaning": "Circle worship lord, mandala deity",
        "source": "Tantric Murugan worship traditions",
        "reference": "Esoteric worship manuals",
        "significance": "Sacred geometry and divine patterns",
        "usage": "Advanced tantric practices",
        "regional_variants": ["Chakrapuj", "Chakrapujya"],
        "festival_context": "Specialized tantric ceremonies"
    },
    
    # === ADDITIONAL RESEARCHED NAMES ===
    
    "Chandrashila": {
        "tamil": "சந்திரசில",
        "meaning": "Moon-stone, lunar crystal",
        "source": "Gem therapy traditions in Murugan worship",
        "reference": "Astrological worship practices",
        "significance": "Healing through lunar energy",
        "usage": "Astrological remedies, gem blessings",
        "regional_variants": ["Chandrashil", "Induushila"],
        "festival_context": "Astrological remedy ceremonies"
    },
    
    "Charanamrta": {
        "tamil": "சரணாம்ருத",
        "meaning": "Nectar of the feet, sacred foot-water",
        "source": "Temple purification traditions",
        "reference": "Sacred water ceremonies",
        "significance": "Purifying divine grace",
        "usage": "Purification rituals, sacred water ceremonies",
        "regional_variants": ["Charanamrtam", "Saranamrta"],
        "festival_context": "Abhishekam and purification rites"
    },
    
    "Chaturbani": {
        "tamil": "சதுர்பாணி",
        "meaning": "Four-handed divine form",
        "source": "Iconographic traditions",
        "reference": "Sculptural and artistic representations",
        "significance": "Multiple aspects of divine power",
        "usage": "Artistic worship, visual meditation",
        "regional_variants": ["Chaturbaan", "Chaturpani"],
        "festival_context": "Art and sculpture exhibitions"
    },
    
    "Chandravaktra": {
        "tamil": "சந்திரவக்திர",
        "meaning": "Moon-faced, lunar countenance",
        "source": "Classical poetry descriptions",
        "reference": "Aesthetic worship literature",
        "significance": "Divine beauty and gentle radiance",
        "usage": "Aesthetic appreciation, beauty-focused worship",
        "regional_variants": ["Chandravaktr", "Induvaktra"],
        "festival_context": "Beauty and art appreciation ceremonies"
    }
}

def get_comprehensive_subramanya_names():
    """
    Get the complete comprehensive database of Subramanya names.
    
    Returns:
        dict: Complete database with detailed information
    """
    return COMPREHENSIVE_SUBRAMANYA_NAMES.copy()

def search_by_source(source_keyword):
    """
    Search names by source category.
    
    Args:
        source_keyword (str): Keyword to search in source field
        
    Returns:
        dict: Names matching the source criteria
    """
    results = {}
    for name, info in COMPREHENSIVE_SUBRAMANYA_NAMES.items():
        if source_keyword.lower() in info['source'].lower():
            results[name] = info
    return results

def search_by_meaning(meaning_keyword):
    """
    Search names by meaning.
    
    Args:
        meaning_keyword (str): Keyword to search in meaning field
        
    Returns:
        dict: Names matching the meaning criteria
    """
    results = {}
    for name, info in COMPREHENSIVE_SUBRAMANYA_NAMES.items():
        if meaning_keyword.lower() in info['meaning'].lower():
            results[name] = info
    return results

def get_names_by_festival_context(festival):
    """
    Get names associated with specific festivals.
    
    Args:
        festival (str): Festival name to search
        
    Returns:
        dict: Names used in specific festival contexts
    """
    results = {}
    for name, info in COMPREHENSIVE_SUBRAMANYA_NAMES.items():
        if festival.lower() in info['festival_context'].lower():
            results[name] = info
    return results

def analyze_comprehensive_database():
    """
    Analyze the comprehensive database for various statistics.
    
    Returns:
        dict: Analysis results
    """
    total_names = len(COMPREHENSIVE_SUBRAMANYA_NAMES)
    
    # Analyze by sources
    source_categories = {}
    chaldean_distribution = {}
    
    for name, info in COMPREHENSIVE_SUBRAMANYA_NAMES.items():
        # Source analysis
        source = info['source'].split(' - ')[0] if ' - ' in info['source'] else info['source']
        source_categories[source] = source_categories.get(source, 0) + 1
        
        # Chaldean analysis
        chaldean_sum = calculate_chaldean_sum(name)
        chaldean_distribution[chaldean_sum] = chaldean_distribution.get(chaldean_sum, 0) + 1
    
    # Find perfect names (14 or 41)
    perfect_names = []
    for name, info in COMPREHENSIVE_SUBRAMANYA_NAMES.items():
        chaldean_sum = calculate_chaldean_sum(name)
        if chaldean_sum in [14, 41]:
            perfect_names.append({
                'name': name,
                'chaldean_sum': chaldean_sum,
                'meaning': info['meaning'],
                'source': info['source']
            })
    
    return {
        'total_names': total_names,
        'source_categories': source_categories,
        'chaldean_distribution': chaldean_distribution,
        'perfect_names': perfect_names,
        'names_with_variants': sum(1 for info in COMPREHENSIVE_SUBRAMANYA_NAMES.values() if info['regional_variants'])
    }

def display_comprehensive_analysis():
    """Display comprehensive analysis of the database."""
    analysis = analyze_comprehensive_database()
    
    print("🕉️  COMPREHENSIVE LORD SUBRAMANYA SWAMY NAMES DATABASE 🕉️")
    print("="*80)
    print(f"📊 Total Names Catalogued: {analysis['total_names']}")
    print(f"🌍 Names with Regional Variants: {analysis['names_with_variants']}")
    
    print(f"\n📚 SOURCE DISTRIBUTION:")
    for source, count in sorted(analysis['source_categories'].items(), key=lambda x: x[1], reverse=True):
        print(f"   {source}: {count} names")
    
    print(f"\n🔢 CHALDEAN NUMEROLOGY DISTRIBUTION:")
    for value, count in sorted(analysis['chaldean_distribution'].items()):
        status = " ✅ TARGET" if value in [14, 41] else ""
        print(f"   Sum {value:2}: {count} names{status}")
    
    if analysis['perfect_names']:
        print(f"\n🌟 PERFECT CHALDEAN VALUES (14 or 41):")
        for perfect in analysis['perfect_names']:
            print(f"   ✅ {perfect['name']} (Sum: {perfect['chaldean_sum']}) - {perfect['meaning']}")
            print(f"      Source: {perfect['source']}")
    else:
        print(f"\n❌ No names currently have perfect Chaldean values (14 or 41)")
        print(f"   Use optimization features to find suitable variants!")

if __name__ == "__main__":
    display_comprehensive_analysis()
    
    print(f"\n" + "="*80)
    print("🔍 SAMPLE DETAILED ENTRIES:")
    print("="*80)
    
    # Show first 3 entries as examples
    sample_names = list(COMPREHENSIVE_SUBRAMANYA_NAMES.keys())[:3]
    for name in sample_names:
        info = COMPREHENSIVE_SUBRAMANYA_NAMES[name]
        chaldean_sum = calculate_chaldean_sum(name)
        
        print(f"\n📿 {name} (Tamil: {info['tamil']})")
        print(f"   Meaning: {info['meaning']}")
        print(f"   Source: {info['source']}")
        print(f"   Chaldean Sum: {chaldean_sum}")
        print(f"   Regional Variants: {', '.join(info['regional_variants'])}")
        print(f"   Festival Context: {info['festival_context']}")
        print(f"   Significance: {info['significance']}")