import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  getServiciosService,
  createServicioService,
  updateServicioService,
} from '../services/dataService';
import { getPerfilService } from '../services/authService';
import './Servicios.css';

export const Servicios = () => {
  const [servicios, setServicios] = useState([]);
  const [rol, setRol] = useState('');
  const [nombre, setNombre] = useState('');
  const [precio, setPrecio] = useState('');
  const [descripcion, setDescripcion] = useState('');
  const [error, setError] = useState('');
  const [mensaje, setMensaje] = useState('');
  const navigate = useNavigate();

  const cargarDatos = async () => {
    try {
      const [perfilData, serviciosData] = await Promise.all([
        getPerfilService(),
        getServiciosService(),
      ]);
      setRol(perfilData.rol);
      setServicios(serviciosData);
    } catch (err) {
      setError('Error al obtener los servicios.');
    }
  };

  useEffect(() => {
    cargarDatos();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setMensaje('');

    try {
      await createServicioService({
        nombre,
        precio: Number(precio),
        descripcion,
      });
      setMensaje('Servicio registrado exitosamente.');
      setNombre('');
      setPrecio('');
      setDescripcion('');
      cargarDatos();
    } catch (err) {
      if (err.response?.status === 403) {
        setError('Solo el rol ADMIN puede dar de alta servicios.');
      } else if (err.response?.status === 422) {
        setError('Verificá que el precio sea mayor a 0 y los campos sean válidos.');
      } else {
        setError('Error al crear el servicio.');
      }
    }
  };

  const toggleEstadoServicio = async (servicio) => {
    setError('');
    setMensaje('');
    try {
      await updateServicioService(servicio.id_servicio, {
        estado: !servicio.estado,
      });
      setMensaje(`Estado de "${servicio.nombre}" actualizado.`);
      cargarDatos();
    } catch (err) {
      setError('No se pudo actualizar el estado del servicio.');
    }
  };

  return (
    <div className="servicios-container">
      <button onClick={() => navigate('/dashboard')} className="btn-back">
        ← Volver al Dashboard
      </button>

      <h2>Gestión de Servicios / Planes</h2>

      {rol === 'ADMIN' && (
        <div className="form-card">
          <h3>Registrar Nuevo Plan de Entrenamiento</h3>
          <form onSubmit={handleSubmit} className="inline-form">
            <input
              type="text"
              placeholder="Nombre del Plan (ej. 3 veces por semana)"
              value={nombre}
              onChange={(e) => setNombre(e.target.value)}
              required
            />
            <input
              type="number"
              step="0.01"
              min="1"
              placeholder="Precio Base ($)"
              value={precio}
              onChange={(e) => setPrecio(e.target.value)}
              required
            />
            <input
              type="text"
              placeholder="Descripción"
              value={descripcion}
              onChange={(e) => setDescripcion(e.target.value)}
            />
            <button type="submit">Guardar Plan</button>
          </form>
          {mensaje && <p className="mensaje-exito">{mensaje}</p>}
          {error && <p className="mensaje-error">{error}</p>}
        </div>
      )}

      <h3>Planes Disponibles</h3>
      <table className="tabla-clientes">
        <thead>
          <tr>
            <th>ID</th>
            <th>Nombre del Plan</th>
            <th>Precio Base</th>
            <th>Descripción</th>
            <th>Estado</th>
            {rol === 'ADMIN' && <th>Acción</th>}
          </tr>
        </thead>
        <tbody>
          {servicios.map((s) => (
            <tr key={s.id_servicio}>
              <td>{s.id_servicio}</td>
              <td>{s.nombre}</td>
              <td>${Number(s.precio).toFixed(2)}</td>
              <td>{s.descripcion || '-'}</td>
              <td>{s.estado ? 'Activo' : 'Inactivo'}</td>
              {rol === 'ADMIN' && (
                <td>
                  <button
                    type="button"
                    onClick={() => toggleEstadoServicio(s)}
                    className="btn-toggle"
                  >
                    {s.estado ? 'Desactivar' : 'Activar'}
                  </button>
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};