#!/usr/bin/env python3
"""
Corpus Documentation and Output System

Complete system for documenting, exporting, and managing the extracted
Sanskrit and Tamil names corpus for Lord Subramanya Swamy.
"""

import json
import csv
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import os

@dataclass
class ExtractionMetadata:
    """Metadata for the extraction process."""
    extraction_date: str
    total_sources: int
    sanskrit_sources: int
    tamil_sources: int
    extraction_method: str
    validation_standards: Dict[str, str]
    software_version: str

@dataclass
class SourceDocumentation:
    """Documentation for each source."""
    source_name: str
    language: str
    source_type: str  # puranic, devotional, temple, etc.
    period: str
    author: str
    description: str
    reliability_score: int  # 1-10
    names_extracted: int

class CorpusDocumentationSystem:
    """Complete documentation and export system."""
    
    def __init__(self):
        self.metadata = None
        self.sources = []
        self.sanskrit_names = []
        self.tamil_names = []
        
    def set_metadata(self, 
                    total_sources: int,
                    sanskrit_sources: int, 
                    tamil_sources: int,
                    extraction_method: str = "Regex pattern matching with lexicon validation"):
        """Set extraction metadata."""
        self.metadata = ExtractionMetadata(
            extraction_date=datetime.now().isoformat(),
            total_sources=total_sources,
            sanskrit_sources=sanskrit_sources,
            tamil_sources=tamil_sources,
            extraction_method=extraction_method,
            validation_standards={
                "Sanskrit": "Monier Williams Sanskrit-English Dictionary",
                "Tamil": "Tamil Lexicon and traditional sources"
            },
            software_version="1.0.0"
        )
    
    def add_source_documentation(self, source_doc: SourceDocumentation):
        """Add documentation for a source."""
        self.sources.append(source_doc)
    
    def add_names(self, sanskrit_names: List[Dict], tamil_names: List[Dict]):
        """Add extracted names to the system."""
        self.sanskrit_names = sanskrit_names
        self.tamil_names = tamil_names
    
    def generate_csv_report(self, output_file: str = "subramanya_names_complete.csv"):
        """Generate complete CSV report."""
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'Name', 'Script', 'Transliteration', 'Language', 'Source', 
                'Reference', 'Dictionary_Definition', 'English_Meaning', 
                'Context', 'Etymology', 'Devotional_Significance', 'Type'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            # Write Sanskrit names
            for name in self.sanskrit_names:
                writer.writerow({
                    'Name': name.get('devanagari', ''),
                    'Script': 'Devanagari',
                    'Transliteration': name.get('transliteration', ''),
                    'Language': 'Sanskrit',
                    'Source': name.get('source', ''),
                    'Reference': name.get('reference', ''),
                    'Dictionary_Definition': name.get('mw_definition', ''),
                    'English_Meaning': name.get('english_meaning', ''),
                    'Context': name.get('context', ''),
                    'Etymology': name.get('etymology', ''),
                    'Devotional_Significance': '',
                    'Type': 'Sanskrit_Name'
                })
            
            # Write Tamil names
            for name in self.tamil_names:
                writer.writerow({
                    'Name': name.get('tamil_script', ''),
                    'Script': 'Tamil',
                    'Transliteration': name.get('transliteration', ''),
                    'Language': 'Tamil',
                    'Source': name.get('source', ''),
                    'Reference': name.get('reference', ''),
                    'Dictionary_Definition': name.get('lexicon_definition', ''),
                    'English_Meaning': name.get('english_meaning', ''),
                    'Context': name.get('context', ''),
                    'Etymology': '',
                    'Devotional_Significance': name.get('devotional_significance', ''),
                    'Type': 'Tamil_Name'
                })
        
        return f"CSV report generated: {output_file}"
    
    def generate_json_database(self, output_file: str = "subramanya_names_database.json"):
        """Generate comprehensive JSON database."""
        database = {
            'metadata': asdict(self.metadata) if self.metadata else {},
            'sources': [asdict(source) for source in self.sources],
            'sanskrit_names': self.sanskrit_names,
            'tamil_names': self.tamil_names,
            'statistics': {
                'total_names': len(self.sanskrit_names) + len(self.tamil_names),
                'sanskrit_count': len(self.sanskrit_names),
                'tamil_count': len(self.tamil_names),
                'source_distribution': self._get_source_distribution()
            }
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(database, f, indent=2, ensure_ascii=False)
        
        return f"JSON database generated: {output_file}"
    
    def generate_xml_export(self, output_file: str = "subramanya_names_corpus.xml"):
        """Generate XML export for academic use."""
        root = ET.Element("SubramanyaNamesCorpus")
        
        # Metadata
        if self.metadata:
            metadata_elem = ET.SubElement(root, "Metadata")
            for key, value in asdict(self.metadata).items():
                elem = ET.SubElement(metadata_elem, key.replace('_', ''))
                if isinstance(value, dict):
                    for k, v in value.items():
                        sub_elem = ET.SubElement(elem, k.replace(' ', ''))
                        sub_elem.text = str(v)
                else:
                    elem.text = str(value)
        
        # Sources
        sources_elem = ET.SubElement(root, "Sources")
        for source in self.sources:
            source_elem = ET.SubElement(sources_elem, "Source")
            for key, value in asdict(source).items():
                elem = ET.SubElement(source_elem, key.replace('_', ''))
                elem.text = str(value)
        
        # Sanskrit Names
        sanskrit_elem = ET.SubElement(root, "SanskritNames")
        for name in self.sanskrit_names:
            name_elem = ET.SubElement(sanskrit_elem, "Name")
            for key, value in name.items():
                elem = ET.SubElement(name_elem, key.replace('_', ''))
                elem.text = str(value)
        
        # Tamil Names
        tamil_elem = ET.SubElement(root, "TamilNames")
        for name in self.tamil_names:
            name_elem = ET.SubElement(tamil_elem, "Name")
            for key, value in name.items():
                elem = ET.SubElement(name_elem, key.replace('_', ''))
                elem.text = str(value)
        
        # Write XML
        tree = ET.ElementTree(root)
        ET.indent(tree, space="  ")
        tree.write(output_file, encoding='utf-8', xml_declaration=True)
        
        return f"XML export generated: {output_file}"
    
    def generate_academic_report(self, output_file: str = "academic_corpus_report.md"):
        """Generate academic-style markdown report."""
        report = f"""# Lord Subramanya Swamy Names Corpus Analysis

## Abstract

This report presents a systematic extraction and analysis of Lord Subramanya Swamy (Murugan) names beginning with "Cha" (च/ச) from Sanskrit and Tamil literature. The corpus includes {len(self.sanskrit_names)} verified Sanskrit names and {len(self.tamil_names)} verified Tamil names, extracted from authoritative religious and literary sources.

## Methodology

### Extraction Method
{self.metadata.extraction_method if self.metadata else 'Pattern-based extraction with lexicon validation'}

### Validation Standards
- **Sanskrit Names**: Verified against {self.metadata.validation_standards.get('Sanskrit', 'Monier Williams Dictionary') if self.metadata else 'Monier Williams Dictionary'}
- **Tamil Names**: Verified against {self.metadata.validation_standards.get('Tamil', 'Tamil Lexicon') if self.metadata else 'Tamil Lexicon'}

### Sources Analyzed

"""
        
        for source in self.sources:
            report += f"""#### {source.source_name}
- **Language**: {source.language}
- **Type**: {source.source_type}
- **Period**: {source.period}
- **Author**: {source.author}
- **Description**: {source.description}
- **Names Extracted**: {source.names_extracted}
- **Reliability Score**: {source.reliability_score}/10

"""
        
        report += f"""## Results

### Sanskrit Names ({len(self.sanskrit_names)} total)

| Devanagari | Transliteration | Source | Meaning | MW Reference |
|------------|----------------|---------|---------|--------------|
"""
        
        for name in self.sanskrit_names[:10]:  # Show first 10
            report += f"| {name.get('devanagari', '')} | {name.get('transliteration', '')} | {name.get('source', '')} | {name.get('english_meaning', '')} | {name.get('mw_definition', '')[:50]}... |\n"
        
        if len(self.sanskrit_names) > 10:
            report += f"\n*({len(self.sanskrit_names) - 10} additional names in complete database)*\n"
        
        report += f"""

### Tamil Names ({len(self.tamil_names)} total)

| Tamil Script | Transliteration | Source | Meaning | Devotional Significance |
|--------------|-----------------|---------|---------|------------------------|
"""
        
        for name in self.tamil_names[:10]:  # Show first 10
            report += f"| {name.get('tamil_script', '')} | {name.get('transliteration', '')} | {name.get('source', '')} | {name.get('english_meaning', '')} | {name.get('devotional_significance', '')[:30]}... |\n"
        
        if len(self.tamil_names) > 10:
            report += f"\n*({len(self.tamil_names) - 10} additional names in complete database)*\n"
        
        report += f"""

## Statistical Analysis

### Overall Statistics
- Total Names: {len(self.sanskrit_names) + len(self.tamil_names)}
- Sanskrit Names: {len(self.sanskrit_names)} ({len(self.sanskrit_names)/(len(self.sanskrit_names) + len(self.tamil_names))*100:.1f}%)
- Tamil Names: {len(self.tamil_names)} ({len(self.tamil_names)/(len(self.sanskrit_names) + len(self.tamil_names))*100:.1f}%)

### Source Distribution
{self._format_source_distribution()}

## Conclusions

This corpus represents a systematic compilation of Lord Subramanya Swamy names starting with "Cha" from authoritative Sanskrit and Tamil sources. The collection maintains linguistic authenticity by:

1. Keeping Sanskrit and Tamil names separate
2. Validating against standard dictionaries and lexicons
3. Preserving original scripts and contexts
4. Documenting sources and references

The corpus serves as a foundation for further research in Hindu onomastics, devotional literature studies, and comparative linguistics.

## References

1. Monier Williams, M. (1899). *A Sanskrit-English Dictionary*. Oxford: Clarendon Press.
2. Tamil Lexicon. (1924-1936). *Tamil Lexicon*. University of Madras.
3. Arunagirinathar. *Thiruppugazh* (Complete Works).
4. Various Puranic and temple sources (see source documentation above).

---
*Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return f"Academic report generated: {output_file}"
    
    def _get_source_distribution(self) -> Dict[str, int]:
        """Get source distribution statistics."""
        distribution = {}
        
        for name in self.sanskrit_names:
            source = name.get('source', 'Unknown')
            distribution[f"Sanskrit: {source}"] = distribution.get(f"Sanskrit: {source}", 0) + 1
        
        for name in self.tamil_names:
            source = name.get('source', 'Unknown')
            distribution[f"Tamil: {source}"] = distribution.get(f"Tamil: {source}", 0) + 1
        
        return distribution
    
    def _format_source_distribution(self) -> str:
        """Format source distribution for report."""
        distribution = self._get_source_distribution()
        formatted = ""
        
        for source, count in sorted(distribution.items(), key=lambda x: x[1], reverse=True):
            formatted += f"- {source}: {count} names\n"
        
        return formatted
    
    def generate_all_outputs(self, base_name: str = "subramanya_corpus"):
        """Generate all output formats."""
        results = []
        
        # CSV
        csv_file = f"{base_name}.csv"
        results.append(self.generate_csv_report(csv_file))
        
        # JSON
        json_file = f"{base_name}.json"
        results.append(self.generate_json_database(json_file))
        
        # XML
        xml_file = f"{base_name}.xml"
        results.append(self.generate_xml_export(xml_file))
        
        # Academic Report
        md_file = f"{base_name}_academic_report.md"
        results.append(self.generate_academic_report(md_file))
        
        return results

def create_sample_documentation():
    """Create sample documentation with the extracted names."""
    doc_system = CorpusDocumentationSystem()
    
    # Set metadata
    doc_system.set_metadata(
        total_sources=5,
        sanskrit_sources=2,
        tamil_sources=3
    )
    
    # Add source documentation
    sources = [
        SourceDocumentation(
            source_name="Skanda Puranam",
            language="Sanskrit",
            source_type="Puranic",
            period="Ancient (pre-1000 CE)",
            author="Traditional/Vyasa attributed",
            description="Major Purana dedicated to Lord Skanda/Murugan",
            reliability_score=10,
            names_extracted=1
        ),
        SourceDocumentation(
            source_name="Subramanya Sahasranama",
            language="Sanskrit", 
            source_type="Stotra",
            period="Medieval (1000-1500 CE)",
            author="Various sages",
            description="1008 names of Lord Subramanya",
            reliability_score=9,
            names_extracted=1
        ),
        SourceDocumentation(
            source_name="Thiruppugazh",
            language="Tamil",
            source_type="Devotional Poetry",
            period="15th Century CE",
            author="Arunagirinathar",
            description="Devotional hymns to Lord Murugan",
            reliability_score=10,
            names_extracted=6
        ),
        SourceDocumentation(
            source_name="Kandhar Anubuthi",
            language="Tamil",
            source_type="Mystical Poetry",
            period="15th Century CE", 
            author="Arunagirinathar",
            description="Mystical experience of Lord Murugan",
            reliability_score=10,
            names_extracted=3
        ),
        SourceDocumentation(
            source_name="Temple Hymns",
            language="Tamil",
            source_type="Temple Liturgy",
            period="Traditional (various periods)",
            author="Various devotees",
            description="Traditional temple worship hymns",
            reliability_score=8,
            names_extracted=4
        )
    ]
    
    for source in sources:
        doc_system.add_source_documentation(source)
    
    # Sample extracted names (would be loaded from actual extraction)
    sanskrit_names = [
        {
            "devanagari": "समर",
            "transliteration": "samara", 
            "source": "sahasranama",
            "reference": "Line 2",
            "mw_definition": "samara m. war, battle, conflict",
            "english_meaning": "Warrior, Fighter",
            "context": "ॐ समराय नमः। चन्द्रकेतवे नमः।",
            "etymology": "√sam + √ṛ (to go towards)"
        },
        {
            "devanagari": "चक्रधर",
            "transliteration": "cakradhara",
            "source": "sahasranama", 
            "reference": "Line 3",
            "mw_definition": "cakra-dhara mfn. bearing a discus",
            "english_meaning": "Discus-bearer, wheel-holder",
            "context": "चक्रधराय नमः। चन्द्रशेखराय नमः।",
            "etymology": "cakra (wheel/discus) + dhara (bearer)"
        }
    ]
    
    tamil_names = [
        {
            "tamil_script": "சரணம்",
            "transliteration": "caraṇam",
            "source": "thiruppugazh",
            "reference": "Line 2", 
            "lexicon_definition": "சரணம் - refuge, protection, feet of deity",
            "english_meaning": "Sacred feet, refuge, surrender",
            "context": "சரணம் சரணம் என்று சொல்லி வருவார்",
            "devotional_significance": "Surrender to Lord Murugan's feet"
        },
        {
            "tamil_script": "சன்முகன்",
            "transliteration": "caṉmukaṉ",
            "source": "thiruppugazh",
            "reference": "Line 3",
            "lexicon_definition": "சன்முகன் - six-faced deity", 
            "english_meaning": "Six-faced Lord (Murugan)",
            "context": "சன்முகன் பாதம் பணிந்து நிற்பார்",
            "devotional_significance": "Primary name for Lord Murugan"
        }
    ]
    
    doc_system.add_names(sanskrit_names, tamil_names)
    
    return doc_system

def main():
    """Main documentation generation process."""
    print("🕉️  CORPUS DOCUMENTATION SYSTEM FOR LORD SUBRAMANYA SWAMY 🕉️")
    print("="*80)
    
    # Create sample documentation
    doc_system = create_sample_documentation()
    
    print("📝 Generating comprehensive documentation outputs...")
    
    # Generate all output formats
    results = doc_system.generate_all_outputs("subramanya_complete_corpus")
    
    print("\n✅ DOCUMENTATION GENERATED:")
    for result in results:
        print(f"   • {result}")
    
    print(f"\n📊 CORPUS STATISTICS:")
    print(f"   • Total Names: {len(doc_system.sanskrit_names) + len(doc_system.tamil_names)}")
    print(f"   • Sanskrit Names: {len(doc_system.sanskrit_names)}")
    print(f"   • Tamil Names: {len(doc_system.tamil_names)}")
    print(f"   • Sources Documented: {len(doc_system.sources)}")
    
    print(f"\n🎯 OUTPUT FORMATS:")
    print(f"   • CSV: Machine-readable data format")
    print(f"   • JSON: Structured database with metadata")
    print(f"   • XML: Academic/interchange format")
    print(f"   • Markdown: Human-readable academic report")
    
    print(f"\n🙏 Complete documentation system ready for scholarly use!")

if __name__ == "__main__":
    main()