import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';

    function Home() {
      const styles = {
        // Full screen container
        container: {
          height: '100vh',
          display: 'flex',
        },
        // Left section (black background) with centered text
        leftSection: {
          backgroundColor: 'black',
          color: 'white',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          flex: 1,
          textAlign: 'center',
        },
        // Right section (white background) with centered text
        rightSection: {
          backgroundColor: 'white',
          color: 'black',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          flex: 1,
          textAlign: 'center',
        },
      };
    
      return (
        /*Will fit window to size of users screen*/
        <Container fluid style={styles.container}>
          {/* Left Section (this is the black background) */}
          <Row style={{ flex: 1 }}>
            <Col style={styles.leftSection}>
              <div>
                <h1>How To Use</h1>
              </div>
            </Col>
    
            {/* Right Section (this is the black white Background) */}
            <Col style={styles.rightSection}>
              <div>
                <p>
                  Navigate to the Predictions page and input the home team and the away team. Select a prediction model
                  from the dropdown menu and press "Get Prediction" to see the winning team. The Rankings tab has the teams rankings 
                  based on the analysis of all the data derived from various websites.
                </p>
              </div>
            </Col>
          </Row>
        </Container>
      );
    }
    
    export default Predictions;
    