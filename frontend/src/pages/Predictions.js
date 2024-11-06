import React, {useState} from 'react';
import {Row, Col, Form, Button} from 'react-bootstrap';

function Predictions() {
  const [formData, setFormData] = useState({
    // Set default values for form data
    model: 'rf',
    homeTeam: '',
    awayTeam: ''
  });

  const handleChange = (e) => {
    const {name, value} = e.target;
    setFormData({...formData, [name]: value});
  }

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log(formData);

    // TODO: Make API call to get prediction
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
                <option value="model1">Model 1</option>
                <option value="model2">Model 2</option>
                <option value="model3">Model 3</option>
              </Form.Select>
            </Form.Group>
            <Form.Group controlId="homeTeam">
              <Form.Label>Home Team</Form.Label>
              <Form.Control type="text" placeholder="Enter home team" name="homeTeam" value={formData.name} onChange={handleChange}/>
            </Form.Group>
            <Form.Group controlId="awayTeam">
              <Form.Label>Away Team</Form.Label>
              <Form.Control type="text" placeholder="Enter away team" name="awayTeam" vaue={formData.name} onChange={handleChange}/>
            </Form.Group>
            <Button variant="primary" type="submit">
              Get Prediction
            </Button>
          </Form>
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