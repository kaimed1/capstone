import football from './football.png';
import georgia from './georgia.png';
import ohio from './ohio.png';
import ou from './ou.png';
import gator from './gator.png';
import kansas from './Kansas.png';
import rabbit from './rabbits.png';
import graph from './graph.png';
import pie from './pie.png';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

import React, { useState } from 'react';

function App() {
  const [homeTeam, setHomeTeam] = useState('');
  const [awayTeam, setAwayTeam] = useState('');
  const [terminalOutput, setTerminalOutput] = useState('Fetching terminal output...');
  const [isFetching, setIsFetching] = useState(false);

  const handleInputChange = (setter) => (e) => {
    setter(e.target.value.replace(/ /g, '_'));
  };

  const fetchTerminalOutput = async () => {
    setIsFetching(true);
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/random?home=${homeTeam}&away=${awayTeam}`);
      const data = await response.json();
      setTerminalOutput(`Winner: ${data.winner_name}`);
    } catch (error) {
      setTerminalOutput('Error fetching terminal output.');
    }
    setIsFetching(false);
  };

  return (
    <div className="App">
      <header className="multicolor-background">
        <p className="header-text">NCAA Football Prediction</p>

        <div className="input-container">
          <input
            type="text"
            value={homeTeam}
            onChange={handleInputChange(setHomeTeam)}
            placeholder="Home Team"
          />
          <input
            type="text"
            value={awayTeam}
            onChange={handleInputChange(setAwayTeam)}
            placeholder="Away Team"
          />
        </div>

        <button
          onClick={fetchTerminalOutput}
          className="myButton"
          disabled={isFetching}
        >
          {isFetching ? 'Calculating...' : 'Calculate'}
        </button>

        <p>{terminalOutput}</p>

        {/* Image container with left, right, and center images */}
      <div className="logo-grid">
        <img src={football} alt="Football" className="center-football" />
      </div>
      </header>
    </div>
  );
}

export default App;
