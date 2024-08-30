from datetime import datetime

class Pulse:
    def __init__(self, content, sentiment_result, company):
        self.content = content
        self.sentiment = sentiment_result  
        self.company_name = company  
        self.timestamp = datetime.now()

    def get_summary(self):
        summary = (
            f"Target Company: {self.company_name}\n"
            f"Content: {self.content}\n"
            f"Sentiment: {self.sentiment}\n" 
            f"Polarity: {self.sentiment['compound']:.2f}\n"
            f"Timestamp: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
        )
        return summary

    def as_dict(self):
        return {
            "content": self.content,
            "sentiment": self.sentiment, 
            "company": self.company_name,
            "timestamp": self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }
