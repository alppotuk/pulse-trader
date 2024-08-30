from datetime import datetime

class Pulse:
    def __init__(self, content, sentiment_result, company):
        self.content = content
        self.sentiment = sentiment_result  # Use the entire sentiment dictionary
        self.company_name = company  # Add company name to metadata
        self.timestamp = datetime.now()

    def get_summary(self):
        summary = (
            f"Target Company: {self.company_name}\n"
            f"Content: {self.content}\n"
            f"Sentiment: {self.sentiment}\n"  # Now correctly uses the sentiment category
            f"Polarity: {self.sentiment['compound']:.2f}\n"
            f"Timestamp: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
        )
        return summary

    def as_dict(self):
        return {
            "content": self.content,
            "sentiment": self.sentiment,  # Use the entire sentiment dictionary
            "company": self.company_name,
            "timestamp": self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }
