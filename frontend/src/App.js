import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import NavBar from './components/NavBar';

function App() {
  return (
    <Router>
    <NavBar /> {/* Navbar is outside Routes so it appears on all pages */}
    <Routes>
      <Route path="/" element={<h1>home</h1>} />
      <Route path="/predictions" element={<h1>predictions</h1>} />
    </Routes>
  </Router>
  );
}

//Exports the app to a server running locally
export default App;
