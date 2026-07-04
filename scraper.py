import os
import json
import cloudscraper
import gspread
from google.oauth2 import service_account

# 1. Scopes Define Karo
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# 2. Credentials Setup (Secrets se file banana)
gcp_creds_json = os.getenv('GCP_CREDENTIALS')
with open('credentials.json', 'w') as f:
    f.write(gcp_creds_json)

# 3. API se data fetch karne ka function (Cloudscraper ke saath)
def get_anime_data():
    api_url = "http://senpaianimes.rf.gd/api/anime-world-india/v1/home.php"
    
    # Cloudscraper ka use karke bypass karna
    scraper = cloudscraper.create_scraper()
    
    try:
        # Browser emulation ke saath request
        response = scraper.get(api_url, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                # Series aur Movies ko combine karke return karo
                return data.get('latest_series', []) + data.get('latest_movies', [])
            else:
                print("API Success False:", data)
        else:
            print(f"Server Status Code: {response.status_code}")
            
    except Exception as e:
        print(f"Error fetching API: {e}")
    return None

# 4. Google Sheet update function
def update_google_sheet():
    # Sahi credentials loading with SCOPES
    creds = service_account.Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
    client = gspread.authorize(creds)
    
    # Sheet open karo
    sheet = client.open("AniStream_Database").sheet1 
    anime_list = get_anime_data()
    
    if anime_list:
        sheet.clear()
        sheet.append_row(["Title", "Image", "Link"])
        
        for anime in anime_list:
            title = anime.get('title', 'N/A')
            image = anime.get('image', 'N/A')
            # PHP code ke hisaab se agar 'link' key nahi hai, toh ye safe rahega
            link = anime.get('link', 'N/A') 
            sheet.append_row([title, image, link])
            
        print("Sheet successfully updated!")
    else:
        print("API se data nahi mila ya error aaya!")

if __name__ == "__main__":
    update_google_sheet()
