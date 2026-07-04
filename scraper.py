import os
import json
import gspread
import requests
from bs4 import BeautifulSoup
from google.oauth2 import service_account

# 1. Setup - GitHub Secrets se credentials uthana
creds_dict = json.loads(os.environ['GCP_CREDENTIALS'])
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=scope)
client = gspread.authorize(creds)
sheet = client.open("AniStream_Database").sheet1

# 2. Anime list jise scrap karna hai
# Tu yahan aur bhi anime add kar sakta hai
anime_list = [
    {"base_url": "https://animesalt.in/episode/jujutsu-kaisen-1x", "max_eps": 24},
    {"base_url": "https://animesalt.in/episode/fullmetal-alchemist-brotherhood-1x", "max_eps": 64}
]

existing_links = sheet.col_values(3) # Duplicate check ke liye 3rd column check hoga

# 3. Scraping Loop
for anime in anime_list:
    base_url = anime["base_url"]
    max_eps = anime["max_eps"]
    
    print(f"--- Scraping Anime: {base_url.split('/')[-1]} ---")
    
    for i in range(1, max_eps + 1):
        url = f"{base_url}{i}"
        
        if url in existing_links:
            continue
        
        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Title aur Video Link
                title_meta = soup.find("meta", property="og:title")
                title = title_meta["content"] if title_meta else "Title Not Found"
                
                iframe = soup.find("iframe")
                video_link = iframe['src'] if iframe else "No Link Found"
                
                # Sheet mein data daalo
                sheet.append_row(["ID_AUTO", title, video_link, "FALSE"])
                existing_links.append(url) # Local list update karo
                print(f"Added: {title}")
        except Exception as e:
            print(f"Error on {url}: {e}")

print("Scraping Process Completed Successfully!")
