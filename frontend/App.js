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
