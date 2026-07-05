import requests
from bs4 import BeautifulSoup
from config import TMDB_API_KEY

def parse_anime_list(soup):
    """Animesalt.in ke homepage/recent se anime list nikaalne ke liye"""
    items = []
    # Animesalt ke common selectors
    for card in soup.select('a[href*="/anime/"], .anime-card, .series-item'):
        link = card.get('href') or card.get('data-href')
        if not link:
            continue
        title_tag = card.select_one('h3, .title, .name, img[alt]')
        title = title_tag.get('alt') or title_tag.text.strip() if title_tag else ''
        
        items.append({
            'id': link.split('/')[-1].split('-')[0] if link else 'unknown',
            'name': title,
            'url': link if link.startswith('http') else 'https://animesalt.in' + link,
            'poster': ''
        })
    return items

def parse_episode_page(url):
    """Particular episode page se data nikaalna"""
    try:
        resp = requests.get(url, timeout=15)
        soup = BeautifulSoup(resp.text, 'lxml')
        
        # Player iframe ya video source dhundna
        player = soup.find('iframe') or soup.find('video')
        player_url = player.get('src') if player else url
        
        return {
            'title': soup.find('h1').text.strip() if soup.find('h1') else 'Episode',
            'thumbnail': '',
            'player_url': player_url
        }
    except:
        return None
