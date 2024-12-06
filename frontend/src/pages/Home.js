import { Row, Col } from 'react-bootstrap';

function Home() {
    return (
        <div className="Home">
        <Row>
            <Col>
            <h1>Home</h1>
            </Col>
        </Row>
        <Row>
            <Col>
            <p>Welcome to the Sports Prediction Service! Here you can get predictions for the next match of your favorite team. Select one of our various models, and then enter the matchup you'd like to predict! 
            </p>
            </Col>
        </Row>
        </div>
    );
}

export default Home;