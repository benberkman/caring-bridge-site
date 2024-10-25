import json
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

nltk.download('vader_lexicon', quiet=True)

def calculate_sentiment_scores(entries):
    sia = SentimentIntensityAnalyzer()
    sentiment_scores = {}
    
    for entry in entries:
        score = sia.polarity_scores(entry['entry'])['compound']
        sentiment_scores[entry['date']] = round(score, 2)
    
    with open('sentiment_scores.json', 'w') as f:
        json.dump(sentiment_scores, f)
    
    return sentiment_scores

def load_sentiment_scores():
    try:
        with open('sentiment_scores.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
