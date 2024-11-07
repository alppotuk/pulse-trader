import feedparser
import time
from pulse import Pulse

from listeners.listener_adapter import ListenerAdapter
from processors.sentiment_analyzer import SentimentAnalyzer
from utils.database_utils import save_pulse_to_db

class RSSFeedListener(ListenerAdapter):
    def __init__(self, rss_feed_url, polling_interval=60):
        super().__init__(source_type="RSSFeed")

        self.feed_url = rss_feed_url
        self.polling_interval = polling_interval

        if not self.feed_url:
            self.logger.log('error', "RSS feed URL property is missing.")
            raise ValueError("RSS feed URL is required to fetch data.")

        self.logger.log("info", f"RSSFeedListener initialized with feed URL: {self.feed_url}")

        self.latest_entry = None
        self.running = False
        self.sentiment_analyzer = SentimentAnalyzer()

    def run(self):
        self.running = True
        while self.running:
            try:
                raw_feed_entry = self.fetch_data()
                self.logger.log("debug", f"Fetched raw feed entry: {raw_feed_entry}")

                if raw_feed_entry:
                    if  raw_feed_entry != self.latest_entry: # new entry
                        self.logger.log("info", "New entry detected. Processing...")
                        self.latest_entry = raw_feed_entry
                        pulse = self.get_pulse()
                        if pulse:
                            self.logger.log("info", f"Pulse created: \n{pulse.get_summary()}")
                            save_pulse_to_db(pulse)

                        else:
                            self.logger.log("warning", "Failed to create pulse from fetched data.")
                    else: # no new entry
                        self.latest_entry = raw_feed_entry
                        self.logger.log("debug", "No new entries found in the RSS feed.")
            except Exception as e:
                self.logger.log("error", f"Failed to fetch RSS feed: {e}")

            time.sleep(self.polling_interval)

    def stop(self):
        self._stop_event.set()

    def fetch_data(self):
        try:
            feed = feedparser.parse(self.feed_url)
            if feed.entries:
                self.raw_data = feed.entries[0].title + ": " + feed.entries[0].summary
                return self.raw_data
            else:
                self.logger.log("warning", "No entries found in the RSS feed.")
                return None
        except Exception as e:
            self.logger.log("error", f"Failed to fetch RSS feed: {e}")
            return None

        

    def get_pulse(self):
        """Processes data and returns analyzed data as a Pulse"""
        if self.raw_data:
            processed_data = self.raw_data.strip()
            self.logger.log("debug", f"Processing data: {processed_data}")
            sentiment_analysis = self.sentiment_analyzer.analyze(processed_data)
            self.metadata = {
                "company_name": sentiment_analysis['company_name'],
                "compound": sentiment_analysis['compound'],
                "negative": sentiment_analysis['neg'],
                "positive": sentiment_analysis['pos'],
                "neutral": sentiment_analysis['neu'],
                "sentiment": sentiment_analysis['sentiment']
            }
        
            pulse = Pulse(content=processed_data, sentiment_result=self.metadata, company=self.metadata['company_name'])
            return pulse
        else:
            self.logger.log("warning", f"Failed to create pulse. Processed data: {processed_data}")
            return None
