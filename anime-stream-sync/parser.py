import requests
from bs4 import BeautifulSoup
from config import TMDB_API_KEY

def parse_anime_list(soup):
    """Animesalt.in homepage se anime list"""
    items = []
    # Animesalt ke common card selectors
    cards = soup.select('.anime-card, .series, .item, a[href*="/anime/"]')
    
    for card in cards:
        link_tag = card.find('a') or card
        link = link_tag.get('href', '')
        
        if not link or '/episode/' in link:
            continue
            
        title_tag = card.select_one('h3, .title, .name, img')
        title = title_tag.get('alt') or title_tag.text.strip() if title_tag else ''
        
        if title and link:
            full_link = link if link.startswith('http') else 'https://animesalt.in' + link
            items.append({
                'id': full_link.split('/')[-1],
                'name': title,
                'url': full_link,
                'poster': ''
            })
    return items[:20]  # Limit for testing

def parse_episode_page(url):
    """Episode page se player aur details"""
    try:
        resp = requests.get(url, timeout=15)
        soup = BeautifulSoup(resp.text, 'lxml')
        
        title = soup.find('h1')
        title = title.text.strip() if title else 'Episode'
        
        # Player iframe dhundna
        iframe = soup.find('iframe')
        player_url = iframe.get('src') if iframe else url
        
        return {
            'title': title,
            'thumbnail': '',
            'player_url': player_url
        }
    except:
        return None
