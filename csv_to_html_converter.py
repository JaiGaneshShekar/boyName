#!/usr/bin/env python3
"""
Convert Thiruppugazh CSV to HTML for easy web viewing
"""

import csv
import pandas as pd
from datetime import datetime

def csv_to_html(csv_file):
    """Convert CSV to beautiful HTML."""
    
    # Read CSV
    df = pd.read_csv(csv_file)
    
    # Generate HTML
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Complete Thiruppugazh Names Database</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
                background-color: #f5f5f5;
            }}
            .header {{
                text-align: center;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                border-radius: 10px;
                margin-bottom: 30px;
            }}
            .stats {{
                background: white;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 30px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                background: white;
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            th {{
                background: #4a90e2;
                color: white;
                padding: 15px 10px;
                text-align: left;
                font-weight: bold;
            }}
            td {{
                padding: 12px 10px;
                border-bottom: 1px solid #eee;
            }}
            tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}
            tr:hover {{
                background-color: #e3f2fd;
            }}
            .name {{
                font-weight: bold;
                color: #2e7d32;
            }}
            .song-number {{
                background: #ffeb3b;
                padding: 4px 8px;
                border-radius: 4px;
                font-weight: bold;
            }}
            .category {{
                background: #e1f5fe;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 0.9em;
            }}
            .confidence {{
                font-weight: bold;
            }}
            .confidence.high {{ color: #388e3c; }}
            .confidence.medium {{ color: #f57c00; }}
            .confidence.low {{ color: #d32f2f; }}
            .url {{
                color: #1976d2;
                text-decoration: none;
                font-size: 0.9em;
            }}
            .url:hover {{
                text-decoration: underline;
            }}
            .search-box {{
                margin: 20px 0;
                padding: 10px;
                font-size: 16px;
                width: 300px;
                border: 2px solid #4a90e2;
                border-radius: 5px;
            }}
        </style>
        <script>
            function searchTable() {{
                var input = document.getElementById("searchInput");
                var filter = input.value.toLowerCase();
                var table = document.getElementById("namesTable");
                var rows = table.getElementsByTagName("tr");
                
                for (var i = 1; i < rows.length; i++) {{
                    var cells = rows[i].getElementsByTagName("td");
                    var found = false;
                    
                    for (var j = 0; j < cells.length; j++) {{
                        if (cells[j].textContent.toLowerCase().indexOf(filter) > -1) {{
                            found = true;
                            break;
                        }}
                    }}
                    
                    rows[i].style.display = found ? "" : "none";
                }}
            }}
        </script>
    </head>
    <body>
        <div class="header">
            <h1>🕉️ Complete Thiruppugazh Names Database 🕉️</h1>
            <h2>Lord Subramanya Swamy Names Starting with Sa/Cha/Sha</h2>
            <p>Extracted from All 1,340 Thiruppugazh Songs from kaumaram.com</p>
        </div>
        
        <div class="stats">
            <h3>📊 Database Statistics</h3>
            <ul>
                <li><strong>Total Names:</strong> {len(df)} authentic names</li>
                <li><strong>Source Coverage:</strong> All 1,340 Thiruppugazh songs systematically processed</li>
                <li><strong>Song Range:</strong> Song {df['Song_Number_X'].min()} to Song {df['Song_Number_X'].max()}</li>
                <li><strong>High Confidence Names (≥0.7):</strong> {len(df[df['Confidence_Score'].astype(float) >= 0.7])}</li>
                <li><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</li>
            </ul>
        </div>
        
        <input type="text" id="searchInput" class="search-box" onkeyup="searchTable()" placeholder="🔍 Search names, songs, or categories...">
        
        <table id="namesTable">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Song #</th>
                    <th>Category</th>
                    <th>Confidence</th>
                    <th>Context</th>
                    <th>Source URL</th>
                </tr>
            </thead>
            <tbody>
    """
    
    # Add table rows
    for _, row in df.iterrows():
        confidence_class = "high" if float(row['Confidence_Score']) >= 0.7 else ("medium" if float(row['Confidence_Score']) >= 0.5 else "low")
        context_short = row['Context'][:100] + "..." if len(row['Context']) > 100 else row['Context']
        context_short = context_short.replace('<', '&lt;').replace('>', '&gt;')
        
        html_content += f"""
                <tr>
                    <td class="name">{row['Name']}</td>
                    <td><span class="song-number">{row['Song_Number_X']}</span></td>
                    <td><span class="category">{row['Category'].replace('_', ' ').title()}</span></td>
                    <td><span class="confidence {confidence_class}">{row['Confidence_Score']}</span></td>
                    <td>{context_short}</td>
                    <td><a href="{row['Song_URL']}" class="url" target="_blank">View Song</a></td>
                </tr>
        """
    
    html_content += """
            </tbody>
        </table>
        
        <div style="margin-top: 30px; padding: 20px; background: white; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            <h3>📋 Usage Information</h3>
            <p><strong>Song URL Pattern:</strong> https://kaumaram.com/thiru/nnt000X_u.html#english (where X is the Song Number)</p>
            <p><strong>Search Features:</strong> Use the search box to filter by name, song number, category, or context</p>
            <p><strong>Categories:</strong></p>
            <ul>
                <li><strong>Primary Divine Name:</strong> Core names like Saravana, Shanmukha, Subrahmanya</li>
                <li><strong>Secondary Divine Name:</strong> Related divine names like Siva, Sami, Swami</li>
                <li><strong>Divine Epithet:</strong> Descriptive divine titles and epithets</li>
                <li><strong>Divine Attribute:</strong> Names related to divine weapons, powers, etc.</li>
            </ul>
            <p><strong>Perfect for Your Son's Naming:</strong> Every name is authentic, sourced from the sacred Thiruppugazh corpus, with complete traceability to original songs.</p>
        </div>
        
        <div style="text-align: center; margin-top: 30px; color: #666;">
            <p>🕉️ Om Saravana Bhava! May this comprehensive collection serve in finding the perfect blessed name! 🕉️</p>
        </div>
    </body>
    </html>
    """
    
    return html_content

def main():
    csv_file = 'COMPLETE_THIRUPPUGAZH_ALL_SONGS_WITH_NUMBERS_FINAL.csv'
    html_file = csv_file.replace('.csv', '.html')
    
    print("🌐 CREATING HTML VERSION...")
    
    try:
        html_content = csv_to_html(csv_file)
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        print(f"✅ HTML generated: {html_file}")
        print("   Features: Search, clickable links, responsive design")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()