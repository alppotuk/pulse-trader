from datetime import datetime

class Pulse:
    def __init__(self, content, sentiment, metadata):
        self.content = content
        self.sentiment = sentiment
        self.metadata = metadata if metadata is not None else {}
        self.timestamp = datetime.now()  
    
    def get_summary(self):
        summary = (
                   f"   Target Company: {self.metadata.get('target_company')}\n"
                   f"   Content: {self.content}\n"
                   f"   Sentiment: {self.sentiment}\n"
                   f"   Polarity: {self.metadata.get('polarity'):.2f}\n"
                   f"   Subjectivity: {self.metadata.get('subjectivity'):.2f}\n"
                   f"   Timestamp: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        return summary
    
    def as_dict(self):
        return {
            "content": self.content,
            "sentiment": self.sentiment,
            "metadata": self.metadata,
            "timestamp": self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }