import feedparser
import os
from pulse_adapter import PulseAdapter
from pulse import Pulse
from logger import logger
from textblob import TextBlob

import nltk
nltk.download('punkt_tab')

class RSSFeedListener(PulseAdapter):
    def __init__(self, rss_feed_url):
        super().__init__(source_type="RSSFeed")

        self.feed_url = rss_feed_url
        
        if not self.feed_url:
            logger.error("RSS feed URL is missing. Please ensure it's set in the .env file.")
            raise ValueError("RSS feed URL is required to fetch data from the RSS feed.")

        logger.info("RSSFeedListener initialized with feed URL: %s", self.feed_url)

    def fetch_data(self):
        try:
            feed = feedparser.parse(self.feed_url)
            if feed.entries:
                self.raw_data = feed.entries[0].title + ": " + feed.entries[0].summary
                logger.debug("Fetched data: %s", self.raw_data)
            else:
                self.raw_data = None
                logger.warning("No entries found in the RSS feed.")
        except Exception as e:
            logger.error(f"Failed to fetch RSS feed: {e}")
            self.raw_data = None
        return self.raw_data

    def process_data(self):
        if self.raw_data:
            self.pulse_data = self.raw_data.strip()  
            self.calculate_sentiment()
            logger.debug("Processed data: %s", self.pulse_data)
        return self.pulse_data

    def calculate_sentiment(self):
        if self.pulse_data:
            blob = TextBlob(self.pulse_data)
            self.blob = blob
            self.sentiment = "Positive" if blob.sentiment.polarity > 0 else "Negative"
            
            noun_phrases = blob.noun_phrases
            
            self.metadata = {
                "polarity": blob.sentiment.polarity,
                "subjectivity": blob.sentiment.subjectivity,
                "noun_phrases": noun_phrases  
            }
            
            logger.debug(f"Calculated sentiment: {self.sentiment}, "
                        f"polarity: {self.metadata['polarity']:.2f}, "
                        f"subjectivity: {self.metadata['subjectivity']:.2f}, "
                        f"noun phrases: {', '.join(self.metadata['noun_phrases'])}")
        return self.sentiment

    def get_pulse(self):
        processed_data = self.process_data()
        sentiment = self.calculate_sentiment()
        
        if processed_data and sentiment:
            pulse = Pulse(content=processed_data, sentiment=sentiment, metadata=self.metadata)
            logger.info(f"Pulse created by RSSListener: {pulse.content}, Sentiment: {pulse.sentiment}")
            return pulse
        return None

if __name__ == "__main__":
    try:
        logger.info("Starting RSS feed listener...")

        rss_feed_listener = RSSFeedListener()

        raw_feed_entry = rss_feed_listener.fetch_data()
        pulse = rss_feed_listener.get_pulse()

    except Exception as e:
        logger.error(f"An error occurred: {e}")
