import football from './football.png';
import georgia from './georgia.png';
import ohio from './ohio.png';
import alabama from './Alabama.png';
import './App.css';
import React, {useState} from 'react';


function App() {
  const [inputValue, setInputValue]= useState('');
  const handleInputCharge = (e) => {setInputValue(e.target.value)};

  return (
    <div className="App">
  
      <header className="multicolor-background">
      <p className = "header-text">
      NCAA Football Prediction
      </p>

      <div class="hollow-circle"></div>
      <img src={football} alt="logo" class = 'center-image' />
      <img src={georgia} alt="Left Image" class="left-image"></img>
      <img src={ohio} alt="Left Image" class="left-image-second"></img>
      <img src={alabama} alt="Left Image" class="left-image-last"></img>
  
      <input type = "text" id ="textbox" class = 'textbox' value = {inputValue} onChange = {handleInputCharge} placeholder = "Team 1"/>
      <input type = "text" id ="textbox" class = 'second-textbox' value = {inputValue} onChange = {handleInputCharge} placeholder = "Team 2"/>
      
      </header>
    </div>
  );
}

export default App;
