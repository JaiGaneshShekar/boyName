#!/usr/bin/env python3
"""
Convert Skanda Purana CSV to HTML format
Create beautiful HTML pages for Skanda Purana names
"""

import pandas as pd
import csv
from datetime import datetime

def create_skanda_html():
    """Create HTML version of Skanda Purana names."""
    
    print("🌐 CONVERTING SKANDA PURANA CSV TO HTML")
    print("="*50)
    
    try:
        # Use the final clean authentic Sanskrit baby names CSV
        df = pd.read_csv('FINAL_CLEAN_AUTHENTIC_SANSKRIT_BABY_NAMES.csv')
        print(f"✅ Loaded Skanda Purana names: {len(df)} authentic names")
    except FileNotFoundError:
        print("❌ Authentic Sanskrit baby names CSV not found!")
        return
    
    # Generate HTML content
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Complete Skanda Purana Names Database - Authentic Sanskrit Names</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #ff9a56 0%, #ff6b6b 100%);
            min-height: 100vh;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        .header {{
            text-align: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 20px;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        .header h2 {{
            margin: 10px 0;
            font-size: 1.3em;
            opacity: 0.9;
        }}
        .stats {{
            background: #f8f9fa;
            padding: 25px;
            border-bottom: 3px solid #dee2e6;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 15px;
        }}
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-left: 4px solid #ff6b6b;
        }}
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: #ff6b6b;
        }}
        .search-container {{
            padding: 20px;
            background: white;
            border-bottom: 2px solid #e9ecef;
        }}
        .search-box {{
            width: 100%;
            max-width: 400px;
            padding: 15px 20px;
            font-size: 16px;
            border: 2px solid #ff6b6b;
            border-radius: 25px;
            outline: none;
            transition: all 0.3s ease;
        }}
        .search-box:focus {{
            border-color: #ff4757;
            box-shadow: 0 0 0 3px rgba(255,107,107,0.25);
        }}
        .table-container {{
            padding: 0;
            overflow-x: auto;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
        }}
        th {{
            background: linear-gradient(135deg, #ff6b6b 0%, #ff4757 100%);
            color: white;
            padding: 18px 15px;
            text-align: left;
            font-weight: 600;
            font-size: 1.1em;
            position: sticky;
            top: 0;
            z-index: 10;
            cursor: pointer;
        }}
        td {{
            padding: 15px;
            border-bottom: 1px solid #dee2e6;
            vertical-align: top;
        }}
        tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        tr:hover {{
            background-color: #ffe8e8;
            transform: scale(1.01);
            transition: all 0.2s ease;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .name {{
            font-weight: bold;
            font-size: 1.2em;
            color: #ff4757;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        }}
        .frequency {{
            background: linear-gradient(135deg, #ffc107 0%, #fd7e14 100%);
            color: white;
            padding: 8px 12px;
            border-radius: 20px;
            font-weight: bold;
            display: inline-block;
            min-width: 40px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }}
        .pattern {{
            background: linear-gradient(135deg, #6f42c1 0%, #6610f2 100%);
            color: white;
            padding: 6px 12px;
            border-radius: 15px;
            font-size: 0.9em;
            font-weight: 500;
            display: inline-block;
            white-space: nowrap;
        }}
        .meaning {{
            font-style: italic;
            color: #495057;
            line-height: 1.4;
            background: #fff3cd;
            padding: 8px 12px;
            border-radius: 8px;
            border-left: 4px solid #ffc107;
        }}
        .confidence {{
            font-weight: bold;
            padding: 6px 10px;
            border-radius: 20px;
            color: white;
            display: inline-block;
            min-width: 50px;
            text-align: center;
        }}
        .confidence.high {{ 
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            box-shadow: 0 2px 4px rgba(40,167,69,0.3);
        }}
        .confidence.medium {{ 
            background: linear-gradient(135deg, #fd7e14 0%, #ffc107 100%);
            box-shadow: 0 2px 4px rgba(253,126,20,0.3);
        }}
        .confidence.low {{ 
            background: linear-gradient(135deg, #dc3545 0%, #e83e8c 100%);
            box-shadow: 0 2px 4px rgba(220,53,69,0.3);
        }}
        .quality-score {{
            background: linear-gradient(135deg, #17a2b8 0%, #138496 100%);
            color: white;
            padding: 6px 10px;
            border-radius: 15px;
            font-weight: bold;
            display: inline-block;
            min-width: 60px;
            text-align: center;
        }}
        .footer {{
            background: #343a40;
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .footer h3 {{
            color: #ff6b6b;
            margin-bottom: 20px;
        }}
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        .info-card {{
            background: #495057;
            padding: 20px;
            border-radius: 10px;
            border-top: 3px solid #ff6b6b;
        }}
        @media (max-width: 768px) {{
            .header h1 {{ font-size: 2em; }}
            .header h2 {{ font-size: 1.1em; }}
            th, td {{ padding: 10px 8px; }}
            .search-box {{ font-size: 14px; }}
        }}
        .loading {{
            text-align: center;
            padding: 40px;
            font-size: 1.2em;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🕉️ Complete Skanda Purana Names Database 🕉️</h1>
            <h2>Authentic Sanskrit Names Starting with Sa/Cha/Sha/Se/Che/Chi</h2>
            <p>Extracted from All 20 Volumes of Sacred Skanda Purana</p>
        </div>
        
        <div class="stats">
            <h3>📊 Database Statistics</h3>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">{len(df)}</div>
                    <div>Authentic Names</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">20</div>
                    <div>Volumes Processed</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{len(df[df['Confidence'] >= 0.8])}</div>
                    <div>High Confidence</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{df['Starting_Pattern'].nunique()}</div>
                    <div>Pattern Types</div>
                </div>
            </div>
        </div>
        
        <div class="search-container">
            <input type="text" id="searchInput" class="search-box" onkeyup="searchTable()" 
                   placeholder="🔍 Search authentic Sanskrit names, meanings, patterns...">
            <p id="resultsCount" style="margin-top: 10px; color: #6c757d;">Showing all {len(df)} authentic names</p>
        </div>
        
        <div class="table-container">
            <table id="namesTable">
                <thead>
                    <tr>
                        <th onclick="sortTable(0)">Name ↕️</th>
                        <th onclick="sortTable(1)">Pattern ↕️</th>
                        <th onclick="sortTable(2)">Frequency ↕️</th>
                        <th onclick="sortTable(3)">Confidence ↕️</th>
                        <th onclick="sortTable(4)">Quality Score ↕️</th>
                        <th onclick="sortTable(5)">Sanskrit Meaning ↕️</th>
                        <th onclick="sortTable(6)">Type ↕️</th>
                        <th>Source</th>
                    </tr>
                </thead>
                <tbody>"""
    
    # Add table rows
    for _, row in df.iterrows():
        confidence = float(row['Confidence'])
        confidence_class = "high" if confidence >= 0.8 else ("medium" if confidence >= 0.6 else "low")
        
        # Clean and truncate meaning
        meaning = str(row['Sanskrit_Meaning']) if pd.notna(row['Sanskrit_Meaning']) else 'Authentic Sanskrit name from Skanda Purana'
        if len(meaning) > 80:
            meaning = meaning[:77] + "..."
        
        # Clean source context
        source_context = str(row['Source_Context']) if pd.notna(row['Source_Context']) else 'Sacred Skanda Purana'
        if len(source_context) > 50:
            source_context = source_context[:47] + "..."
        
        name_type = str(row['Name_Type']).replace('_', ' ').title()
        
        html_content += f"""
                    <tr>
                        <td><span class="name">{row['Name']}</span></td>
                        <td><span class="pattern">{row['Starting_Pattern']}</span></td>
                        <td><span class="frequency">{row['Frequency']}</span></td>
                        <td><span class="confidence {confidence_class}">{row['Confidence']:.1f}</span></td>
                        <td><span class="quality-score">{row['Quality_Score']:.0f}</span></td>
                        <td><div class="meaning">{meaning.replace('<', '&lt;').replace('>', '&gt;')}</div></td>
                        <td>{name_type}</td>
                        <td>{row['Part_Found']}, {row['Page_Found']}</td>
                    </tr>"""
    
    html_content += f"""
                </tbody>
            </table>
        </div>
        
        <div class="footer">
            <h3>📋 Skanda Purana Information</h3>
            
            <div class="info-grid">
                <div class="info-card">
                    <h4>📚 Source Texts</h4>
                    <p><strong>Complete Coverage:</strong><br>
                    All 20 volumes of Skanda Purana<br>
                    Systematic extraction from every page<br>
                    ({len(df)} authentic names total)</p>
                </div>
                
                <div class="info-card">
                    <h4>🔤 Pattern Types</h4>
                    <p><strong>Starting Patterns:</strong><br>
                    Sa, Cha, Sha, Se, Che, Chi<br>
                    Sanskrit and IAST transliterations<br>
                    Complete pattern coverage</p>
                </div>
                
                <div class="info-card">
                    <h4>🎯 Features</h4>
                    <p><strong>Search:</strong> Filter by any column<br>
                    <strong>Sort:</strong> Click column headers<br>
                    <strong>Quality Score:</strong> Frequency × Confidence<br>
                    <strong>Authentic:</strong> Direct from sacred texts</p>
                </div>
                
                <div class="info-card">
                    <h4>🙏 For Your Son</h4>
                    <p>Every name is <strong>authentic</strong> from sacred Skanda Purana<br>
                    Complete <strong>traceability</strong> to original sources<br>
                    Perfect for traditional Sanskrit naming with<br>
                    <strong>zero compromise</strong> on authenticity</p>
                </div>
            </div>
            
            <div style="margin-top: 30px; padding-top: 20px; border-top: 2px solid #495057;">
                <p style="font-size: 1.2em;">🕉️ <strong>Om Namah Shivaya!</strong> 🕉️</p>
                <p>May this comprehensive collection from sacred Skanda Purana serve in finding the perfect blessed name for your son!</p>
                <p style="font-size: 0.9em; opacity: 0.8;">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
        </div>
    </div>

    <script>
        let allData = [];
        
        // Initialize with static data
        document.addEventListener('DOMContentLoaded', function() {{
            console.log('Skanda Purana names loaded: {len(df)} authentic names');
            document.getElementById('resultsCount').textContent = 'Showing all {len(df)} authentic names';
        }});
        
        function searchTable() {{
            const input = document.getElementById("searchInput");
            const filter = input.value.toLowerCase();
            const table = document.getElementById("namesTable");
            const rows = table.getElementsByTagName("tr");
            let visibleCount = 0;
            
            for (let i = 1; i < rows.length; i++) {{
                const cells = rows[i].getElementsByTagName("td");
                let found = false;
                
                for (let j = 0; j < cells.length; j++) {{
                    if (cells[j].textContent.toLowerCase().indexOf(filter) > -1) {{
                        found = true;
                        break;
                    }}
                }}
                
                if (found) {{
                    rows[i].style.display = "";
                    visibleCount++;
                }} else {{
                    rows[i].style.display = "none";
                }}
            }}
            
            document.getElementById("resultsCount").textContent = 
                filter ? `Showing ${{visibleCount}} of {len(df)} names` : `Showing all {len(df)} names`;
        }}
        
        function sortTable(column) {{
            const table = document.getElementById("namesTable");
            let switching = true;
            let dir = "asc";
            let switchcount = 0;
            
            while (switching) {{
                switching = false;
                const rows = table.rows;
                
                for (let i = 1; i < (rows.length - 1); i++) {{
                    let shouldSwitch = false;
                    const x = rows[i].getElementsByTagName("TD")[column];
                    const y = rows[i + 1].getElementsByTagName("TD")[column];
                    
                    let xValue = x.innerHTML.toLowerCase();
                    let yValue = y.innerHTML.toLowerCase();
                    
                    // Handle numeric columns
                    if (column === 2 || column === 3 || column === 4) {{ // Frequency, Confidence, Quality Score
                        xValue = parseFloat(x.textContent) || 0;
                        yValue = parseFloat(y.textContent) || 0;
                    }}
                    
                    if (dir === "asc") {{
                        if (xValue > yValue) {{
                            shouldSwitch = true;
                            break;
                        }}
                    }} else if (dir === "desc") {{
                        if (xValue < yValue) {{
                            shouldSwitch = true;
                            break;
                        }}
                    }}
                }}
                
                if (shouldSwitch) {{
                    rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
                    switching = true;
                    switchcount++;
                }} else {{
                    if (switchcount === 0 && dir === "asc") {{
                        dir = "desc";
                        switching = true;
                    }}
                }}
            }}
        }}
    </script>
</body>
</html>"""
    
    # Save HTML file
    with open('COMPLETE_SKANDA_PURANA_NAMES.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Created Skanda Purana HTML: COMPLETE_SKANDA_PURANA_NAMES.html")
    print(f"📊 Contains {len(df)} authentic Sanskrit names with full functionality")
    
    return html_content

if __name__ == "__main__":
    create_skanda_html()
    print("\n🎉 SKANDA PURANA HTML CONVERSION COMPLETE!")
    print("📄 File: COMPLETE_SKANDA_PURANA_NAMES.html")
    print("🎯 Ready for your son's authentic Sanskrit naming!")