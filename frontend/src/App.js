import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

// Import Bootstrap Components
import Container from 'react-bootstrap/Container';

// Import Components
import NavBar from './components/NavBar';

// Import Pages
import Home from './pages/Home';
import Predictions from './pages/Predictions';
import Rankings from './pages/Rankings';

function App() {
  return (
    <Router>
    <NavBar /> {/* Navbar is outside Routes so it appears on all pages */}
    <Container>
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/predictions" element={<Predictions />} />
      <Route path="/rankings" element={<Rankings />} />
      <Route path="*" element={<h1>Page not found!</h1>} />
    </Routes>
    </Container>
  </Router>
  );
}

//Exports the app to a server running locally
export default App;
