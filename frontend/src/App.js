import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

// Import Bootstrap Components
import Container from 'react-bootstrap/Container';

// Import Components
import NavBar from './components/NavBar';

// Import Pages
import Predictions from './pages/Predictions';

function App() {
  return (
    <Router>
    <NavBar /> {/* Navbar is outside Routes so it appears on all pages */}
    <Container>
    <Routes>
      <Route path="/" element={<h1>home</h1>} />
      <Route path="/predictions" element={<Predictions />} />
    </Routes>
    </Container>
  </Router>
  );
}

//Exports the app to a server running locally
export default App;
