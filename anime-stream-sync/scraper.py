import requests
import logging
import time
from bs4 import BeautifulSoup

from config import TARGET_SITES, USER_AGENT, TMDB_API_KEY
from parser import parse_anime_list, get_tmdb_metadata
from extractor import extract_episode_data
from cache import load_cache, save_cache

logger = logging.getLogger(__name__)

def scrape_anime():
    cache = load_cache()
    new_data = []
    headers = {"User-Agent": USER_AGENT}

    for url in TARGET_SITES:
        try:
            resp = requests.get(url, headers=headers, timeout=20)
            soup = BeautifulSoup(resp.text, 'lxml')
            anime_list = parse_anime_list(soup)

            for anime in anime_list:
                tmdb = get_tmdb_metadata(anime['name']) if TMDB_API_KEY else {}
                anime.update(tmdb)

                new_eps = extract_episode_data(anime, cache.get(anime['id'], []))
                if new_eps:
                    new_data.append({'anime': anime, 'episodes': new_eps})
                    cache.setdefault(anime['id'], []).extend([ep['number'] for ep in new_eps])

            time.sleep(3)
        except Exception as e:
            logger.error(f"Error {url}: {e}")

    save_cache(cache)
    return new_data
