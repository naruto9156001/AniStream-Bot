import os, json, gspread, requests
from bs4 import BeautifulSoup

# Setup
creds = service_account.Credentials.from_service_account_info(json.loads(os.environ['GCP_CREDENTIALS']))
client = gspread.authorize(creds)
sheet = client.open("AniStream_Database").sheet1

def update_sheet():
    base_url = "https://animesalt.in"
    # Homepage scan (yahan saare latest updates hote hain)
    soup = BeautifulSoup(requests.get(f"{base_url}/").text, 'html.parser')
    
    # Ye selector animesalt ke episode links ko pakad lega
    links = [a['href'] for a in soup.select('a[href*="/episode/"]')]
    
    existing_links = sheet.col_values(6) # URL column check karna
    
    for link in links:
        if link not in existing_links:
            # Full URL banao
            full_url = base_url + link if not link.startswith('http') else link
            
            # Metadata extract karo
            # Format: anime-dub-1x1
            parts = link.split('/')[-1].split('-')
            name = parts[0].upper()
            ep = parts[-1].split('x')[-1]
            lang = "Hindi" if "dub" in link else "English"
            
            # Sheet mein add karo
            sheet.append_row([name, 1, ep, f"{name} Ep {ep}", "N/A", full_url, lang])
            print(f"✅ Added to Sheet: {name} - Ep {ep}")

update_sheet()
