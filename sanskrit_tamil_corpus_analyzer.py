#!/usr/bin/env python3
"""
Sanskrit-Tamil Corpus Cross-Reference Analyzer

Systematic analysis and cross-referencing of Sanskrit and Tamil names for Lord Subramanya Swamy,
keeping the languages separate while identifying relationships and authenticity.
"""

import json
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass
from sanskrit_name_extractor import SanskritNameExtractor, SanskritName
from tamil_name_extractor import TamilNameExtractor, TamilName

@dataclass
class CorpusAnalysis:
    """Analysis results for the combined corpus."""
    sanskrit_names: List[SanskritName]
    tamil_names: List[TamilName]
    total_names: int
    sanskrit_count: int
    tamil_count: int
    source_distribution: Dict[str, int]
    etymology_patterns: Dict[str, List[str]]
    phonetic_relationships: List[Tuple[str, str, str]]  # (sanskrit, tamil, relationship)

class SanskritTamilCorpusAnalyzer:
    """Analyze Sanskrit and Tamil names separately with cross-referencing."""
    
    def __init__(self):
        self.sanskrit_extractor = SanskritNameExtractor()
        self.tamil_extractor = TamilNameExtractor()
        self.analysis_results = None
    
    def process_corpus(self, sanskrit_texts: Dict[str, str], tamil_texts: Dict[str, str]) -> CorpusAnalysis:
        """Process both Sanskrit and Tamil corpora separately."""
        
        print("🕉️  PROCESSING SEPARATE SANSKRIT AND TAMIL CORPORA 🕉️")
        print("="*70)
        
        # Process Sanskrit texts
        print("\n📜 PROCESSING SANSKRIT SOURCES:")
        sanskrit_names = []
        for source_name, text in sanskrit_texts.items():
            print(f"   🔍 Extracting from {source_name}...")
            names = self.sanskrit_extractor.extract_from_text(text, source_name)
            sanskrit_names.extend(names)
            print(f"      Found {len(names)} verified Sanskrit names")
        
        # Process Tamil texts  
        print("\n📿 PROCESSING TAMIL SOURCES:")
        tamil_names = []
        for source_name, text in tamil_texts.items():
            print(f"   🔍 Extracting from {source_name}...")
            names = self.tamil_extractor.extract_from_text(text, source_name)
            tamil_names.extend(names)
            print(f"      Found {len(names)} verified Tamil names")
        
        # Analyze corpus
        analysis = self._analyze_corpus(sanskrit_names, tamil_names)
        self.analysis_results = analysis
        
        return analysis
    
    def _analyze_corpus(self, sanskrit_names: List[SanskritName], tamil_names: List[TamilName]) -> CorpusAnalysis:
        """Analyze the complete corpus."""
        
        # Source distribution
        source_dist = {}
        for name in sanskrit_names:
            source_dist[f"Sanskrit: {name.source_text}"] = source_dist.get(f"Sanskrit: {name.source_text}", 0) + 1
        for name in tamil_names:
            source_dist[f"Tamil: {name.source_text}"] = source_dist.get(f"Tamil: {name.source_text}", 0) + 1
        
        # Etymology patterns
        etymology_patterns = self._analyze_etymology_patterns(sanskrit_names, tamil_names)
        
        # Phonetic relationships (without creating new names)
        phonetic_relationships = self._identify_phonetic_relationships(sanskrit_names, tamil_names)
        
        return CorpusAnalysis(
            sanskrit_names=sanskrit_names,
            tamil_names=tamil_names,
            total_names=len(sanskrit_names) + len(tamil_names),
            sanskrit_count=len(sanskrit_names),
            tamil_count=len(tamil_names),
            source_distribution=source_dist,
            etymology_patterns=etymology_patterns,
            phonetic_relationships=phonetic_relationships
        )
    
    def _analyze_etymology_patterns(self, sanskrit_names: List[SanskritName], tamil_names: List[TamilName]) -> Dict[str, List[str]]:
        """Analyze etymology patterns across languages."""
        patterns = {
            "Sanskrit_roots": [],
            "Tamil_adaptations": [],
            "Common_themes": [],
            "Divine_attributes": []
        }
        
        # Sanskrit roots
        for name in sanskrit_names:
            if name.etymology:
                patterns["Sanskrit_roots"].append(f"{name.devanagari}: {name.etymology}")
        
        # Tamil adaptations (many Tamil names have Sanskrit origins)
        for name in tamil_names:
            if "Sanskrit" in name.lexicon_definition:
                patterns["Tamil_adaptations"].append(f"{name.tamil_script}: adapted from Sanskrit")
        
        # Common themes
        divine_themes = ["moon", "six-faced", "warrior", "consciousness", "beautiful", "powerful"]
        for theme in divine_themes:
            sanskrit_matches = [n.devanagari for n in sanskrit_names if theme in n.english_meaning.lower()]
            tamil_matches = [n.tamil_script for n in tamil_names if theme in n.english_meaning.lower()]
            
            if sanskrit_matches or tamil_matches:
                patterns["Common_themes"].append(f"{theme}: Sanskrit {len(sanskrit_matches)}, Tamil {len(tamil_matches)}")
        
        return patterns
    
    def _identify_phonetic_relationships(self, sanskrit_names: List[SanskritName], tamil_names: List[TamilName]) -> List[Tuple[str, str, str]]:
        """Identify phonetic relationships between Sanskrit and Tamil names (for academic analysis only)."""
        relationships = []
        
        # Known phonetic correspondences (for analysis, not name creation)
        known_pairs = [
            ("चन्द्रमुख", "சந்திரமுகன்", "Direct adaptation: Sanskrit candramukha > Tamil cantiramukaṉ"),
            ("षण्मुख", "சன்முகன்", "Phonetic adaptation: Sanskrit ṣaṇmukha > Tamil caṉmukaṉ"),
            ("चैतन्य", "சைதன்யன்", "Philosophical term: Sanskrit caitanya > Tamil caitaṉyaṉ"),
            ("समर", "சமरன्", "Conceptual: Sanskrit samara (battle) related to Tamil warrior names"),
        ]
        
        # Check for these relationships in our extracted names
        sanskrit_dict = {name.devanagari: name for name in sanskrit_names}
        tamil_dict = {name.tamil_script: name for name in tamil_names}
        
        for skt, tam, relationship in known_pairs:
            if skt in sanskrit_dict and tam in tamil_dict:
                relationships.append((skt, tam, relationship))
        
        return relationships
    
    def generate_separate_reports(self) -> Tuple[str, str]:
        """Generate separate reports for Sanskrit and Tamil names."""
        
        if not self.analysis_results:
            return "No analysis available", "No analysis available"
        
        # Sanskrit report
        sanskrit_report = self._generate_sanskrit_report()
        
        # Tamil report  
        tamil_report = self._generate_tamil_report()
        
        return sanskrit_report, tamil_report
    
    def _generate_sanskrit_report(self) -> str:
        """Generate Sanskrit names report."""
        if not self.analysis_results:
            return "No Sanskrit names found"
        
        report = "🕉️  SANSKRIT NAMES FOR LORD SUBRAMANYA SWAMY 🕉️\n"
        report += "="*60 + "\n"
        report += f"📊 Total Sanskrit Names: {self.analysis_results.sanskrit_count}\n\n"
        
        # Group by source
        sources = {}
        for name in self.analysis_results.sanskrit_names:
            if name.source_text not in sources:
                sources[name.source_text] = []
            sources[name.source_text].append(name)
        
        for source, names in sources.items():
            report += f"📜 {source.upper()} ({len(names)} names):\n"
            for name in names:
                report += f"   • {name.devanagari} ({name.transliteration})\n"
                report += f"     MW: {name.mw_definition}\n"
                report += f"     Meaning: {name.english_meaning}\n"
                if name.etymology:
                    report += f"     Etymology: {name.etymology}\n"
                report += f"     Context: {name.context}\n\n"
        
        return report
    
    def _generate_tamil_report(self) -> str:
        """Generate Tamil names report."""
        if not self.analysis_results:
            return "No Tamil names found"
        
        report = "🕉️  TAMIL NAMES FOR LORD SUBRAMANYA SWAMY 🕉️\n"
        report += "="*60 + "\n"
        report += f"📊 Total Tamil Names: {self.analysis_results.tamil_count}\n\n"
        
        # Group by source
        sources = {}
        for name in self.analysis_results.tamil_names:
            if name.source_text not in sources:
                sources[name.source_text] = []
            sources[name.source_text].append(name)
        
        for source, names in sources.items():
            report += f"📿 {source.upper()} ({len(names)} names):\n"
            for name in names:
                report += f"   • {name.tamil_script} ({name.transliteration})\n"
                report += f"     Lexicon: {name.lexicon_definition}\n"
                report += f"     Meaning: {name.english_meaning}\n"
                report += f"     Context: {name.context}\n"
                if name.devotional_significance:
                    report += f"     Devotional: {name.devotional_significance}\n"
                report += "\n"
        
        return report
    
    def generate_cross_reference_analysis(self) -> str:
        """Generate cross-reference analysis without mixing languages."""
        if not self.analysis_results:
            return "No analysis available"
        
        report = "🔍  SANSKRIT-TAMIL CROSS-REFERENCE ANALYSIS 🔍\n"
        report += "="*60 + "\n"
        report += "Note: This analysis identifies relationships while keeping languages separate.\n\n"
        
        # Source distribution
        report += "📚 SOURCE DISTRIBUTION:\n"
        for source, count in self.analysis_results.source_distribution.items():
            report += f"   {source}: {count} names\n"
        
        # Etymology patterns
        report += "\n🔬 ETYMOLOGY PATTERNS:\n"
        for pattern_type, patterns in self.analysis_results.etymology_patterns.items():
            if patterns:
                report += f"\n   {pattern_type.replace('_', ' ').title()}:\n"
                for pattern in patterns[:5]:  # Show top 5
                    report += f"     • {pattern}\n"
        
        # Phonetic relationships
        if self.analysis_results.phonetic_relationships:
            report += "\n🔗 IDENTIFIED RELATIONSHIPS (Academic Analysis):\n"
            for skt, tam, relationship in self.analysis_results.phonetic_relationships:
                report += f"   Sanskrit: {skt} ↔ Tamil: {tam}\n"
                report += f"   Relationship: {relationship}\n\n"
        
        # Summary statistics
        report += "\n📈 SUMMARY STATISTICS:\n"
        report += f"   Total Verified Names: {self.analysis_results.total_names}\n"
        report += f"   Sanskrit Names: {self.analysis_results.sanskrit_count}\n"
        report += f"   Tamil Names: {self.analysis_results.tamil_count}\n"
        report += f"   Identified Relationships: {len(self.analysis_results.phonetic_relationships)}\n"
        
        return report
    
    def export_separate_databases(self, format_type: str = 'json') -> Tuple[str, str]:
        """Export separate databases for Sanskrit and Tamil names."""
        if not self.analysis_results:
            return "", ""
        
        # Export Sanskrit database
        sanskrit_data = []
        for name in self.analysis_results.sanskrit_names:
            sanskrit_data.append({
                'devanagari': name.devanagari,
                'transliteration': name.transliteration,
                'source': name.source_text,
                'reference': name.reference,
                'mw_definition': name.mw_definition,
                'english_meaning': name.english_meaning,
                'context': name.context,
                'etymology': name.etymology,
                'language': 'Sanskrit'
            })
        
        # Export Tamil database
        tamil_data = []
        for name in self.analysis_results.tamil_names:
            tamil_data.append({
                'tamil_script': name.tamil_script,
                'transliteration': name.transliteration,
                'source': name.source_text,
                'reference': name.reference,
                'lexicon_definition': name.lexicon_definition,
                'english_meaning': name.english_meaning,
                'context': name.context,
                'devotional_significance': name.devotional_significance,
                'language': 'Tamil'
            })
        
        if format_type == 'json':
            sanskrit_export = json.dumps(sanskrit_data, indent=2, ensure_ascii=False)
            tamil_export = json.dumps(tamil_data, indent=2, ensure_ascii=False)
        else:
            # CSV format
            sanskrit_export = "Devanagari,Transliteration,Source,Reference,MW_Definition,English_Meaning,Context,Etymology\n"
            for item in sanskrit_data:
                sanskrit_export += f'"{item["devanagari"]}","{item["transliteration"]}","{item["source"]}","{item["reference"]}","{item["mw_definition"]}","{item["english_meaning"]}","{item["context"]}","{item["etymology"]}"\n'
            
            tamil_export = "Tamil_Script,Transliteration,Source,Reference,Lexicon_Definition,English_Meaning,Context,Devotional_Significance\n"
            for item in tamil_data:
                tamil_export += f'"{item["tamil_script"]}","{item["transliteration"]}","{item["source"]}","{item["reference"]}","{item["lexicon_definition"]}","{item["english_meaning"]}","{item["context"]}","{item["devotional_significance"]}"\n'
        
        return sanskrit_export, tamil_export

