import axios from 'axios';

// Log the environment variable to debug
console.log('REACT_APP_BACKEND_URL:', process.env.REACT_APP_BACKEND_URL);

// Create an instance of axios with the base URL set to the environment variable
const axiosInstance = axios.create({
  baseURL: process.env.REACT_APP_BACKEND_URL
});

export default axiosInstance;
