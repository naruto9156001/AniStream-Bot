import requests
from bs4 import BeautifulSoup

def parse_anime_list(soup):
    items = []
    # Stronger selectors for animesalt.in
    for card in soup.select('a, div'):
        link = card.get('href', '')
        if '/anime/' in link or '/series/' in link:
            title = card.get('title') or card.text.strip()
            if len(title) > 3 and title not in ['Home', 'Anime', 'Login']:
                full_url = link if link.startswith('http') else 'https://animesalt.in' + link
                items.append({
                    'id': full_url.split('/')[-1],
                    'name': title,
                    'url': full_url,
                    'poster': ''
                })
    return list({v['url']:v for v in items}.values())  # remove duplicates

def parse_episode_page(url):
    try:
        r = requests.get(url, timeout=15)
        soup = BeautifulSoup(r.text, 'lxml')
        
        return {
            'title': soup.find('h1').text.strip() if soup.find('h1') else 'Episode',
            'player_url': url
        }
    except:
        return None
