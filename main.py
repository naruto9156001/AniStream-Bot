import os
import json
import time
import gspread
import traceback
from scraper import get_embed_link

def get_gspread_client():
    try:
        creds_json_string = os.getenv("GCP_CREDENTIALS")
        if not creds_json_string:
            return None
        creds_dict = json.loads(creds_json_string)
        client = gspread.service_account_from_dict(creds_dict)
        return client
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def update_all_links():
    print("[*] Continuous update cycle start...")
    client = get_gspread_client()
    if not client:
        return
        
    try:
        sheet = client.open("AniStream_Database").sheet1
        urls = sheet.col_values(1)[1:]
        
        for index, url in enumerate(urls, start=2):
            if not url or "animesalt" not in url:
                continue
                
            new_embed = get_embed_link(url)
            if new_embed and new_embed != "No embed link found":
                old_embed = sheet.cell(index, 2).value
                if new_embed != old_embed:
                    print(f"✅ Updating Row {index}")
                    sheet.update_cell(index, 2, new_embed)
                    time.sleep(3) # Google API limit ke liye
            
    except Exception as e:
        print(f"❌ Error in loop: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 Bot Continuous Mode mein start ho gaya!")
    while True:
        update_all_links()
        print("[*] Cycle complete. 5 minute rest...")
        time.sleep(300) # 300 seconds = 5 minute ka gap
