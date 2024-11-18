import React, {useState, useEffect} from 'react';
import {Row, Col, Form, Button} from 'react-bootstrap';

function Predictions() {
  const [formData, setFormData] = useState({
    // Set default values for form data
    model: 'rf',
    homeTeam: '',
    awayTeam: ''
  });

  const [prediction, setPrediction] = useState({
    // Set default values for prediction
    winner: '',
    loser: ''
  });

  // Get model options from backend
  const [predictionMethods, setPredictionMethods] = useState([]);
  useEffect(() => {
    fetch("http://localhost:8000/api/get_prediction_methods")
      .then((response) => response.json())
      .then((data) => {
        setPredictionMethods(data.prediction_methods);
      })
      .catch((error) => console.error("Error fetching prediction methods:", error));
  }, []);

  // Get all teams from backend
  const [teams, setTeams] = useState([]);
  useEffect(() => {
    fetch("http://localhost:8000/api/get_teams")
      .then((response) => response.json())
      .then((data) => {
        setTeams(data.teams);
      })
      .catch((error) => console.error("Error fetching teams:", error));
  }, []);

  const handleChange = (e) => {
    const {name, value} = e.target;
    setFormData({...formData, [name]: value});
  }

  const handleSubmit = (e) => {
    e.preventDefault();

    // Make fetch request to backend to get prediction
    fetch(`http://localhost:8000/${formData.model}?home=${formData.homeTeam}&away=${formData.awayTeam}`, {
      method: 'GET',
    }).then((response) => response.json())
      .then((data) => {
        setPrediction(data);
      })
      .catch((error) => console.error("Error fetching prediction:", error));
  }
  
  return (
    <div className="Predictions">
      <Row>
        <Col>
          <h1>Prediction Service</h1>
        </Col>
      </Row>
      <Row>
        <Col>
          <p>Here you can get predictions for the next match of your favorite team. Select one of our various models, and then enter
            the matchup you'd like to predict! 
          </p>
        </Col>
      </Row>

      <Row>
        <Col className='col-8'>
          <Form onSubmit={handleSubmit}>
            <Form.Group controlId="model">
              <Form.Label>Model</Form.Label>
              <Form.Select name="model" value={formData.model} onChange={handleChange}>
              {predictionMethods.map((method) => (
                <option key={method.path} value={method.path}>
                  {method.name}
                </option>
              ))}
              </Form.Select>
            </Form.Group>
            <Form.Group controlId="homeTeam">
              <Form.Label>Home Team</Form.Label>
              <Form.Select name="homeTeam" value={formData.homeTeam} onChange={handleChange}>
                {teams.map((team) => (
                  <option key={team[0]} value={team[0]}>
                    {team[1]}
                  </option>
                ))}
              </Form.Select>
            </Form.Group>
            <Form.Group controlId="awayTeam">
              <Form.Label>Away Team</Form.Label>
              <Form.Select name="awayTeam" value={formData.awayTeam} onChange={handleChange}>
                  {teams.map((team) => (
                    <option key={team[0]} value={team[0]}>
                      {team[1]}
                    </option>
                  ))}
                </Form.Select>
            </Form.Group>
            <Button variant="primary" type="submit">
              Get Prediction
            </Button>
          </Form>
          <Row>
            <Col>
              <h2>Prediction</h2>
              <p>{prediction.winner} will beat {prediction.loser}</p>
            </Col>
          </Row>
        </Col>
        <Col className='col-4 d-flex justify-content-center'>
          <Row>
            <Col>
              <h2 className='text-center'>Available Models</h2>
              <ul>
                <li>Flip a Coin - a random prediction that is not based on any statistics</li>
                <li>ChatGPT Prediction - utilize ChatGPT to predict the outcome of a game</li>
                <li>Random Forest Model - A random forest model trained on season long statistics</li>
              </ul>
            </Col>
          </Row>
        </Col>
      </Row>
    </div>
  );
}

export default Predictions;