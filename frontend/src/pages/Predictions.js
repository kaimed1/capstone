import {Row, Col, Form, Button} from 'react-bootstrap';


function Predictions() {
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
          <Form>
            <Form.Group>
              <Form.Label>Model</Form.Label>
              <Form.Control as="select">
                <option>Model 1</option>
                <option>Model 2</option>
                <option>Model 3</option>
              </Form.Control>
            </Form.Group>
            <Form.Group>
              <Form.Label>Home Team</Form.Label>
              <Form.Control type="text" placeholder="Enter home team" />
            </Form.Group>
            <Form.Group>
              <Form.Label>Away Team</Form.Label>
              <Form.Control type="text" placeholder="Enter away team" />
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