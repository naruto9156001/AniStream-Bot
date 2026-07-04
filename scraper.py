import os, json, gspread, requests, time
from bs4 import BeautifulSoup
from google.oauth2 import service_account

# Setup
creds_dict = json.loads(os.environ['GCP_CREDENTIALS'])
creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"])
client = gspread.authorize(creds)
sheet = client.open("AniStream_Database").sheet1

# TMDB Config
TMDB_KEY = "9912d7e50dc9a4589075d72b3aa3c6e6" # Yahan apni API Key daal
BASE_TMDB_URL = "https://api.themoviedb.org/3"

def get_tmdb_data(anime_name, season, ep):
    # Search for the anime to get its ID
    search_url = f"{BASE_TMDB_URL}/search/tv?api_key={TMDB_KEY}&query={anime_name}"
    res = requests.get(search_url).json()
    if not res['results']: return None
    
    anime_id = res['results'][0]['id']
    # Get episode image
    ep_url = f"{BASE_TMDB_URL}/tv/{anime_id}/season/{season}/episode/{ep}?api_key={TMDB_KEY}"
    ep_res = requests.get(ep_url).json()
    
    if 'still_path' in ep_res and ep_res['still_path']:
        return f"https://image.tmdb.org/t/p/w500{ep_res['still_path']}"
    return None

# Scraper Loop mein ye integrate kar le:
# thumbnail = get_tmdb_data("Jujutsu Kaisen", "1", i)
