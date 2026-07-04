import os, json, gspread, requests, time
from bs4 import BeautifulSoup
from google.oauth2 import service_account

# Setup
creds_dict = json.loads(os.environ['GCP_CREDENTIALS'])
creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"])
client = gspread.authorize(creds)
sheet = client.open("AniStream_Database").sheet1

TMDB_KEY = os.environ['TMDB_KEY'] 
BASE_TMDB_URL = "https://api.themoviedb.org/3"

def get_tmdb_thumb(anime_name, season, ep):
    try:
        search_url = f"{BASE_TMDB_URL}/search/tv?api_key={TMDB_KEY}&query={anime_name}"
        res = requests.get(search_url).json()
        if not res['results']: return "N/A"
        anime_id = res['results'][0]['id']
        
        ep_url = f"{BASE_TMDB_URL}/tv/{anime_id}/season/{season}/episode/{ep}?api_key={TMDB_KEY}"
        ep_res = requests.get(ep_url).json()
        if 'still_path' in ep_res and ep_res['still_path']:
            return f"https://image.tmdb.org/t/p/w500{ep_res['still_path']}"
    except: return "N/A"
    return "N/A"

# --- DEBUGGING START ---
print("🚀 Scraper Start ho raha hai...")

index_url = "https://animesalt.in/az-list/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

response = requests.get(index_url, headers=headers)
print(f"📡 Website Status Code: {response.status_code}")

if response.status_code != 200:
    print("❌ Website block kar rahi hai (Shayad Cloudflare).")
else:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Check if we are finding ANY links
    all_links = soup.find_all('a', href=True)
    print(f"🔗 Website par total links mile: {len(all_links)}")
    
    # Check specifically for anime links
    anime_links = soup.select('a[href*="/anime/"]')
    print(f"🎯 '/anime/' wale links mile: {len(anime_links)}")
    
    if len(anime_links) == 0:
        print("⚠️ DHYAN DO: /anime/ wale links zero hain! URL format kuch aur hai.")
    
    for anime_a in anime_links[:5]: # Sirf pehle 5 check karenge test ke liye
        anime_url = anime_a['href']
        if not anime_url.startswith('http'):
            anime_url = "https://animesalt.in" + anime_url
            
        anime_name = anime_a.text.strip()
        print(f"\n📺 Scanning Anime: {anime_name} ({anime_url})")
        
        try:
            ep_res = requests.get(anime_url, headers=headers)
            ep_soup = BeautifulSoup(ep_res.text, 'html.parser')
            episodes = ep_soup.select('a[href*="/episode/"]')
            print(f"   => Episodes mile: {len(episodes)}")
            
            for ep in episodes[:1]: # Sirf 1 episode test ke liye
                ep_url = ep['href']
                if not ep_url.startswith('http'):
                    ep_url = "https://animesalt.in" + ep_url
                    
                data = BeautifulSoup(requests.get(ep_url, headers=headers).text, 'html.parser')
                title = data.find("meta", property="og:title")["content"] if data.find("meta", property="og:title") else "No Title"
                video = data.find("iframe")['src'] if data.find("iframe") else "N/A"
                thumb = get_tmdb_thumb(anime_name, 1, 1)
                
                sheet.append_row([anime_name, "01", title, thumb, ep_url, video, "FALSE"])
                print(f"   ✅ SUCCESS: {title} sheet me add ho gaya!")
                time.sleep(1)
        except Exception as e:
            print(f"   ❌ ERROR: {e}")

print("🏁 Scraper Finish!")
