import requests
from bs4 import BeautifulSoup

def parse_anime_list(soup):
    items = []
    print("DEBUG: Page title:", soup.title.string if soup.title else "No title")
    
    # Dump some HTML for debugging
    print("DEBUG: Sample HTML:", str(soup)[:500])  # First 500 chars
    
    # Try general link finder
    for a in soup.find_all('a', href=True):
        link = a['href']
        if '/anime/' in link and len(link) > 20:
            title = a.get('title') or a.text.strip()
            if len(title) > 5 and not title.lower() in ['home', 'search', 'login']:
                full_url = 'https://animesalt.ac' + link if not link.startswith('http') else link
                items.append({
                    'id': full_url.split('/')[-1],
                    'name': title,
                    'url': full_url,
                    'poster': ''
                })
    print(f"DEBUG: Found {len(items)} anime")
    return items[:15]

def get_tmdb_metadata(name):
    return {}

def parse_episode_page(url):
    return {'title': 'Episode', 'player_url': url}
