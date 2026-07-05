import gspread
import json
import logging
from google.oauth2.service_account import Credentials

from config import GOOGLE_SHEET_ID, ANIME_SHEET, EPISODES_SHEET, GCP_CREDENTIALS

logger = logging.getLogger(__name__)

def get_client():
    if GCP_CREDENTIALS:
        creds_info = json.loads(GCP_CREDENTIALS)
        creds = Credentials.from_service_account_info(creds_info)
    else:
        creds = Credentials.from_service_account_file('credentials.json')
    return gspread.authorize(creds)

def update_google_sheet(data):
    try:
        client = get_client()
        sheet = client.open_by_key(GOOGLE_SHEET_ID)
        
        anime_ws = sheet.worksheet(ANIME_SHEET)
        episodes_ws = sheet.worksheet(EPISODES_SHEET)

        for entry in data:
            a = entry['anime']
            anime_ws.append_row([
                a.get('id'), a.get('name'), a.get('poster'), a.get('synopsis'),
                a.get('imdb'), json.dumps(a.get('genres', [])), 'Ongoing',
                a.get('year'), len(entry['episodes']), 'Auto'
            ])

            for ep in entry['episodes']:
                episodes_ws.append_row([
                    a.get('id'), ep.get('number'), ep.get('title'),
                    ep.get('thumbnail'), json.dumps(ep.get('streams', {})),
                    str(list(ep.get('streams', {}).keys())), ep.get('hindi_dub', False)
                ])
        logger.info("✅ Sheet updated")
    except Exception as e:
        logger.error(f"Sheet error: {e}")
