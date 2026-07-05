import time
import logging
import os
from datetime import datetime

from scraper import scrape_anime
from sheet import update_google_sheet
from config import CHECK_INTERVAL

# Ensure directories exist
os.makedirs("logs", exist_ok=True)
os.makedirs("cache", exist_ok=True)

# Logging Setup
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
            logger.info(f"🔄 Scrape cycle started at {datetime.now()}")
            new_data = scrape_anime()
            if new_data:
                update_google_sheet(new_data)
                logger.info(f"✅ Updated {len(new_data)} items")
            else:
                logger.info("ℹ️ No new content found")
        except Exception as e:
            logger.error(f"❌ Error: {e}", exc_info=True)
        
        logger.info(f"⏳ Sleeping for {CHECK_INTERVAL//60} minutes...")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
