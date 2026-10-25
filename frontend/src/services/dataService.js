import api from '../api/axios.js';

// CLIENTES  //
export const getClientesService = async () => {
  const response = await api.get('/clientes/');
  return response.data;
};

export const createClienteService = async (clienteData) => {
  const response = await api.post('/clientes/', clienteData);
  return response.data;
};

// USUARIOS //
export const getUsuariosService = async () => {
  const response = await api.get('/usuarios/');
  return response.data;
};

export const createUsuarioService = async (userData) => {
  const response = await api.post('/usuarios/', userData);
  return response.data;
};

export const deleteUsuarioService = async (idUsuario) => {
  const response = await api.delete(`/usuarios/${idUsuario}`);
  return response.data;
};

// SERVICIOS //
export const getServiciosService = async () => {
  const response = await api.get('/servicios/');
  return response.data;
};

export const createServicioService = async (servicioData) => {
  const response = await api.post('/servicios/', servicioData);
  return response.data;
};

export const updateServicioService = async (idServicio, servicioData) => {
  const response = await api.put(`/servicios/${idServicio}`, servicioData);
  return response.data;
};

export const deleteServicioService = async (idServicio) => {
  const response = await api.delete(`/servicios/${idServicio}`);
  return response.data;
};

// CUOTAS //
export const getCuotasService = async () => {
  const response = await api.get('/cuotas/');
  return response.data;
};

export const createCuotaService = async (cuotaData) => {
  const response = await api.post('/cuotas/', cuotaData);
  return response.data;
};

export const deleteCuotaService = async (idCuota) => {
  const response = await api.delete(`/cuotas/${idCuota}`);
  return response.data;
};

// PAGOS //
export const getPagosService = async () => {
  const response = await api.get('/pagos/');
  return response.data;
};

export const registrarPagoService = async (pagoData) => {
  const response = await api.post('/pagos/', pagoData);
  return response.data;
};