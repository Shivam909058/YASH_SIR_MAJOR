import pandas as pd
import numpy as np
import pickle
from src.config import MODEL_PATHS
from src.tweetcleaner import TweetCleaner

class PersonalityPredictor:
    def __init__(self):
        # Load the personality dataset
        self.data = pd.read_csv(MODEL_PATHS['PERSONALITY_DATASET'])
        
        # Load pre-trained models
        with open(MODEL_PATHS['PERSONALITY_VECTORIZER'], 'rb') as f:
            self.cntizer = pickle.load(f)
        with open(MODEL_PATHS['PERSONALITY_TRANSFORMER'], 'rb') as f:
            self.tfizer = pickle.load(f)
        
        # Initialize tweet cleaner
        self.tweet_cleaner = TweetCleaner()
        
        # Personality type mappings
        self.personality_map = {
            'I': 0, 'E': 1,
            'N': 0, 'S': 1,
            'F': 0, 'T': 1,
            'J': 0, 'P': 1
        }
        
        self.personality_list = [
            {0: 'I', 1: 'E'},
            {0: 'N', 1: 'S'},
            {0: 'F', 1: 'T'},
            {0: 'J', 1: 'P'}
        ]
        
        self.personality_types = [
            'INFJ', 'ENTP', 'INTP', 'INTJ', 'ENTJ', 'ENFJ', 'INFP', 'ENFP',
            'ISFP', 'ISTP', 'ISFJ', 'ISTJ', 'ESTP', 'ESFP', 'ESTJ', 'ESFJ'
        ]
        self.personality_types = [x.lower() for x in self.personality_types]

    def preprocess_text(self, text):
        """Preprocess the input text"""
        cleaned_text = self.tweet_cleaner.clean_tweet(text)
        features = self.cntizer.transform([cleaned_text])
        features = self.tfizer.transform(features)
        return features

    def get_personality(self, text):
        """Predict personality type from text"""
        try:
            if not text or len(text.strip()) == 0:
                return "Insufficient text for analysis"

            # Preprocess the text
            features = self.preprocess_text(text)
            
            # Make predictions for each personality dimension
            predictions = []
            for model_name in ['IE', 'NS', 'FT', 'JP']:
                with open(f'Models/{model_name}_personality.pickle', 'rb') as f:
                    model = pickle.load(f)
                    pred = model.predict(features)[0]
                    predictions.append(pred)
            
            # Convert predictions to personality type
            personality_type = ''
            for i, pred in enumerate(predictions):
                personality_type += self.personality_list[i][pred]
            
            return personality_type.upper()

        except Exception as e:
            print(f"Error in personality prediction: {str(e)}")
            return "Error in analysis"

