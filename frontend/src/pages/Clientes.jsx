import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getClientesService, createClienteService } from '../services/dataService';
import './Clientes.css';

export const Clientes = () => {
  const [clientes, setClientes] = useState([]);
  const [nombre, setNombre] = useState('');
  const [apellido, setApellido] = useState('');
  const [dni, setDni] = useState('');
  const [email, setEmail] = useState('');
  const [telefono, setTelefono] = useState('');
  const [fechaNacimiento, setFechaNacimiento] = useState('');
  const [error, setError] = useState('');
  const [mensaje, setMensaje] = useState('');
  const navigate = useNavigate();

  const cargarClientes = async () => {
    try {
      const data = await getClientesService();
      setClientes(data);
    } catch (err) {
      setError('Error al obtener la lista de clientes');
    }
  };

  useEffect(() => {
    cargarClientes();
  }, []);

  const handleSubmit = async (e) => {
  e.preventDefault();
  setError('');
  setMensaje('');

  try {
    await createClienteService({ 
      nombre, 
      apellido, 
      dni, 
      email, 
      telefono,
      fecha_nacimiento: fechaNacimiento 
    });

    setMensaje('Cliente creado exitosamente');
    setNombre('');
    setApellido('');
    setDni('');
    setEmail('');
    setTelefono('');
    setFechaNacimiento('');
    cargarClientes();
  } catch (err) {
    if (err.response?.status === 403) {
      setError('No tenés permisos de ADMIN para crear clientes.');
    } else if (err.response?.status === 422) {
      setError('Faltan campos obligatorios o el formato es incorrecto.');
    } else {
      setError('Error al crear el cliente');
    }
  }
};

  return (
    <div className="clientes-container">
      <button onClick={() => navigate('/dashboard')} className="btn-back">
        ← Volver al Dashboard
      </button>

      <h2>Gestión de Clientes</h2>

      {/* Formulario de Alta */}
      <div className="form-card">
        <h3>Registrar Nuevo Cliente</h3>
        <form onSubmit={handleSubmit} className="inline-form">
          <input
            type="text"
            placeholder="Nombre"
            value={nombre}
            onChange={(e) => setNombre(e.target.value)}
            required
          />
          <input
            type="text"
            placeholder="Apellido"
            value={apellido}
            onChange={(e) => setApellido(e.target.value)}
            required
          />
          <input
            type="text"
            placeholder="DNI"
            value={dni}
            onChange={(e) => setDni(e.target.value)}
            required
          />
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <input
            type="text"
            placeholder="Telefono"
            value={telefono}
            onChange={(e) => setTelefono(e.target.value)}
            required
          />
          <input
            type="date"
            value={fechaNacimiento}
            onChange={(e) => setFechaNacimiento(e.target.value)}
            required
          />
          <button type="submit">Guardar Cliente</button>
        </form>
        {mensaje && <p className="mensaje-exito">{mensaje}</p>}
        {error && <p className="mensaje-error">{error}</p>}
      </div>

      {/* Tabla de Listado */}
      <h3>Listado de Clientes</h3>
      <table className="tabla-clientes">
        <thead>
          <tr>
            <th>ID</th>
            <th>Nombre</th>
            <th>Apellido</th>
            <th>DNI</th>
            <th>Email</th>
            <th>Teléfono</th>
          </tr>
        </thead>
        <tbody>
          {clientes.map((c) => (
            <tr key={c.id || c.id_cliente}>
              <td>{c.id || c.id_cliente}</td>
              <td>{c.nombre}</td>
              <td>{c.apellido}</td>
              <td>{c.dni}</td>
              <td>{c.email}</td>
              <td>{c.telefono}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};