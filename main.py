import os
import json
import time
import schedule
import gspread
import traceback
from scraper import get_embed_link

def get_gspread_client():
    try:
        # Railway ke Variables se credentials uthana
        creds_json_string = os.getenv("GCP_CREDENTIALS")
        
        if not creds_json_string:
            print("❌ Error: GCP_CREDENTIALS variable missing in Railway!")
            return None
            
        creds_dict = json.loads(creds_json_string)
        
        # Modern stable method for Google Sheets connection
        client = gspread.service_account_from_dict(creds_dict)
        return client
    except Exception as e:
        print(f"❌ Google Sheet connect karne me error aaya: {e}")
        traceback.print_exc()
        return None

def update_logic():
    print("[*] Scraper check start ho gaya...")
    
    client = get_gspread_client()
    if not client:
        print("❌ Google Sheet client nahi mila, process abort!")
        return
        
    try:
        # Sheet ka naam verify kar le, database ka exact wahi hona chahiye
        sheet = client.open("AniStream_Database").sheet1
        
        # Column A (1) mein links hain
        urls_to_check = sheet.col_values(1)[1:] 
        
        for index, url in enumerate(urls_to_check, start=2):
            if not url or "animesalt" not in url:
                continue
                
            print(f"Checking link: {url}")
            new_embed = get_embed_link(url)
            
            if new_embed and new_embed != "No embed link found":
                old_embed = sheet.cell(index, 2).value
                
                if new_embed != old_embed:
                    print(f"✅ Updating Row {index}: {new_embed}")
                    sheet.update_cell(index, 2, new_embed)
                else:
                    print(f"ℹ️ Row {index}: No change.")
            else:
                print(f"❌ Row {index}: Scrape failed.")
            
            # API Rate limiting se bachne ke liye gap
            time.sleep(3)
                
    except Exception as e:
        print(f"❌ Automation loop mein error aaya: {e}")
        traceback.print_exc()
        
    print("[*] Check complete. Bot agle round ke liye wait kar raha hai.")

# Scheduler
schedule.every(1).hours.do(update_logic)

if __name__ == "__main__":
    print("🚀 AniStream-Bot start ho gaya!")
    update_logic() # Pehli baar execute
    
    while True:
        schedule.run_pending()
        time.sleep(60)
