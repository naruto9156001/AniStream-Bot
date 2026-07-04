import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
from bs4 import BeautifulSoup

# Secret se credentials load karo
creds_dict = json.loads(os.environ['GCP_CREDENTIALS'])
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open("AniStream_Database").sheet1

# Scrape logic
url = "https://animesalt.in/episode/fullmetal-alchemist-brotherhood-1x2"
response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(response.text, 'html.parser')

title = soup.find("meta", property="og:title")["content"]
video_link = soup.find("iframe")['src']

# Sheet mein daalo
sheet.append_row(["ID_AUTO", title, video_link, "FALSE"])
print(f"Success: {title} added!")
