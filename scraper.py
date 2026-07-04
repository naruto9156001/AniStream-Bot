import os
import json
import gspread
import requests
from bs4 import BeautifulSoup
from google.oauth2 import service_account

# 1. Credentials load karo (GitHub Secret se)
creds_dict = json.loads(os.environ['GCP_CREDENTIALS'])
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# 2. Sahi tarike se authenticate karo
creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=scope)
client = gspread.authorize(creds)

# 3. Google Sheet access karo
sheet = client.open("AniStream_Database").sheet1

# 4. Scraper Logic
url = "https://animesalt.in/episode/fullmetal-alchemist-brotherhood-1x2"
response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(response.text, 'html.parser')

# Title aur Video Link nikalna
title_meta = soup.find("meta", property="og:title")
title = title_meta["content"] if title_meta else "No Title Found"

video_iframe = soup.find("iframe")
video_link = video_iframe['src'] if video_iframe else "No Link Found"

# 5. Sheet mein entry daalo
sheet.append_row(["ID_AUTO", title, video_link, "FALSE"])
print(f"Success: {title} successfully added to Sheet!")
