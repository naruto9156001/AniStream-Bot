import requests
import gspread
from google.oauth2 import service_account

# 1. API se data fetch karne ka logic
def get_anime_data():
    api_url = "http://senpaianimes.rf.gd/api/anime-world-india/v1/home.php"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    return None

# 2. Google Sheet mein update karne ka logic
def update_google_sheet():
    # Credentials setup (Apni JSON file ka path yahan daal)
    creds = service_account.Credentials.from_service_account_file('credentials.json')
    client = gspread.authorize(creds)
    
    # Sheet ka naam ya ID
    sheet = client.open("AniStream_Database").sheet1 
    
    # API se data lao
    anime_list = get_anime_data()
    
    if anime_list:
        # Sheet saaf karo aur naya data dalo
        sheet.clear()
        # Header add karo
        sheet.append_row(["Title", "Image", "Link"])
        
        # Data insert karo
        for anime in anime_list:
            title = anime.get('title', 'N/A')
            image = anime.get('image', 'N/A')
            link = anime.get('link', 'N/A')
            sheet.append_row([title, image, link])
            
        print("Sheet successfully updated!")
    else:
        print("API se data nahi mila!")

# Run the function
update_google_sheet()
