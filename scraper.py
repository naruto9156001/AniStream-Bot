import os
import json
import gspread
import requests
from bs4 import BeautifulSoup
from google.oauth2 import service_account

# Setup
creds_dict = json.loads(os.environ['GCP_CREDENTIALS'])
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=scope)
client = gspread.authorize(creds)
sheet = client.open("AniStream_Database").sheet1

existing_links = sheet.col_values(3) # Duplicate check ke liye

# Pagination Setup: Page 1 se shuru karke tab tak chalega jab tak links mil rahe hain
page_num = 1
while True:
    print(f"--- Scraping Page {page_num} ---")
    url = f"https://animesalt.in/page/{page_num}" # Ye structure check kar lena
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    if response.status_code != 200:
        print("Saare pages finish ho gaye!")
        break
        
    soup = BeautifulSoup(response.text, 'html.parser')
    episodes = soup.find_all('a', href=lambda x: x and '/episode/' in x)
    
    if not episodes: # Agar page par koi link nahi mila toh ruk jao
        break

    for ep in episodes:
        link = ep['href']
        if not link.startswith('http'):
            link = "https://animesalt.in" + link
            
        if link in existing_links:
            continue
            
        try:
            # Video page par jaakar detail nikalo
            res = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})
            soup_ep = BeautifulSoup(res.text, 'html.parser')
            
            title = soup_ep.find("meta", property="og:title")["content"]
            iframe = soup_ep.find("iframe")
            video_link = iframe['src'] if iframe else "No Link"
            
            sheet.append_row(["ID_AUTO", title, video_link, "FALSE"])
            existing_links.append(link) # Memory mein add karo
            print(f"Added: {title}")
        except:
            continue
            
    page_num += 1 # Agle page par jao

print("Scanning Complete!")
