import os
import tweepy
from dotenv import load_dotenv

load_dotenv()

class TwitterListener(ListenerAdapter):
    def __init__(self):
        super().__init__(source_type="Twitter")

        
        self.api_key = os.getenv("API_KEY")
        self.api_secret_key = os.getenv("API_SECRET_KEY")
        self.access_token = os.getenv("ACCESS_TOKEN")
        self.access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")
        self.target_account = os.getenv("TARGET_ACCOUNT")

        
        auth = tweepy.OAuthHandler(self.api_key, self.api_secret_key)
        auth.set_access_token(self.access_token, self.access_token_secret)
        self.api = tweepy.API(auth)

        
        self.stream_listener = TwitterStreamListener(self)
        self.stream = tweepy.Stream(auth=self.api.auth, listener=self.stream_listener)

    def start_stream(self):
        
        self.stream.filter(follow=[self.target_account])

    def process_data(self, raw_data):
        
        self.pulse_data = raw_data.strip()
        return self.pulse_data

    def calculate_sentiment(self, processed_data):
        
        self.sentiment = "Positive" if "profit" in processed_data.lower() else "Negative"
        return self.sentiment

    def get_pulse(self, processed_data, sentiment):
        
        pulse = Pulse(content=processed_data, sentiment=sentiment)
        return pulse