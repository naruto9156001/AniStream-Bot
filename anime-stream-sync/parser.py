import requests
from bs4 import BeautifulSoup

def parse_anime_list(soup):
    items = []
    for card in soup.select('a, div, h3'):
        link = card.get('href', '')
        if '/anime/' in link or '/series/' in link:
            title = card.get('title') or card.text.strip()
            if len(title) > 5:
                full_url = link if link.startswith('http') else 'https://animesalt.in' + link
                items.append({
                    'id': full_url.split('/')[-1],
                    'name': title,
                    'url': full_url,
                    'poster': ''
                })
    return list({v['url']:v for v in items}.values())[:15]

def get_tmdb_metadata(name):
    """TMDB metadata"""
    try:
        url = f"https://api.themoviedb.org/3/search/tv?api_key={TMDB_API_KEY}&query={name.replace(' ', '+')}"
        data = requests.get(url).json()
        if data.get('results'):
            item = data['results'][0]
            return {
                'synopsis': item.get('overview', ''),
                'poster': f"https://image.tmdb.org/t/p/w500{item.get('poster_path')}" if item.get('poster_path') else '',
                'year': item.get('first_air_date', '')[:4]
            }
    except:
        pass
    return {}

def parse_episode_page(url):
    return {'title': 'Episode', 'player_url': url}
