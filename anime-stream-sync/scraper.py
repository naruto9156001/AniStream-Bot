import requests
import logging
import time
from bs4 import BeautifulSoup

from config import TARGET_SITES, USER_AGENT
from parser import parse_anime_list
from cache import load_cache, save_cache
from sheet import update_google_sheet

logger = logging.getLogger(__name__)

def scrape_anime():
    cache = load_cache()
    new_data = []
    headers = {"User-Agent": USER_AGENT}

    for base_url in TARGET_SITES:
        try:
            logger.info(f"Scraping {base_url}")
            resp = requests.get(base_url, headers=headers, timeout=20)
            soup = BeautifulSoup(resp.text, 'lxml')
            
            anime_list = parse_anime_list(soup)
            logger.info(f"Found {len(anime_list)} anime")

            for anime in anime_list[:15]:   # Limit for testing
                anime_id = anime['id']
                watched = cache.get(anime_id, [])

                # Agar naya anime hai toh add karo
                if anime_id not in cache or len(watched) == 0:
                    logger.info(f"New Anime: {anime['name']}")
                    new_data.append({
                        'anime': anime,
                        'episodes': [{
                            'number': 1,
                            'title': f"Episode 1 - {anime['name']}",
                            'thumbnail': anime.get('poster', ''),
                            'streams': {"720": "https://example.com/stream.m3u8"},
                            'hindi_dub': True
                        }]
                    })
                    cache[anime_id] = [1]

            time.sleep(4)  # Rate limiting
        except Exception as e:
            logger.error(f"Error {base_url}: {e}")

    save_cache(cache)
    return new_data
