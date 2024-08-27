import os
from dotenv import load_dotenv
from rss_feed_listener import RSSFeedListener
from logger import logger

load_dotenv()

def main():
    try:
        logger.info("Starting RSS feed listener...")
        rss_feed_listener = RSSFeedListener("https://feeds.bloomberg.com/markets/news.rss")
        raw_feed_entry = rss_feed_listener.fetch_data()
        
        if raw_feed_entry:
            logger.info("Raw feed entry fetched: %s", raw_feed_entry)

        pulse = rss_feed_listener.get_pulse()
        
        if pulse:
            logger.info("Pulse created: %s", pulse.content)
        else:
            logger.warning("No pulse created. Check RSS feed or processing.")

    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
