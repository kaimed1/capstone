import football from './football.png';
import georgia from './georgia.png';
import ohio from './ohio.png';
import ou from './ou.png';
import gator from './gator.png'
import kansas from './Kansas.png'
import rabbit from './rabbits.png'
import graph from './graph.png'
import pie from './pie.png'
import './App.css';

import React, {useState} from 'react';

function App() {
  //Creates the input places for the user
  const [homeTeam, setHomeTeam]= useState('');
  const [awayTeam, setAwayTeam] = useState('');

  //handles input from user in each box
  const handleInputChargeHome = (e) => {setHomeTeam(e.target.value.replace(/ /g, '_'))};
  const handleInputChargeAway = (e) => {setAwayTeam(e.target.value.replace(/ /g, '_'))};
  //Outputs the the user the terminal output
  const [terminalOutput, setTerminalOutput] = useState("Fetching terminal output...");

  //if the terminal is not fetching set the state to false
  const [isFetching, setIsFetching] = useState(false);

  //This is the function that fetches the terminal output from the server with the 
  //get request to the API,
  const fetchTerminalOutput = async () => {
    setIsFetching(true);

    //Waits fo the response of the server with the winning team
    try {
      const response = await fetch('http://127.0.0.1:8000/api/random?home=${homeTeam}&away=${awayTeam}');
      
      const data = await response.json();

      setTerminalOutput(`Winner: ${data.winner_name}`);

    } catch (error) {
      setTerminalOutput("Error fetching terminal output.");
    }
    setIsFetching(false);
  };

  //This runs all the pictures and the website text and styling 
  return (
    <div className="App">
      <header className="multicolor-background">
      <p className = "header-text">
      NCAA Football Prediction
      </p>
      <button 
        onClick={fetchTerminalOutput} 
        style={{
          padding: "10px 20px",
          backgroundColor: isFetching ? "#888" : "#4CAF50",
          color: "white",
          border: "none",
          borderRadius: "5px",
          cursor: "pointer",
          marginTop: "495px",
        }}
        disabled={isFetching}
      >
      
        {isFetching ? "Calculating..." : "Calculate"}
      </button>

      <p>{terminalOutput}</p>

      <div class="hollow-circle"></div>
      <img src={football} alt="logo" class = 'center-image' />
      <img src={georgia} alt="Left Image" class="left-image"></img>
      <img src={ohio} alt="Left Image" class="left-image-second"></img>
      <img src={ou} alt="Left Image" class="left-image-last"></img>
      <img src={gator} alt="Right Image" class="right-image"></img>
      <img src={kansas} alt="Right Image" class="right-image-second"></img>
      <img src={rabbit} alt="Right Image" class="right-image-last"></img>
      <img src = {graph} alt = "graph" class = "graph-image"></img>
      <img src = {pie} alt = "pie" class = "piechart-image"></img>

      
      <input type = "text" id ="textbox" class = 'textbox' value = {homeTeam} onChange = {handleInputChargeHome} placeholder= "Home Team"/>
      <input type = "text" id ="textbox" class = 'second-textbox' value = {awayTeam} onChange = {handleInputChargeAway} placeholder = "Away Team"/>

      </header>
    </div>
  );
}

//Exports the app to a server running locally
export default App;
