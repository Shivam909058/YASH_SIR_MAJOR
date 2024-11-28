import React, { useState } from 'react';
import { Result } from './Components';
import './App.css';

function App() {
  const [username, setUsername] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    const newUsername = e.target.elements.username.value;
    console.log('Submitting username:', newUsername); // Debug log
    setUsername(newUsername);
    setSubmitted(true);
  };

  return (
    <div className="App">
      <div className="search-container">
        <form onSubmit={handleSubmit}>
          <input 
            type="text" 
            name="username" 
            placeholder="Enter Twitter username" 
            required
          />
          <button type="submit">Analyze</button>
        </form>
      </div>
      {submitted && username && <Result username={username} />}
    </div>
  );
}

export default App;