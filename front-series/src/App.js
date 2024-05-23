import React from 'react';
import { BrowserRouter as Router, Routes, Route, NavLink } from 'react-router-dom'; // Actualización aquí
import Nav from 'react-bootstrap/Nav';
import './App.css';
import Home from './Home';
import IndividualSearch from './IndividualSearch';
import DualSearch from './DualSearch';

function App() {
  return (
    <Router>
      <div className="App">
        <FillExample />
        <div className="container">
          <Routes> {/* Usamos Routes en lugar de Switch */}
            <Route path="/" element={<Home />} />
            <Route path="/individual" element={<IndividualSearch />} />
            <Route path="/dual" element={<DualSearch />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

function FillExample() {
  return (
    <Nav fill variant="tabs" defaultActiveKey="/">
      <Nav.Item>
        <Nav.Link as={NavLink} to="/" end className="nav-link-custom">
          Principal
        </Nav.Link>
      </Nav.Item>
      <Nav.Item>
        <Nav.Link as={NavLink} to="/individual" className="nav-link-custom">
          Búsquedas Individuales
        </Nav.Link>
      </Nav.Item>
      <Nav.Item>
        <Nav.Link as={NavLink} to="/dual" className="nav-link-custom">
          Búsquedas Duales
        </Nav.Link>
      </Nav.Item>
    </Nav>
  );
}

export default App;