def create_sample_corpus():
    """Create sample corpus for testing."""
    
    # Sanskrit texts (Devanagari)
    sanskrit_texts = {
        'skanda_puranam': """
स्कन्दस्य नाम महतः समरप्रिय तस्य।
सुब्रह्मण्यो मुनिगणैः स्तूयते सर्वदा च।
षण्मुखो देवसेनायाः पतिर्योऽसौ सनातनः।
चन्द्रमुखो ललितकोऽद्भुतरूप धारी।
सेनानी देवगणानां चतुर्भुजो महाबलः।
        """,
        'sahasranama': """
ॐ समराय नमः। चन्द्रकेतवे नमः।
सेनापतये नमः। चैतन्याय नमः।
चक्रधराय नमः। चन्द्रशेखराय नमः।
        """
    }
    
    # Tamil texts
    tamil_texts = {
        'thiruppugazh': """
சரணம் சரணம் என்று சொல்லி வருவார்
சன்முகன் பாதம் பணிந்து நிற்பார்
சந்திரமுகன் அருளால் பெற்ற
சக்திவேல் ஏந்திய கண்டன் தன்னை
சரவணன் என்று சொல்லி வணங்கி
        """,
        'kandhar_anubuthi': """
சைதன்யன் தன்னை அறிந்து கொள்வாய்
சகலாகமன் தன்னை துதிப்பாய்
சஞ்சலன் தன்னை வணங்கி நிற்பாய்
        """,
        'temple_hymns': """
சாமி நீ எங்கள் தலைவன்
சார்வன் நீ எங்கள் காவலன்
சத்குரு நீ எங்கள் வழிகாட்டி
சாந்தன் நீ எங்கள் சாந்தி
        """
    }
    
    return sanskrit_texts, tamil_texts

