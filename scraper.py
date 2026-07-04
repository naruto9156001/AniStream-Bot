import os
import json
import requests
import gspread
from google.oauth2 import service_account

# Scopes Define Karo
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# Credentials Setup
gcp_creds_json = os.getenv('GCP_CREDENTIALS')
with open('credentials.json', 'w') as f:
    f.write(gcp_creds_json)

# UPDATED: Browser Header ke saath API fetch function
def get_anime_data():
    api_url = "http://senpaianimes.rf.gd/api/anime-world-india/v1/home.php"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(api_url, headers=headers, timeout=15) 
        print(f"Status Code: {response.status_code}") # Ye check karo
        print(f"Response Body: {response.text[:200]}") # Response kya aa raha hai
        
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error: {e}")
    return None

# Google Sheet update function
def update_google_sheet():
    creds = service_account.Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
    client = gspread.authorize(creds)
    
    sheet = client.open("AniStream_Database").sheet1 
    anime_list = get_anime_data()
    
    if anime_list:
        sheet.clear()
        sheet.append_row(["Title", "Image", "Link"])
        
        for anime in anime_list:
            title = anime.get('title', 'N/A')
            image = anime.get('image', 'N/A')
            link = anime.get('link', 'N/A')
            sheet.append_row([title, image, link])
            
        print("Sheet successfully updated!")
    else:
        print("API se data nahi mila ya error aaya!")

if __name__ == "__main__":
    update_google_sheet()
