#!/usr/bin/env python3
"""
Convert Thiruppugazh CSV to HTML with Meaning column instead of Context
Cleaner version for better readability
"""

import csv
import pandas as pd
from datetime import datetime

def csv_to_html_with_meaning(csv_file):
    """Convert CSV to beautiful HTML with Meaning column."""
    
    # Read CSV
    df = pd.read_csv(csv_file)
    
    # Generate HTML
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Complete Thiruppugazh Names Database - With Meanings</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
                background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
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
                border-left: 4px solid #007bff;
            }}
            .stat-number {{
                font-size: 2em;
                font-weight: bold;
                color: #007bff;
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
                border: 2px solid #007bff;
                border-radius: 25px;
                outline: none;
                transition: all 0.3s ease;
            }}
            .search-box:focus {{
                border-color: #0056b3;
                box-shadow: 0 0 0 3px rgba(0,123,255,0.25);
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
                background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
                color: white;
                padding: 18px 15px;
                text-align: left;
                font-weight: 600;
                font-size: 1.1em;
                position: sticky;
                top: 0;
                z-index: 10;
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
                background-color: #e3f2fd;
                transform: scale(1.01);
                transition: all 0.2s ease;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }}
            .name {{
                font-weight: bold;
                font-size: 1.2em;
                color: #d63384;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
            }}
            .song-number {{
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
            .category {{
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
                background: #e8f4f8;
                padding: 8px 12px;
                border-radius: 8px;
                border-left: 4px solid #17a2b8;
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
            .url {{
                color: #007bff;
                text-decoration: none;
                font-weight: 500;
                padding: 8px 15px;
                background: #e3f2fd;
                border-radius: 20px;
                display: inline-block;
                transition: all 0.3s ease;
            }}
            .url:hover {{
                background: #007bff;
                color: white;
                text-decoration: none;
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0,123,255,0.3);
            }}
            .footer {{
                background: #343a40;
                color: white;
                padding: 30px;
                text-align: center;
            }}
            .footer h3 {{
                color: #ffc107;
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
                border-top: 3px solid #ffc107;
            }}
            @media (max-width: 768px) {{
                .header h1 {{ font-size: 2em; }}
                .header h2 {{ font-size: 1.1em; }}
                th, td {{ padding: 10px 8px; }}
                .search-box {{ font-size: 14px; }}
            }}
        </style>
        <script>
            function searchTable() {{
                var input = document.getElementById("searchInput");
                var filter = input.value.toLowerCase();
                var table = document.getElementById("namesTable");
                var rows = table.getElementsByTagName("tr");
                var visibleCount = 0;
                
                for (var i = 1; i < rows.length; i++) {{
                    var cells = rows[i].getElementsByTagName("td");
                    var found = false;
                    
                    for (var j = 0; j < cells.length; j++) {{
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
                
                // Update results counter
                document.getElementById("resultsCount").textContent = 
                    filter ? `Showing ${{visibleCount}} of {len(df)} names` : `Showing all {len(df)} names`;
            }}
            
            function sortTable(column) {{
                var table = document.getElementById("namesTable");
                var switching = true;
                var dir = "asc";
                var switchcount = 0;
                
                while (switching) {{
                    switching = false;
                    var rows = table.rows;
                    
                    for (var i = 1; i < (rows.length - 1); i++) {{
                        var shouldSwitch = false;
                        var x = rows[i].getElementsByTagName("TD")[column];
                        var y = rows[i + 1].getElementsByTagName("TD")[column];
                        
                        if (dir == "asc") {{
                            if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {{
                                shouldSwitch = true;
                                break;
                            }}
                        }} else if (dir == "desc") {{
                            if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {{
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
                        if (switchcount == 0 && dir == "asc") {{
                            dir = "desc";
                            switching = true;
                        }}
                    }}
                }}
            }}
        </script>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🕉️ Complete Thiruppugazh Names Database 🕉️</h1>
                <h2>Lord Subramanya Swamy Names Starting with Sa/Cha/Sha</h2>
                <p>Extracted from All 1,340 Thiruppugazh Songs with Complete Meanings</p>
            </div>
            
            <div class="stats">
                <h3>📊 Database Statistics</h3>
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-number">{len(df)}</div>
                        <div>Authentic Names</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">1,340</div>
                        <div>Songs Processed</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{len(df[df['Confidence_Score'].astype(float) >= 0.7])}</div>
                        <div>High Confidence</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{df['Song_Number_X'].nunique()}</div>
                        <div>Songs with Names</div>
                    </div>
                </div>
            </div>
            
            <div class="search-container">
                <input type="text" id="searchInput" class="search-box" onkeyup="searchTable()" 
                       placeholder="🔍 Search names, meanings, categories, or song numbers...">
                <p id="resultsCount" style="margin-top: 10px; color: #6c757d;">Showing all {len(df)} names</p>
            </div>
            
            <div class="table-container">
                <table id="namesTable">
                    <thead>
                        <tr>
                            <th onclick="sortTable(0)" style="cursor: pointer;">Name ↕️</th>
                            <th onclick="sortTable(1)" style="cursor: pointer;">Song # ↕️</th>
                            <th onclick="sortTable(2)" style="cursor: pointer;">Category ↕️</th>
                            <th onclick="sortTable(3)" style="cursor: pointer;">Confidence ↕️</th>
                            <th onclick="sortTable(4)" style="cursor: pointer;">Meaning ↕️</th>
                            <th>Source URL</th>
                        </tr>
                    </thead>
                    <tbody>
    """
    
    # Add table rows
    for _, row in df.iterrows():
        confidence_class = "high" if float(row['Confidence_Score']) >= 0.7 else ("medium" if float(row['Confidence_Score']) >= 0.5 else "low")
        
        # Use the Meaning column from CSV, clean it up
        meaning = row['Meaning'].replace('<', '&lt;').replace('>', '&gt;')
        # Truncate very long meanings
        if len(meaning) > 150:
            meaning = meaning[:147] + "..."
        
        html_content += f"""
                <tr>
                    <td><span class="name">{row['Name']}</span></td>
                    <td><span class="song-number">{row['Song_Number_X']}</span></td>
                    <td><span class="category">{row['Category'].replace('_', ' ').title()}</span></td>
                    <td><span class="confidence {confidence_class}">{row['Confidence_Score']}</span></td>
                    <td><div class="meaning">{meaning}</div></td>
                    <td><a href="{row['Song_URL']}" class="url" target="_blank">View Song</a></td>
                </tr>
        """
    
    html_content += f"""
            </tbody>
        </table>
        </div>
        
        <div class="footer">
            <h3>📋 Usage Information</h3>
            
            <div class="info-grid">
                <div class="info-card">
                    <h4>🔗 Source Links</h4>
                    <p><strong>URL Pattern:</strong><br>
                    https://kaumaram.com/thiru/nnt000X_u.html#english<br>
                    (X = Song Number from 6 to 1340)</p>
                </div>
                
                <div class="info-card">
                    <h4>🏷️ Categories</h4>
                    <p><strong>Primary Divine:</strong> Saravana, Shanmukha, Subrahmanya<br>
                    <strong>Secondary Divine:</strong> Siva, Sami, Swami<br>
                    <strong>Divine Epithet:</strong> Descriptive titles<br>
                    <strong>Divine Attribute:</strong> Powers, weapons</p>
                </div>
                
                <div class="info-card">
                    <h4>🎯 Features</h4>
                    <p><strong>Search:</strong> Filter by any column<br>
                    <strong>Sort:</strong> Click column headers<br>
                    <strong>Meanings:</strong> Complete interpretations<br>
                    <strong>Links:</strong> Direct to original songs</p>
                </div>
                
                <div class="info-card">
                    <h4>🙏 For Your Son</h4>
                    <p>Every name is <strong>authentic</strong> from sacred Thiruppugazh<br>
                    Complete <strong>traceability</strong> to original sources<br>
                    Perfect for traditional naming with<br>
                    <strong>no compromise</strong> on authenticity</p>
                </div>
            </div>
            
            <div style="margin-top: 30px; padding-top: 20px; border-top: 2px solid #495057;">
                <p style="font-size: 1.2em;">🕉️ <strong>Om Saravana Bhava!</strong> 🕉️</p>
                <p>May this comprehensive collection serve in finding the perfect blessed name for your son!</p>
                <p style="font-size: 0.9em; opacity: 0.8;">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
        </div>
        </div>
    </body>
    </html>
    """
    
    return html_content

def main():
    csv_file = 'COMPLETE_THIRUPPUGAZH_ALL_SONGS_WITH_NUMBERS_FINAL.csv'
    html_file = 'COMPLETE_THIRUPPUGAZH_WITH_MEANINGS.html'
    
    print("🌐 CREATING ENHANCED HTML WITH MEANINGS...")
    
    try:
        html_content = csv_to_html_with_meaning(csv_file)
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        print(f"✅ Enhanced HTML generated: {html_file}")
        print("   Features:")
        print("   • Meaning column instead of Context")
        print("   • Beautiful gradient design")
        print("   • Advanced search and sort functionality")
        print("   • Responsive mobile-friendly layout")
        print("   • Statistics dashboard")
        print("   • Clickable source links to original songs")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()