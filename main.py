import os
from dotenv import load_dotenv
from rss_feed_listener import RSSFeedListener
from logger import Logger
import threading
import time

def main():
    try:
        load_dotenv()
        logger = Logger("Main")
        rss_feed_url = os.getenv("RSS_FEED_URL", "https://feeds.bloomberg.com/markets/news.rss")
        polling_interval = int(os.getenv("POLLING_INTERVAL", 60))  


        rss_feed_listener = RSSFeedListener(rss_feed_url, polling_interval)

        listener_thread = threading.Thread(target=rss_feed_listener.run)
        listener_thread.start()

        num_iterations = 10
        for _ in range(num_iterations):
            logger.log("info",f"Iteration: {_ + 1}")
            time.sleep(polling_interval)

        rss_feed_listener.stop()
        logger.log("info","Listener stopped")

        listener_thread.join()  
        logger.log("info","Thread stopped")

    except Exception as e:
        logger.log("error",f"An error occurred: {e}")

if __name__ == "__main__":
    main()
