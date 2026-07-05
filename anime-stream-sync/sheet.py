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
        
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        logger.error(f"Credentials Error: {e}")
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
            # Anime row
            anime_ws.append_row([
                a.get('id'), 
                a.get('name'), 
                a.get('poster'), 
                '',  # synopsis
                '',  # imdb
                '',  # genres
                'Ongoing',
                '',  # year
                1,   # episodes count
                'Auto'
            ])

            for ep in entry['episodes']:
                episodes_ws.append_row([
                    a.get('id'), 
                    ep.get('number'), 
                    ep.get('title'),
                    ep.get('thumbnail'), 
                    json.dumps(ep.get('streams', {})), 
                    "720", 
                    ep.get('hindi_dub', True)
                ])
        
        logger.info(f"✅ Successfully updated {len(data)} anime in sheet")
    except Exception as e:
        logger.error(f"Sheet error: {e}")