def main():
    """Main corpus analysis process."""
    print("🕉️  SANSKRIT-TAMIL CORPUS ANALYZER FOR LORD SUBRAMANYA SWAMY 🕉️")
    print("="*80)
    print("Systematic extraction and analysis keeping Sanskrit and Tamil names separate")
    print("="*80)
    
    # Initialize analyzer
    analyzer = SanskritTamilCorpusAnalyzer()
    
    # Create sample corpus
    sanskrit_texts, tamil_texts = create_sample_corpus()
    
    # Process corpus
    analysis = analyzer.process_corpus(sanskrit_texts, tamil_texts)
    
    # Generate separate reports
    sanskrit_report, tamil_report = analyzer.generate_separate_reports()
    
    print("\n" + sanskrit_report)
    print("\n" + tamil_report)
    
    # Cross-reference analysis
    cross_ref = analyzer.generate_cross_reference_analysis()
    print("\n" + cross_ref)
    
    # Export separate databases
    sanskrit_json, tamil_json = analyzer.export_separate_databases('json')
    
    # Save outputs
    with open('sanskrit_names_verified.json', 'w', encoding='utf-8') as f:
        f.write(sanskrit_json)
    
    with open('tamil_names_verified.json', 'w', encoding='utf-8') as f:
        f.write(tamil_json)
    
    print("\n📝 OUTPUTS SAVED:")
    print("   • sanskrit_names_verified.json")
    print("   • tamil_names_verified.json")
    
    print("\n🙏 Analysis complete. Sanskrit and Tamil names maintained separately.")
    print("   All names verified against authoritative sources (MW Dictionary for Sanskrit, Tamil Lexicon for Tamil).")

if __name__ == "__main__":
    main()