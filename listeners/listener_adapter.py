from abc import ABC, abstractmethod
from utils.logger import Logger

class ListenerAdapter(ABC):
    def __init__(self, source_type):
        self.source_type = source_type   
        self.logger = Logger(source_type)
        self.raw_data = None             # Raw data fetched from the source
        self.pulse = None           # Processed data as a Pulse object
        
    @abstractmethod
    def fetch_data(self):
        pass


    @abstractmethod
    def get_pulse(self):
        pass
