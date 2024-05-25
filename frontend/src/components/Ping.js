import React, { useState } from 'react';
import { PacmanLoader } from 'react-spinners';
import axiosInstance from '../axiosConfig';

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
    <div className="flex flex-col items-center mt-12">
      <h1 className="text-2xl font-bold">Ping Endpoint</h1>
      <button 
        className="mt-5 px-6 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600"
        onClick={handlePing}
      >
        Ping
      </button>
      {loading ? (
        <div className="mt-5">
          <PacmanLoader color={"#4CAF50"} loading={loading} />
        </div>
      ) : (
        message && <p className="mt-5">{message}</p>
      )}
    </div>
  );
};

export default Ping;
