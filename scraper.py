import os
import json
import requests
import gspread
from google.oauth2 import service_account

# Scopes डिफाइन करें
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# Google Cloud secret से temp file बनाएँ
gcp_creds_json = os.getenv('GCP_CREDENTIALS')
with open('credentials.json', 'w') as f:
    f.write(gcp_creds_json)

# यहाँ scopes=SCOPES जोड़ना न भूलें!
creds = service_account.Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
client = gspread.authorize(creds)

def update_google_sheet():
    # ... बाकी का कोड ...

# Secrets ko environment variable se uthao
gcp_creds_json = os.getenv('GCP_CREDENTIALS')

# Secret ko temporary file mein likho
with open('credentials.json', 'w') as f:
    f.write(gcp_creds_json)

# 1. API se data fetch karne ka logic
def get_anime_data():
    api_url = "http://senpaianimes.rf.gd/api/anime-world-india/v1/home.php"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error fetching API: {e}")
    return None

# 2. Google Sheet mein update karne ka logic
def update_google_sheet():
    # Credentials setup
    creds = service_account.Credentials.from_service_account_file('credentials.json')
    client = gspread.authorize(creds)
    
    # Sheet ka naam
    sheet = client.open("AniStream_Database").sheet1 
    
    # API se data lao
    anime_list = get_anime_data()
    
    if anime_list:
        sheet.clear()
        sheet.append_row(["Title", "Image", "Link"])
        
        for anime in anime_list:
            # Dhyan rakhna ki JSON keys yahi hon (agar API mein 'name' hai toh 'name' likhna)
            title = anime.get('title', 'N/A')
            image = anime.get('image', 'N/A')
            link = anime.get('link', 'N/A')
            sheet.append_row([title, image, link])
            
        print("Sheet successfully updated!")
    else:
        print("API se data nahi mila ya error aaya!")

# Run the function
if __name__ == "__main__":
    update_google_sheet()
