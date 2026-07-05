import time
import logging
from datetime import datetime

from scraper import scrape_anime
from sheet import update_google_sheet
from config import CHECK_INTERVAL

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/scraper.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main():
    logger.info("🚀 Anime Stream Sync Started...")
    while True:
        try:
            logger.info(f"🔄 Scrape cycle at {datetime.now()}")
            new_data = scrape_anime()
            if new_data:
                update_google_sheet(new_data)
                logger.info(f"✅ Updated {len(new_data)} items")
        except Exception as e:
            logger.error(f"Error: {e}", exc_info=True)
        
        logger.info(f"⏳ Sleeping {CHECK_INTERVAL//60} min...")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
