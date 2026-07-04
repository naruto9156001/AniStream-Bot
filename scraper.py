import os, json, gspread, requests
from google.oauth2 import service_account  # Ye line zaroori hai!
from bs4 import BeautifulSoup

# Setup Credentials
creds_dict = json.loads(os.environ['GCP_CREDENTIALS'])
creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"])
client = gspread.authorize(creds)
sheet = client.open("AniStream_Database").sheet1

TMDB_KEY = os.environ.get('TMDB_KEY') # .get() use karna safe hai

def update_sheet():
    print("Scraping started...")
    # Baaki ka logic yahan...
    # (Jo maine pehle diya tha wo yahan paste kar)

if __name__ == "__main__":
    update_sheet()
