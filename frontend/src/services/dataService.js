import api from '../api/axios.js'

// Clientes //
export const getClientesService = async () => {
  const response = await api.get('/clientes/');
  return response.data;
};

export const createClienteService = async (clienteData) => {
  const response = await api.post('/clientes/', clienteData);
  return response.data;
};

// CUOTAS //
export const getCuotasService = async () => {
  const response = await api.get('/cuotas/');
  return response.data;
};

export const generarCuotasService = async (cuotaData) => {
  const response = await api.post('/cuotas/generar', cuotaData);
  return response.data;
};

// Usuarios //
export const getUsuariosService = async () => {
  const response = await api.get('/usuarios/');
  return response.data;
};

export const createUsuarioService = async (userData) => {
  const response = await api.post('/usuarios/', userData);
  return response.data;
};