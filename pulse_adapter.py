from abc import ABC, abstractmethod
from logger import logger

class PulseAdapter(ABC):
    def __init__(self, source_type):
        self.source_type = source_type   
        self.raw_data = None             # Raw data fetched from the source
        self.pulse_data = None           # Processed data as a Pulse object
        self.sentiment = None            # Sentiment calculated from the pulse data
        self.blob = None                
        logger.info(f"Initialized PulseAdapter for {self.source_type}")
    @abstractmethod
    def fetch_data(self):
        pass

    @abstractmethod
    def process_data(self):
        pass

    @abstractmethod
    def calculate_sentiment(self):
        pass

    @abstractmethod
    def get_pulse(self):
        pass
