import requests
from bs4 import BeautifulSoup

def parse_anime_list(soup):
    items = []
    print("DEBUG: Page title:", soup.title.string if soup.title else "No title")
    
    # Better selector for animesalt.ac cards
    for post in soup.select('li.post, article.post'):
        link_tag = post.select_one('a[href*="/series/"], a.lnk-blk')
        if not link_tag:
            continue
            
        href = link_tag.get('href', '')
        if not href or '/series/' not in href:
            continue
            
        # Title
        title_tag = post.select_one('h2.entry-title')
        title = title_tag.text.strip() if title_tag else ''
        
        if len(title) < 3:
            continue
            
        full_url = href if href.startswith('http') else 'https://animesalt.ac' + href
        
        # Poster
        img = post.select_one('img')
        poster = img.get('data-src') or img.get('src', '') if img else ''
        
        items.append({
            'id': full_url.split('/')[-2] if '/series/' in full_url else full_url.split('/')[-1],
            'name': title,
            'url': full_url,
            'poster': poster
        })
    
    unique = {item['url']: item for item in items}
    print(f"DEBUG: Found {len(unique)} anime")
    return list(unique.values())[:30]

def get_tmdb_metadata(name):
    return {}

def parse_episode_page(url):
    return {'title': 'Episode', 'player_url': url}
