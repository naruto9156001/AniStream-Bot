import os
import json
import time
import schedule
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from scraper import get_embed_link

def get_gspread_client():
    try:
        # Secrets se GCP credentials ka string uthana
        creds_json_string = os.getenv("GCP_CREDENTIALS")
        
        if not creds_json_string:
            raise ValueError("Bhai, GCP_CREDENTIALS secret mila hi nahi!")
            
        # String ko wapas JSON dictionary mein badalna
        creds_dict = json.loads(creds_json_string)
        
        # Google Sheets aur Drive ki permission set karna
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        print(f"❌ Google Sheet connect karne me error aaya: {e}")
        return None

def update_logic():
    print("[*] Scraper check start ho gaya...")
    
    client = get_gspread_client()
    if not client:
        print("❌ Google Sheet client nahi mila, process abort!")
        return
        
    try:
        # Apni Google Sheet ka naam yahan likh (e.g., 'Anime List')
        sheet = client.open("AniStream_Database").sheet1
        
        # Maan lete hain Column A (1) mein tere Anime Salt ke links hain
        # Aur Column B (2) mein embed links hain
        urls_to_check = sheet.col_values(1)[1:] # [1:] se header row skip ho jayegi
        
        for index, url in enumerate(urls_to_check, start=2): # Row 2 se start hoga
            if not url or "animesalt" not in url:
                continue
                
            print(f"Checking link: {url}")
            new_embed = get_embed_link(url)
            
            if new_embed and new_embed != "No embed link found":
                # Purana embed link jo sheet me hai use check karo
                old_embed = sheet.cell(index, 2).value
                
                if new_embed != old_embed:
                    print(f"✅ Link badal gaya! Old: {old_embed} -> New: {new_embed}")
                    sheet.update_cell(index, 2, new_embed) # Column B update ho jayega
                else:
                    print("ℹ️ Link bilkul sahi hai, badalne ki zaroorat nahi.")
            else:
                print("❌ Website se link nahi nikal paya.")
                
    except Exception as e:
        print(f"❌ Automation loop me error: {e}")
        
    print("[*] Check complete. Ab bot agle round tak aaram karega.")

# Har 1 ghante mein check karega
schedule.every(1).hours.do(update_logic)

if __name__ == "__main__":
    print("🚀 Bot successfully start ho gaya hai!")
    
    # Pehli baar turant chalega
    update_logic()
    
    while True:
        schedule.run_pending()
        time.sleep(60)
