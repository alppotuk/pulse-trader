from datetime import datetime

class Pulse:
    def __init__(self, content, sentiment_result, target):
        self.content = content
        self.sentiment = sentiment_result  
        self.target_asset = target  
        self.timestamp = datetime.now()

    def get_summary(self):
        summary = (
            f"Target asset: {self.target_asset}\n"
            f"Content: {self.content}\n"
            f"Sentiment: {self.sentiment}\n" 
            f"Compound Scrore: {self.sentiment['compound']:.2f}\n"
            f"Timestamp: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
        )
        return summary

    def as_dict(self):
        return {
            "content": self.content,
            "sentiment": self.sentiment, 
            "target": self.target_asset,
            "timestamp": self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }
