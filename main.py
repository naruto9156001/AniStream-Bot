import os
import json
import time
import gspread
import traceback
from scraper import get_embed_link

def get_gspread_client():
    try:
        # Railway ke Variables mein 'GCP_CREDENTIALS' set hona chahiye
        creds_json_string = os.getenv("GCP_CREDENTIALS")
        if not creds_json_string:
            print("❌ Error: GCP_CREDENTIALS secret Railway mein set nahi hai!")
            return None
        creds_dict = json.loads(creds_json_string)
        return gspread.service_account_from_dict(creds_dict)
    except Exception as e:
        print(f"❌ Critical Connection Error: {e}")
        return None

def update_all_links():
    print("[*] Update cycle shuru ho raha hai...")
    client = get_gspread_client()
    if not client: 
        return
        
    try:
        # Sheet ka naam "AniStream_Database" aur tab "sheet1"
        sheet = client.open("AniStream_Database").sheet1
        
        # Column A (1) se Titles/Links utha rahe hain
        urls = sheet.col_values(1)[1:] 
        
        for index, url in enumerate(urls, start=2):
            # Agar cell khali hai ya link nahi hai toh skip karo
            if not url or "animesalt" not in url: 
                continue
                
            print(f"🔍 Checking row {index}: {url}")
            new_embed = get_embed_link(url)
            
            if new_embed and new_embed != "No embed link found":
                # Link Column C (3) mein update hoga
                old_embed = sheet.cell(index, 3).value
                
                if new_embed != old_embed:
                    print(f"✅ Row {index} update ho rahi hai -> Column C")
                    sheet.update_cell(index, 3, new_embed)
                    # Har write ke baad chhota gap taaki Google block na kare
                    time.sleep(3) 
            else:
                print(f"❌ Row {index} ke liye link nahi mila.")
            
    except Exception as e:
        print(f"❌ Loop mein error: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 AniStream-Bot Continuous Mode mein active hai!")
    while True:
        update_all_links()
        print("[*] Saare episodes check ho gaye. 5 minute ka break le raha hoon...")
        time.sleep(300) # 5 minute = 300 seconds
