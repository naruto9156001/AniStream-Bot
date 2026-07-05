import requests
from config import TMDB_API_KEY

def parse_anime_list(soup):
    """Update selectors according to your anime website"""
    items = []
    # Example selectors (change these)
    for card in soup.select('.card, .anime-item, .series-block, .item'):
        link = card.find('a')
        img = card.find('img')
        title = card.select_one('h3, .title, .name')
        items.append({
            'id': card.get('data-id') or (link['href'].split('/')[-1] if link else 'unknown'),
            'name': title.text.strip() if title else '',
            'url': link['href'] if link else '',
            'poster': img['src'] if img else ''
        })
    return items

def get_tmdb_metadata(name):
    if not TMDB_API_KEY:
        return {}
    try:
        url = f"https://api.themoviedb.org/3/search/tv?api_key={TMDB_API_KEY}&query={name.replace(' ', '+')}"
        data = requests.get(url).json()
        if data.get('results'):
            item = data['results'][0]
            return {
                'synopsis': item.get('overview', ''),
                'poster': f"https://image.tmdb.org/t/p/w500{item.get('poster_path')}" if item.get('poster_path') else '',
                'year': item.get('first_air_date', '')[:4],
                'imdb': item.get('vote_average', 0)
            }
    except:
        pass
    return {}
