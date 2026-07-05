import gspread
import json
import logging
from google.oauth2.service_account import Credentials

from config import GOOGLE_SHEET_ID, ANIME_SHEET, EPISODES_SHEET, GCP_CREDENTIALS

logger = logging.getLogger(__name__)

def get_client():
    try:
        if GCP_CREDENTIALS:
            creds_info = json.loads(GCP_CREDENTIALS)
            scopes = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive',
                'https://www.googleapis.com/auth/spreadsheets'
            ]
            creds = Credentials.from_service_account_info(creds_info, scopes=scopes)
        else:
            creds = Credentials.from_service_account_file('credentials.json', scopes=scopes)
        
        return gspread.authorize(creds)
    except Exception as e:
        logger.error(f"Auth Error: {e}")
        raise

def update_google_sheet(data):
    if not data:
        return
    
    try:
        client = get_client()
        sheet = client.open_by_key(GOOGLE_SHEET_ID)
        
        anime_ws = sheet.worksheet(ANIME_SHEET)
        episodes_ws = sheet.worksheet(EPISODES_SHEET)

        for entry in data:
            a = entry['anime']
            
            # Clean Anime Row
            anime_row = [
                a.get('id', ''), 
                a.get('name', ''), 
                a.get('poster', ''), 
                '',                    # Synopsis (baad mein TMDB se)
                '',                    # IMDb
                '',                    # Genres
                'Ongoing',
                '',                    # Year
                len(entry.get('episodes', [])), 
                'animesalt.ac'
            ]
            anime_ws.append_row(anime_row)

            # Episodes
            for ep in entry.get('episodes', []):
                episodes_ws.append_row([
                    a.get('id', ''),
                    ep.get('number', 1),
                    ep.get('title', ''),
                    ep.get('thumbnail', ''),
                    json.dumps(ep.get('streams', {})),
                    "720p",
                    True,   # Hindi Dub
                    False,  # Japanese
                    False   # English
                ])

        logger.info(f"✅ Sheet updated successfully - {len(data)} anime")
    except Exception as e:
        logger.error(f"Sheet update failed: {e}")
