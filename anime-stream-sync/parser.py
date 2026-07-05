import requests
from bs4 import BeautifulSoup

def parse_anime_list(soup):
    items = []
    print("DEBUG: Page title:", soup.title.string if soup.title else "No title")  # Debug
    
    # Try multiple possible selectors
    for selector in ['a[href*="/anime/"]', 'a[href*="/series/"]', '.card', '.anime', 'h3 a']:
        for card in soup.select(selector):
            link = card.get('href', '')
            if link and ('/anime/' in link or '/series/' in link):
                title = card.get('title') or card.text.strip()
                if len(title) > 5:
                    full_url = 'https://animesalt.in' + link if not link.startswith('http') else link
                    items.append({
                        'id': full_url.split('/')[-1],
                        'name': title,
                        'url': full_url,
                        'poster': ''
                    })
    print(f"DEBUG: Found {len(items)} anime")  # Debug
    return items[:10]

def get_tmdb_metadata(name):
    return {}

def parse_episode_page(url):
    return {'title': 'Episode', 'player_url': url}
