import React, { useState } from 'react';
import styled from 'styled-components';
import { ClipLoader } from 'react-spinners';
import axiosInstance from '../axiosConfig';

const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 50px;
`;

const Button = styled.button`
  padding: 10px 20px;
  margin-top: 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
`;

const Ping = () => {
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const handlePing = async () => {
    setLoading(true);
    try {
      const response = await axiosInstance.get('/api/ping');
      setMessage(response.data.message);
    } catch (error) {
      setMessage('Error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container>
      <h1>Ping Endpoint</h1>
      <Button onClick={handlePing}>Ping</Button>
      {loading ? (
        <ClipLoader size={50} color={"#4CAF50"} loading={loading} />
      ) : (
        message && <p>{message}</p>
      )}
    </Container>
  );
};

export default Ping;
