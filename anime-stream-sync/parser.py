import requests
from bs4 import BeautifulSoup

def parse_anime_list(soup):
    items = []
    print("DEBUG: Page title:", soup.title.string if soup.title else "No title")
    
    # Broad search for anime links
    for a in soup.find_all('a', href=True):
        href = a['href']
        if '/anime/' in href and len(href) > 15:
            # Try to get title from different places
            title = a.get('title') or ''
            if not title:
                img = a.find('img')
                if img:
                    title = img.get('alt', '')
            if not title:
                title = a.text.strip()
                
            if len(title) > 5 and 'episode' not in title.lower():
                full_url = 'https://animesalt.ac' + href if not href.startswith('http') else href
                items.append({
                    'id': full_url.split('/')[-1].split('-')[0],
                    'name': title,
                    'url': full_url,
                    'poster': ''
                })
    
    # Remove duplicates
    unique = {item['url']: item for item in items}
    print(f"DEBUG: Found {len(unique)} anime")
    return list(unique.values())[:25]

def get_tmdb_metadata(name):
    """TMDB se metadata (optional)"""
    return {}

def parse_episode_page(url):
    return {'title': 'Episode', 'player_url': url}
