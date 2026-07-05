import requests
import logging
import time
from bs4 import BeautifulSoup

from config import TARGET_SITES, USER_AGENT
from parser import parse_anime_list, parse_episode_page
from cache import load_cache, save_cache
from sheet import update_google_sheet

logger = logging.getLogger(__name__)

def scrape_anime():
    cache = load_cache()
    new_data = []
    headers = {"User-Agent": USER_AGENT}

    for base_url in TARGET_SITES:
        try:
            logger.info(f"Scraping homepage: {base_url}")
            resp = requests.get(base_url, headers=headers, timeout=20)
            soup = BeautifulSoup(resp.text, 'lxml')
            
            anime_list = parse_anime_list(soup)
            logger.info(f"Found {len(anime_list)} anime on homepage")

            for anime in anime_list[:30]:  # Limit for speed
                anime_id = anime['id']
                if anime_id in cache and len(cache[anime_id]) > 0:
                    continue  # Already processed

                logger.info(f"Processing new anime: {anime['name']}")

                # Episode page scrape (basic for now)
                episodes = []
                try:
                    ep_data = parse_episode_page(anime['url'])
                    if ep_data:
                        episodes.append({
                            'number': 1,
                            'title': ep_data.get('title', f"Episode 1 - {anime['name']}"),
                            'thumbnail': anime.get('poster', ''),
                            'streams': {"720": "https://example.com/placeholder.m3u8"},  # TODO: real extractor
                            'hindi_dub': True
                        })
                except:
                    pass

                if episodes:
                    new_data.append({'anime': anime, 'episodes': episodes})
                    cache[anime_id] = [1]

                time.sleep(2)  # Be gentle

        except Exception as e:
            logger.error(f"Error scraping {base_url}: {e}")

    save_cache(cache)
    return new_data
