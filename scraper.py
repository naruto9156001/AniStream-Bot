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

# 1. Jin websites ko scrap karna hai (List bana lo)
urls = [
    "https://animesalt.in/episode/fullmetal-alchemist-brotherhood-1x2",
    "https://animesalt.in/episode/fullmetal-alchemist-brotherhood-1x3"
]

# 2. Existing links check karo taaki duplicate na ho
existing_links = sheet.col_values(3) # Column 3 mein links hain

for url in urls:
    if url in existing_links:
        print(f"Skipping: {url} (Already in sheet)")
        continue
        
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title = soup.find("meta", property="og:title")["content"]
        video_link = url # Yahan logic update kar sakte ho agar iframe alag ho
        
        sheet.append_row(["ID_AUTO", title, video_link, "FALSE"])
        print(f"Added: {title}")
    except Exception as e:
        print(f"Error scraping {url}: {e}")
