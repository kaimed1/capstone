import football from './football.png';
import georgia from './georgia.png';
import ohio from './ohio.png';
import ou from './ou.png';
import gator from './gator.png'
import kansas from './Kansas.png'
import rabbit from './rabbits.png'
import './App.css';
import React, {useState} from 'react';


function App() {
  const [inputValue, setInputValue]= useState('');
  const handleInputCharge = (e) => {setInputValue(e.target.value)};

  const [terminalOutput, setTerminalOutput] = useState("Fetching terminal output...");
  const [isFetching, setIsFetching] = useState(false);

  const fetchTerminalOutput = async () => {
    setIsFetching(true);

    try {
      const response = await fetch('http://localhost:5000/terminal-output');
      const data = await response.json();
      setTerminalOutput(data.output);
    } catch (error) {
      setTerminalOutput("Error fetching terminal output.");
    }
    setIsFetching(false);
  };

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
        {isFetching ? "Fetching..." : "Calculate"}
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

      <input type = "text" id ="textbox" class = 'textbox' value = {inputValue} onChange = {handleInputCharge} placeholder = "Team 1"/>
      <input type = "text" id ="textbox" class = 'second-textbox' value = {inputValue} onChange = {handleInputCharge} placeholder = "Team 2"/>

      </header>
    </div>
  );
}

export default App;
