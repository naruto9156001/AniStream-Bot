import os, json, gspread, requests, time
from bs4 import BeautifulSoup
from google.oauth2 import service_account

# Setup
creds_dict = json.loads(os.environ['GCP_CREDENTIALS'])
creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"])
client = gspread.authorize(creds)
sheet = client.open("AniStream_Database").sheet1

# TMDB Config (GitHub Secrets se key uthao)
TMDB_KEY = os.environ['TMDB_KEY'] 
BASE_TMDB_URL = "https://api.themoviedb.org/3"

def get_tmdb_thumb(anime_name, season, ep):
    try:
        # 1. Get Anime ID
        search_url = f"{BASE_TMDB_URL}/search/tv?api_key={TMDB_KEY}&query={anime_name}"
        res = requests.get(search_url).json()
        if not res['results']: return "N/A"
        anime_id = res['results'][0]['id']
        
        # 2. Get Episode Image
        ep_url = f"{BASE_TMDB_URL}/tv/{anime_id}/season/{season}/episode/{ep}?api_key={TMDB_KEY}"
        ep_res = requests.get(ep_url).json()
        if 'still_path' in ep_res and ep_res['still_path']:
            return f"https://image.tmdb.org/t/p/w500{ep_res['still_path']}"
    except: return "N/A"
    return "N/A"

# Scraper Loop
index_url = "https://animesalt.in/az-list/"
soup = BeautifulSoup(requests.get(index_url, headers={'User-Agent': 'Mozilla/5.0'}).text, 'html.parser')

for anime_a in soup.select('a[href*="/anime/"]'):
    anime_url = anime_a['href']
    anime_name = anime_a.text.strip()
    
    ep_soup = BeautifulSoup(requests.get(anime_url, headers={'User-Agent': 'Mozilla/5.0'}).text, 'html.parser')
    for ep in ep_soup.select('a[href*="/episode/"]'):
        ep_url = ep['href']
        
        # Scrape detail
        data = BeautifulSoup(requests.get(ep_url, headers={'User-Agent': 'Mozilla/5.0'}).text, 'html.parser')
        title = data.find("meta", property="og:title")["content"]
        video = data.find("iframe")['src'] if data.find("iframe") else "N/A"
        thumb = get_tmdb_thumb(anime_name, 1, 1) # Yahan season/ep logic update kar lena
        
        sheet.append_row([anime_name, "01", title, thumb, ep_url, video, "FALSE"])
        time.sleep(1)
        print(f"Added: {title}")
