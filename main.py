import time
import schedule
from scraper import get_embed_link
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials

def update_logic():
    print("[*] Scraper check start ho gaya...")
    
    # ---------------------------------------------------------
    # GOOGLE SHEET LOGIC YAHAN AAYEGA
    # Niche ek example structure diya hai ki kaise kaam karega:
    # ---------------------------------------------------------
    
    # 1. Sheet se URLs fetch karna
    # urls_to_check = sheet.col_values(1) # Maan le Column 1 mein links hain
    
    # 2. Dummy list for now
    urls_to_check = [
        "https://animesalt.in/episode/bleach-dub-1x20"
    ]
    
    for url in urls_to_check:
        print(f"Checking link: {url}")
        new_embed = get_embed_link(url)
        
        if new_embed and new_embed != "No embed link found":
            print(f"✅ Naya Link Mila: {new_embed}")
            # Yahan Google Sheet ko update karne ka code dalega
            # sheet.update_cell(row, col, new_embed)
        else:
            print("❌ Koi naya link nahi mila.")
            
    print("[*] Check complete. Ab bot 1 ghante tak aaram karega.")

# Railway par continuously run karne ke liye Scheduler
# Har 1 ghante mein ye update_logic() function ko trigger karega
schedule.every(1).hours.do(update_logic)

if __name__ == "__main__":
    print("🚀 Railway server start ho gaya hai!")
    
    # Server start hote hi pehli baar turant run karega
    update_logic()
    
    # Railway ke container ko alive rakhne ke liye infinite loop
    while True:
        schedule.run_pending()
        time.sleep(60) # Har minute check karega ki task ka time aaya ya nahi
