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

# 1. Main Page se saare links nikalna
main_url = "https://animesalt.in/" 
response = requests.get(main_url, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(response.text, 'html.parser')

# Saare episode link dhundo (is site ke structure ke hisaab se)
links = set()
for a in soup.find_all('a', href=True):
    if '/episode/' in a['href']:
        full_link = "https://animesalt.in" + a['href'] if a['href'].startswith('/') else a['href']
        links.add(full_link)

# 2. Existing links check karo
existing_links = sheet.col_values(3)

# 3. Naye links ko scrape karke sheet mein daalo
for url in list(links)[:10]: # Sirf top 10 naye links uthayega
    if url in existing_links:
        continue
        
    try:
        page_res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        page_soup = BeautifulSoup(page_res.text, 'html.parser')
        
        title = page_soup.find("meta", property="og:title")["content"]
        
        # Iframe ka source nikalna
        iframe = page_soup.find("iframe")
        video_link = iframe['src'] if iframe else "N/A"
        
        sheet.append_row(["ID_AUTO", title, video_link, "FALSE"])
        print(f"Added New Episode: {title}")
    except Exception as e:
        print(f"Error: {e}")
