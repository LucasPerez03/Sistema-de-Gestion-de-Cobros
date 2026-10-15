import api from '../api/axios';

export const loginService = async (email, password) => {
  const response = await api.post('/auth/login', { email, password });
  if (response.data.access_token) {
    // Guarda el token para mantener la sesión abierta
    localStorage.setItem('token', response.data.access_token);
  }
  return response.data;
};

export const getPerfilService = async () => {
  const response = await api.get('/auth/me');
  return response.data;
};

export const logoutService = () => {
  localStorage.removeItem('token');
};