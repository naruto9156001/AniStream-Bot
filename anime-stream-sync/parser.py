import requests
from bs4 import BeautifulSoup

def parse_anime_list(soup):
    items = []
    print("DEBUG: Page title:", soup.title.string if soup.title else "No title")
    
    # Better selectors for animesalt.ac
    for card in soup.select('a[href*="/anime/"], .poster, .item, .card'):
        link = card.get('href', '')
        if '/anime/' in link:
            title = card.get('title') or card.select_one('img').get('alt', '') if card.find('img') else ''
            if title:
                full_url = 'https://animesalt.ac' + link if not link.startswith('http') else link
                items.append({
                    'id': full_url.split('/')[-1],
                    'name': title,
                    'url': full_url,
                    'poster': ''
                })
    print(f"DEBUG: Found {len(items)} anime")
    return items[:20]

def get_tmdb_metadata(name):
    return {}

def parse_episode_page(url):
    return {'title': 'Episode', 'player_url': url}
