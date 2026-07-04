import requests
import gspread
from google.oauth2 import service_account

# Tera API URL
API_URL = "http://senpaianimes.rf.gd/api/anime-world-india/v1/home.php"

# API se data fetch karne ka logic
def get_anime_data():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json() # Direct JSON mil gaya!
    return None

# Yahan se aage gspread ka code jo sheet mein data daalega
# ...
