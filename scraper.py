import os, json, gspread, requests
from bs4 import BeautifulSoup

# Google Sheet Setup
creds = service_account.Credentials.from_service_account_info(json.loads(os.environ['GCP_CREDENTIALS']))
client = gspread.authorize(creds)
sheet = client.open("AniStream_Database").sheet1

def start_scraping():
    # 1. Latest Anime Section se links uthao
    url = "https://animesalt.in/" 
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    
    # Ye selector har 'Latest Episode' card ko pakad lega
    anime_cards = soup.select('.latest-episode-card a') 
    
    for card in anime_cards:
        link = card['href']
        # Extract title aur episode logic
        # Agar link mein 'dub' hai toh flag True karo
        is_hindi = "dub" in link
        
        # Metadata nikalna
        name = link.split('/')[-1].split('-')[0].upper()
        
        # Database mein check karo
        if any(row[5] == link for row in sheet.get_all_values()):
            continue
            
        # Naya episode add karo
        sheet.append_row([name, 1, "NEW", "Hindi" if is_hindi else "Sub", link, "PENDING"])
        print(f"🚀 New Content Detected: {name}")

start_scraping()
