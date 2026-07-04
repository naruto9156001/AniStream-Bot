import os, json, gspread, requests
from bs4 import BeautifulSoup

# Setup
creds = service_account.Credentials.from_service_account_info(json.loads(os.environ['GCP_CREDENTIALS']), scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"])
sheet = client.open("AniStream_Database").sheet1

def get_all_anime_links():
    # Yahan wo link daal jahan saari list hai
    url = "https://animesalt.in/anime-list" 
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    # Ye CSS selector tere site ke structure ke hisaab se hoga
    return [a['href'] for a in soup.select('div.anime-list-item a')]

def run_full_scan():
    existing_data = sheet.get_all_values()
    anime_links = get_all_anime_links()
    
    for link in anime_links:
        # Link se name nikalna
        name = link.split('/')[-1].replace('-dub', '').upper()
        
        # Loop for episodes
        for ep in range(1, 1000): # Hard limit
            ep_url = f"{link}-1x{ep}"
            
            # Check if in sheet
            if any(row[0] == name and row[2] == str(ep) for row in existing_data):
                continue
            
            # Fast Check
            if requests.head(ep_url).status_code == 200:
                # Scrape details
                soup = BeautifulSoup(requests.get(ep_url).text, 'html.parser')
                video = soup.find("iframe")['src'] if soup.find("iframe") else "N/A"
                thumb = soup.find("meta", property="og:image")['content']
                
                sheet.append_row([name, 1, ep, f"{name} Ep {ep}", thumb, ep_url, video, "FALSE"])
                print(f"✅ Added: {name} Ep {ep}")
            else:
                break # Episode khatam
