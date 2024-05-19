import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import Ping from './components/Ping';
import CalculateIntake from './components/CalculateIntake';
import AnalyzeImage from './components/AnalyzeImage';
import styled from 'styled-components';

const Navbar = styled.nav`
  display: flex;
  justify-content: space-around;
  background-color: #282c34;
  padding: 20px;
`;

const NavLink = styled(Link)`
  color: white;
  text-decoration: none;
  font-size: 18px;
`;

const App = () => {
  return (
    <Router>
      <Navbar>
        <NavLink to="/">Ping</NavLink>
        <NavLink to="/calculate-intake">Calculate Intake</NavLink>
        <NavLink to="/analyze-image">Analyze Image</NavLink>
      </Navbar>
      <Routes>
        <Route path="/" element={<Ping />} />
        <Route path="/calculate-intake" element={<CalculateIntake />} />
        <Route path="/analyze-image" element={<AnalyzeImage />} />
      </Routes>
    </Router>
  );
};

export default App;
