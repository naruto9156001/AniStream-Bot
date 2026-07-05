from bs4 import BeautifulSoup
import time

def parse_anime_list(soup):
    items = []
    print("DEBUG: Page title:", soup.title.string if soup.title else "No title")
    
    # Selenium ke liye better parsing
    for a in soup.find_all('a', href=True):
        href = a['href']
        if '/anime/' in href and len(href) > 15:
            title = a.get('title') or (a.find('img').get('alt') if a.find('img') else a.text.strip())
            if len(title) > 5 and 'episode' not in title.lower():
                full_url = 'https://animesalt.ac' + href if not href.startswith('http') else href
                items.append({
                    'id': full_url.split('/')[-1].split('-')[0],
                    'name': title,
                    'url': full_url,
                    'poster': ''
                })
    
    unique = {item['url']: item for item in items}
    print(f"DEBUG: Found {len(unique)} anime")
    return list(unique.values())[:30]
