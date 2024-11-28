from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import numpy as np
import requests
import traceback
import pickle
import os
import json
import time
from datetime import datetime
from sklearn.linear_model import LogisticRegression
from src.config import TWITTER_CONFIG, MODEL_PATHS, API_CONFIG
from src.personality_detection import PersonalityPredictor
from src.logisticregression import LogisticRegressionClassifier

app = Flask(__name__)
CORS(app)

# Load models
try:
    with open(MODEL_PATHS['VECTORIZER'], 'rb') as f:
        tf_idf = pickle.load(f)
    print("Successfully loaded CountVectorizer")
    
    with open(MODEL_PATHS['HATE_SPEECH'], 'rb') as f:
        model = pickle.load(f)
        if not isinstance(model, LogisticRegression):
            print(f"Warning: Model type is {type(model)}")
        hate_speech_predictor = LogisticRegressionClassifier(model)
    print("Successfully loaded LogisticRegression")
    
    personality_predictor = PersonalityPredictor()
    print("Successfully initialized PersonalityPredictor")
except Exception as e:
    print(f"Error loading models: {str(e)}")
    traceback.print_exc()
    sys.exit(1)

def get_twitter_data(username):
    
    headers = {
        'Authorization': f'Bearer {TWITTER_CONFIG["BEARER_TOKEN"]}',
        'Content-Type': 'application/json'
    }

    def make_request(url, params=None, max_retries=3):
        for attempt in range(max_retries):
            try:
                response = requests.get(url, headers=headers, params=params)
                if response.status_code == 429:  # Rate limit
                    wait_time = int(response.headers.get('x-rate-limit-reset', 60))
                    print(f"Rate limit hit. Waiting {wait_time} seconds...")
                    time.sleep(min(wait_time, 15))  # Wait max 15 seconds
                    continue
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                if attempt == max_retries - 1:
                    raise
                time.sleep(2 ** attempt)  
        return None

    try:
        # Get user ID
        user_url = f'https://api.twitter.com/2/users/by/username/{username}'
        user_data = make_request(user_url)
        
        if not user_data or 'data' not in user_data:
            return None, "User not found"

        user_id = user_data['data']['id']

        # Get tweets
        tweets_url = f'https://api.twitter.com/2/users/{user_id}/tweets'
        params = {
            'max_results': 10,
            'tweet.fields': 'text',
            'exclude': 'retweets'
        }

        tweets_data = make_request(tweets_url, params)
        if not tweets_data or 'data' not in tweets_data:
            return [], "No tweets found"

        return [tweet['text'] for tweet in tweets_data['data']], None

    except Exception as e:
        return None, str(e)

@app.route("/checkuser")
def checkuser():
    try:
        username = request.args.get('username')
        print(f"Received request for username: {username}")
        
        if not username:
            return jsonify({
                "error": "Username is required",
                "tweets": [],
                "hatespeechCount": "0",
                "personality": "Error"
            }), 400

        # Get tweets
        tweets_arr_fetched, error = get_twitter_data(username)
        
        if error:
            return jsonify({
                "error": error,
                "tweets": [],
                "hatespeechCount": "0",
                "personality": "Error"
            }), 500

        if not tweets_arr_fetched or len(tweets_arr_fetched) < 3:
            return jsonify({
                "error": "Insufficient tweets",
                "message": f"User has only {len(tweets_arr_fetched) if tweets_arr_fetched else 0} tweets. Need more tweets for accurate analysis.",
                "tweets": [{"text": text, "isHateSpeech": "0"} for text in (tweets_arr_fetched or [])],
                "hatespeechCount": "0",
                "personality": "Insufficient data"
            }), 200

        
        try:
            X_test_vec_tweets = tf_idf.transform(tweets_arr_fetched)
            predictions = hate_speech_predictor.predict(X_test_vec_tweets)
            
            posts = " ||| ".join(tweets_arr_fetched)
            personality = personality_predictor.get_personality(posts)

            tweet_list = [{"text": text, "isHateSpeech": str(pred)} 
                         for text, pred in zip(tweets_arr_fetched, predictions)]
            
            return jsonify({
                "tweets": tweet_list,
                "hatespeechCount": str(np.sum(np.array(predictions)==1)),
                "personality": personality
            })
        except Exception as e:
            print(f"Error processing tweets: {str(e)}")
            traceback.print_exc()
            return jsonify({
                "error": "Error processing tweets",
                "details": str(e),
                "tweets": tweets_arr_fetched,
                "hatespeechCount": "0",
                "personality": "Error"
            }), 500

    except Exception as e:
        print(f"Server error: {str(e)}")
        traceback.print_exc()
        return jsonify({
            "error": "Server error",
            "details": str(e),
            "tweets": [],
            "hatespeechCount": "0",
            "personality": "Error"
        }), 500

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

if __name__ == '__main__':
    app.run(
        host=API_CONFIG['HOST'],
        port=API_CONFIG['PORT'],
        debug=API_CONFIG['DEBUG']
    )