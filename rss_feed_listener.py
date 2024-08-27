import feedparser
import os
from pulse_adapter import PulseAdapter
from pulse import Pulse
from logger import logger
from textblob import TextBlob
import threading
import time
import nltk
nltk.download('punkt_tab')
import spacy 


class RSSFeedListener(PulseAdapter):
    def __init__(self, rss_feed_url, polling_interval=60):
        super().__init__(source_type="RSSFeed")

        self.feed_url = rss_feed_url
        self.polling_interval = polling_interval

        if not self.feed_url:
            logger.error("RSS feed URL property is missing.")
            raise ValueError("RSS feed URL is required to fetch data.")

        logger.info("RSSFeedListener initialized with feed URL: %s", self.feed_url)

        self._latest_entry = None
        self._stop_event = threading.Event()

        # Load spaCy model for named entity recognition (NER)
        self.nlp = spacy.load('en_core_web_sm')  # Consider using a smaller model for efficiency

    def run(self):
        while not self._stop_event.is_set():
            try:
                raw_feed_entry = self.fetch_data()
                logger.debug(f"Fetched raw feed entry: {raw_feed_entry}")

                if raw_feed_entry:
                    if self._latest_entry and raw_feed_entry != self._latest_entry:
                        logger.info(f"New entry detected. Processing...")
                        self._latest_entry = raw_feed_entry
                        pulse = self.get_pulse()
                        if pulse:
                            logger.info(f"Pulse created: \n{pulse.get_summary()}")  # Log summary for debugging
                        else:
                            logger.warning("Failed to create pulse from fetched data.")
                    else:
                        self._latest_entry = raw_feed_entry
                        logger.debug("No new entries found in the RSS feed.")

            except Exception as e:
                logger.error(f"Failed to fetch RSS feed: {e}")

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
                logger.warning("No entries found in the RSS feed.")
                return None
        except Exception as e:
            logger.error(f"Failed to fetch RSS feed: {e}")
            return None

    def process_data(self):
        if self.raw_data:
            self.pulse_data = self.raw_data.strip()
            self.calculate_sentiment()
            logger.debug("Processed data: %s", self.pulse_data)
            return self.pulse_data

        return None

    def calculate_sentiment(self):
        if self.pulse_data:
            blob = TextBlob(self.pulse_data)
            self.blob = blob
            self.sentiment = "Positive" if blob.sentiment.polarity > 0 else "Negative"

            noun_phrases = blob.noun_phrases

            # Use spaCy for named entity recognition (NER)
            doc = self.nlp(self.pulse_data)
            for entity in doc.ents:
                if entity.label_ in ('ORG', 'COMPANY'):  # Focus on organizations and companies
                    self.target_company = entity.text
                    break  # Only extract the first company mentioned

            self.metadata = {
                "polarity": blob.sentiment.polarity,
                "subjectivity": blob.sentiment.subjectivity,
                "noun_phrases": noun_phrases,
                "target_company": self.target_company if hasattr(self, 'target_company') else None,
            }

            return self.sentiment

    def get_pulse(self):
        processed_data = self.process_data()
        sentiment = self.calculate_sentiment()

        if processed_data and sentiment:
            pulse = Pulse(content=processed_data, sentiment=sentiment, metadata=self.metadata)
            return pulse
        else:
            logger.warning("Failed to create pulse. Processed data: %s, Sentiment: %s", processed_data, sentiment)
            return None