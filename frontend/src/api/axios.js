import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000', // URL donde corre FastAPI
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor de Petición: Adjunta el JWT automáticamente
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptor de Respuesta: Captura 401 globalmente y redirige a /login
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const isLoginEndpoint = error.config?.url?.includes('/auth/login');
    if (error.response?.status === 401 && !isLoginEndpoint) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;