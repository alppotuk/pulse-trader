import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import spacy
from collections import Counter

nltk.download('vader_lexicon')
nltk.download('punkt')

nlp = spacy.load('en_core_web_sm')

class SentimentAnalyzer:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()

    def analyze(self, news_text):
        preprocessed_text = self.preprocess_text(news_text)
        sentiment_result, sentiment_scores = self.analyze_sentiment(preprocessed_text)
        company = self.identify_companies(news_text)

        return {
            'company_name': company,
            'sentiment': sentiment_result['sentiment'],  # Adjusted to align with Pulse
            'compound': sentiment_scores['compound'],
            'neg': sentiment_scores['neg'],
            'pos': sentiment_scores['pos'],
            'neu': sentiment_scores['neu']
        }

    def preprocess_text(self, text):
        text = text.lower()
        doc = nlp(text)
        tokens = [token.text for token in doc if not token.is_stop and not token.is_punct]
        preprocessed_text = ' '.join(tokens)
        return preprocessed_text

    def analyze_sentiment(self, text):
        sentiment = self.sia.polarity_scores(text)

        sentiment_result = {
            'sentiment': 'positive' if sentiment['compound'] > 0.2 else 'negative' if sentiment['compound'] < -0.2 else 'neutral',
            'compound': sentiment['compound'],
            'positive': sentiment['pos'],
            'negative': sentiment['neg'],
            'neutral': sentiment['neu']
        }

        return sentiment_result, sentiment

    def identify_companies(self, text):
        doc = nlp(text)
        entities = [ent.text for ent in doc.ents if ent.label_ == 'ORG']
        company = Counter(entities).most_common(1)[0][0] if entities else ''
        return company
