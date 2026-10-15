import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000', // URL donde corre Uvicorn (FastAPI)
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor: Adjunta el JWT automáticamente si el usuario inició sesión
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;