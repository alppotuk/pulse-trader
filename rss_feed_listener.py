import feedparser
import threading
import time
from pulse_adapter import PulseAdapter
from pulse import Pulse
from sentiment_analyzer import SentimentAnalyzer

class RSSFeedListener(PulseAdapter):
    def __init__(self, rss_feed_url, polling_interval=60):
        super().__init__(source_type="RSSFeed")

        self.feed_url = rss_feed_url
        self.polling_interval = polling_interval

        if not self.feed_url:
            self.logger.log('error', "RSS feed URL property is missing.")
            raise ValueError("RSS feed URL is required to fetch data.")

        self.logger.log("info", f"RSSFeedListener initialized with feed URL: {self.feed_url}")

        self._latest_entry = None
        self._stop_event = threading.Event()
        self.sentiment_analyzer = SentimentAnalyzer()

    def run(self):
        while not self._stop_event.is_set():
            try:
                raw_feed_entry = self.fetch_data()
                self.logger.log("debug", f"Fetched raw feed entry: {raw_feed_entry}")

                if raw_feed_entry:
                    if self._latest_entry and raw_feed_entry != self._latest_entry:
                        self.logger.log("info", "New entry detected. Processing...")
                        self._latest_entry = raw_feed_entry
                        pulse = self.get_pulse()
                        if pulse:
                            self.logger.log("info", f"Pulse created: \n{pulse.get_summary()}")
                        else:
                            self.logger.log("warning", "Failed to create pulse from fetched data.")
                    else:
                        self._latest_entry = raw_feed_entry
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

    def process_data(self):
        if self.raw_data:
            self.pulse_data = self.raw_data.strip()
            self.logger.log("debug", f"Processing data: {self.pulse_data}")
            sentiment_analysis = self.sentiment_analyzer.analyze(self.pulse_data)
            self.metadata = {
                "company_name": sentiment_analysis['company_name'],
                "compound": sentiment_analysis['compound'],
                "negative": sentiment_analysis['neg'],
                "positive": sentiment_analysis['pos'],
                "neutral": sentiment_analysis['neu'],
                "sentiment": sentiment_analysis['sentiment']
            }
            return self.pulse_data
        return None

    def get_pulse(self):
        processed_data = self.process_data()

        if processed_data:
            pulse = Pulse(content=processed_data, sentiment_result=self.metadata, company=self.metadata['company_name'])
            return pulse
        else:
            self.logger.log("warning", f"Failed to create pulse. Processed data: {processed_data}")
            return None
