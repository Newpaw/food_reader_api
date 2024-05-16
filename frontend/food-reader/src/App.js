import React, { useState, useEffect } from 'react';
import api from './api';

const App = () => {
  const [transactions, setTransactions] = useState([]);
  const [formData, setFormData] = useState({
    height_cm: '',
    weight_kg: '',
    age: '',
    gender: '',
    activity_level: '',
  });

  const fetchTransactions = async () => {
    try {
      const response = await api.get('/calculate-intake');
      setTransactions(response.data);
    } catch (error) {
      console.error('Error fetching transactions:', error);
    }
  };

  useEffect(() => {
    fetchTransactions();
  }, []);

  const handleFormSubmit = async (event) => {
    event.preventDefault();
    try {
      await api.post('/calculate-intake', formData); // Ensure you send formData with the post request
      fetchTransactions();
      setFormData({
        height_cm: '',
        weight_kg: '',
        age: '',
        gender: '',
        activity_level: '',
      });
    } catch (error) {
      console.error('Error submitting form:', error);
    }
  };

  return (
    <div>
      <nav className='navbar navbar-dark bg-primary'>
        <div className='container-fluid'>
          <a className='navbar-brand' href='#'>
            BMI Calculator
          </a>
        </div>
      </nav>
      <div className="container mt-4">
        <form onSubmit={handleFormSubmit}>
          <div className="mb-3">
            <label htmlFor="height_cm" className="form-label">Height (cm)</label>
            <input
              type="text"
              className="form-control"
              id="height_cm"
              value={formData.height_cm}
              onChange={(e) => setFormData({ ...formData, height_cm: e.target.value })}
            />
          </div>
          <div className="mb-3">
            <label htmlFor="weight_kg" className="form-label">Weight (kg)</label>
            <input
              type="text"
              className="form-control"
              id="weight_kg"
              value={formData.weight_kg}
              onChange={(e) => setFormData({ ...formData, weight_kg: e.target.value })}
            />
          </div>
          <div className="mb-3">
            <label htmlFor="age" className="form-label">Age</label>
            <input
              type="text"
              className="form-control"
              id="age"
              value={formData.age}
              onChange={(e) => setFormData({ ...formData, age: e.target.value })}
            />
          </div>
          <div className="mb-3">
            <label htmlFor="gender" className="form-label">Gender</label>
            <input
              type="text"
              className="form-control"
              id="gender"
              value={formData.gender}
              onChange={(e) => setFormData({ ...formData, gender: e.target.value })}
            />
          </div>
          <div className="mb-3">
            <label htmlFor="activity_level" className="form-label">Activity Level</label>
            <input
              type="text"
              className="form-control"
              id="activity_level"
              value={formData.activity_level}
              onChange={(e) => setFormData({ ...formData, activity_level: e.target.value })}
            />
          </div>
          <button type="submit" className="btn btn-primary">Calculate</button>
        </form>
        <h2 className="mt-4">Transactions</h2>
        <ul className="list-group">
          {transactions.map((transaction, index) => (
            <li key={index} className="list-group-item">
              {JSON.stringify(transaction)}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default App;
