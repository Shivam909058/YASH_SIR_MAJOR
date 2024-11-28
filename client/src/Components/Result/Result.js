import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Result.css';
import { API_URL } from '../../config';

const Result = ({ username }) => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [data, setData] = useState(null);

  const getTwitterAnalysis = async (username) => {
    console.log('Fetching data for username:', username); // Debug log
    try {
      const response = await axios.get(`${API_URL}/checkuser`, {
        params: {
          username: username,
          tweets: true,
          retweets: false
        }
      });
      console.log('API Response:', response.data); // Debug log
      return response.data;
    } catch (error) {
      console.error('API Error:', error); // Debug log
      if (error.response && error.response.status === 429) {
        throw new Error("Rate limit exceeded. Please try again in a few minutes.");
      } else if (error.response && error.response.status === 404) {
        throw new Error("User not found. Please check the username and try again.");
      } else if (error.response && error.response.status === 500) {
        throw new Error("Server error. Please try again later.");
      }
      throw error;
    }
  };

  useEffect(() => {
    console.log('Username in useEffect:', username); // Debug log
    const fetchData = async () => {
      if (!username) {
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        setError(null);
        const result = await getTwitterAnalysis(username);
        setData(result);
      } catch (error) {
        console.error('Error in fetchData:', error); // Debug log
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [username]);

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Analyzing Twitter data for @{username}...</p>
      </div>
    );
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  if (!data) {
    return <div className="no-data">No data available</div>;
  }

  return (
    <div className="result-container">
      <div className="stats-section">
        <h2>Analysis Results for @{username}</h2>
        <div className="stat-item">
          <label>Hate Speech Count:</label>
          <span>{data.hatespeechCount}</span>
        </div>
        <div className="stat-item">
          <label>Personality Type:</label>
          <span>{data.personality}</span>
        </div>
      </div>

      <div className="tweets-section">
        <h3>Analyzed Tweets</h3>
        {data.tweets && data.tweets.length > 0 ? (
          data.tweets.map((tweet, index) => (
            <div 
              key={index} 
              className={`tweet-item ${tweet.isHateSpeech === "1" ? "hate-speech" : ""}`}
            >
              <p>{tweet.text}</p>
              {tweet.isHateSpeech === "1" && (
                <span className="hate-speech-tag">Hate Speech Detected</span>
              )}
            </div>
          ))
        ) : (
          <p>No tweets found</p>
        )}
      </div>
    </div>
  );
};

export default Result;