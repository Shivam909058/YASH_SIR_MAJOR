import os
from dotenv import load_dotenv

load_dotenv()

# Twitter API Configuration
TWITTER_CONFIG = {
    'API_KEY': os.getenv('API_KEY'),
    'API_KEY_SECRET': os.getenv('API_KEY_SECRET'),
    'ACCESS_TOKEN': os.getenv('ACCESS_TOKEN'),
    'ACCESS_TOKEN_SECRET': os.getenv('ACCESS_TOKEN_SECRET'),
    'BEARER_TOKEN': os.getenv('BEARER_TOKEN')
}

# Model Paths
MODEL_PATHS = {
    'HATE_SPEECH': 'Models/LogisticRegression.pickle',
    'VECTORIZER': 'Models/CountVectorizerLR.pickle',
    'PERSONALITY_VECTORIZER': 'Models/cntizer.pickle',
    'PERSONALITY_TRANSFORMER': 'Models/tfizer.pickle',
    'PERSONALITY_DATASET': 'Datasets/mbti_1.csv'
}

# API Configuration
API_CONFIG = {
    'HOST': '0.0.0.0',
    'PORT': 8000,
    'DEBUG': True
}