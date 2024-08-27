import os
import tweepy
from dotenv import load_dotenv
from pulse_adapter import PulseAdapter
from pulse import Pulse
from logger import logger

load_dotenv()

# NOT WORKING due to pricing

class TwitterStreamListener(PulseAdapter, tweepy.StreamingClient):
    def __init__(self):
        PulseAdapter.__init__(self, source_type="TwitterStream")

        self.bearer_token = os.getenv("BEARER_TOKEN")
        tweepy.StreamingClient.__init__(self, bearer_token=self.bearer_token)

        logger.info("TwitterStreamListener initialized with StreamingClient")

    def on_tweet(self, tweet):
        self.raw_data = tweet.text
        logger.debug(f"Received tweet: {self.raw_data}")

        self.process_data()
        pulse = self.get_pulse()
        if pulse:
            logger.info(f"Created pulse from tweet: {pulse.content}, Sentiment: {pulse.sentiment}")

    def on_request_error(self, status_code):
        logger.error(f"Request error with status code: {status_code}")

    def on_connection_error(self):
        logger.error("Connection error encountered")
        self.disconnect()

    def fetch_data(self):
        logger.info("Starting to stream tweets using rules...")
        
        self.add_rules(tweepy.StreamRule(f"from:{os.getenv('TARGET_ACCOUNT')}"))
        self.filter()

    def process_data(self):
        if self.raw_data:
            self.pulse_data = self.raw_data.strip() 
            logger.debug(f"Processed data: {self.pulse_data}")
        return self.pulse_data

    def calculate_sentiment(self):
        if self.pulse_data:
            self.sentiment = "Positive" if "profit" in self.pulse_data.lower() else "Negative"
            logger.debug(f"Calculated sentiment: {self.sentiment}")
        return self.sentiment

    def get_pulse(self):
        processed_data = self.process_data()
        sentiment = self.calculate_sentiment()

        if processed_data and sentiment:
            pulse = Pulse(content=processed_data, sentiment=sentiment)
            return pulse
        return None
