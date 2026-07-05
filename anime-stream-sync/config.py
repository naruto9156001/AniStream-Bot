import os
import json
from dotenv import load_dotenv

load_dotenv()

CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', 3600))
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

TMDB_API_KEY = os.getenv('TMDB_KEY')
GCP_CREDENTIALS = os.getenv('GCP_CREDENTIALS')   # JSON string

GOOGLE_SHEET_ID = os.getenv('GOOGLE_SHEET_ID')
ANIME_SHEET = "Anime Database"
EPISODES_SHEET = "Episodes"

TARGET_SITES = ["Animesalt.in"]   # ← Change this

CACHE_FILE = "cache/watched.json"
