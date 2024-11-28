import re
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

# Download required NLTK data
nltk.download('stopwords')
nltk.download('wordnet')

class TweetCleaner:
    def __init__(self):
        self.tokenizer = RegexpTokenizer(r'\w+')
        self.stopwords = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()

    def remove_links_and_mentions(self, text):
        """Remove URLs, @mentions, and #hashtags"""
        text = re.sub(r'http[s]?://\S+', '', text)
        text = re.sub(r'@\w+', '', text)
        text = re.sub(r'#\w+', '', text)
        return text.strip()

    def remove_invalid_chars(self, text):
        """Remove non-ASCII characters"""
        text = self.remove_links_and_mentions(text)
        return ''.join(char for char in text if ord(char) < 128)

    def clean_tweet(self, tweet):
        """Clean a single tweet"""
        tweet = str(tweet).lower()
        tweet = self.remove_invalid_chars(tweet)
        tweet = re.sub(r'\s+', ' ', tweet)
        
        # Tokenize and remove stopwords
        tokens = self.tokenizer.tokenize(tweet)
        tokens = [token for token in tokens if token not in self.stopwords]
        
        # Lemmatize
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens]
        
        return ' '.join(tokens)

    def clean_tweets(self, tweets):
        """Clean a list of tweets"""
        return [self.clean_tweet(tweet) for tweet in tweets]
