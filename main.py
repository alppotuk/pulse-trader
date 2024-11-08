import os
from dotenv import load_dotenv
from listeners.rss_feed_listener import RSSFeedListener
from utils.logger import Logger
from utils.database_utils import save_pulse_to_db  # Direct import
import threading
import time


def database_consumer(pulse):
    """Saves analyzed message (pulse) to the database."""
    save_pulse_to_db(pulse)  # Save pulse directly to DB


# def trader_consumer(pulse):
#     """Notify the trader bot and make a trading decision."""
#     trader_decision(pulse)  # Make a trading decision based on pulse


def main():
    try:
        load_dotenv("config/.env")  # Load environment variables
        logger = Logger("Main")
        rss_feed_url = "https://feeds.bloomberg.com/markets/news.rss"
        rss_feed_url = "https://www.investing.com/rss/forex.rss"
        polling_interval = 60


        rss_feed_listener = RSSFeedListener(rss_feed_url, polling_interval)
        rss_feed_listener.run()

        num_iterations = 2
        for _ in range(num_iterations):
            logger.log("info", f"Iteration: {_ + 1}")
            time.sleep(polling_interval)

        rss_feed_listener.stop()
        logger.log("info", "Listener stopped")

    except Exception as e:
        logger.log("error", f"An error occurred: {e}")


if __name__ == "__main__":
    main()
