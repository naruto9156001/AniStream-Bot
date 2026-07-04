import os, json, gspread, requests, time
from bs4 import BeautifulSoup
from google.oauth2 import service_account

# Setup
creds_dict = json.loads(os.environ['GCP_CREDENTIALS'])
creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"])
client = gspread.authorize(creds)
sheet = client.open("AniStream_Database").sheet1

TMDB_KEY = os.environ['TMDB_KEY'] 
BASE_TMDB_URL = "https://api.themoviedb.org/3"

# TMDB Thumbnail Fetcher
def get_tmdb_thumb(anime_name, season, ep):
    try:
        search_url = f"{BASE_TMDB_URL}/search/tv?api_key={TMDB_KEY}&query={anime_name}"
        res = requests.get(search_url).json()
        if not res['results']: return "N/A"
        anime_id = res['results'][0]['id']
        ep_url = f"{BASE_TMDB_URL}/tv/{anime_id}/season/{season}/episode/{ep}?api_key={TMDB_KEY}"
        ep_res = requests.get(ep_url).json()
        return f"https://image.tmdb.org/t/p/w500{ep_res['still_path']}" if 'still_path' in ep_res else "N/A"
    except: return "N/A"

# --- NEW PATTERN LOGIC ---
anime_slug = "bleach-dub" # Yahan anime ka naam change kar sakte ho
season = 1
for ep_num in range(1, 14): # 1 se 13 tak
    url = f"https://animesalt.in/episode/{anime_slug}-{season}x{ep_num}"
    print(f"📡 Trying: {url}")
    
    try:
        res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            video = soup.find("iframe")['src'] if soup.find("iframe") else "N/A"
            title = f"Bleach Ep {ep_num}"
            thumb = get_tmdb_thumb("Bleach", season, ep_num)
            
            sheet.append_row(["Bleach", season, ep_num, title, thumb, url, video, "FALSE"])
            print(f"✅ Found: Episode {ep_num}")
        else:
            print(f"❌ Not Found: {ep_num}")
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(2) # Site ko spam mat karna, warna block kar degi
