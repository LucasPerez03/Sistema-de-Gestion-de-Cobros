import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  getClientesService,
  createClienteService,
  updateClienteService,
} from '../../services/dataService';
import { getPerfilService } from '../../services/authService';
import './Clientes.css';

export const Clientes = () => {
  const [clientes, setClientes] = useState([]);
  const [rol, setRol] = useState('');
  const [nombre, setNombre] = useState('');
  const [apellido, setApellido] = useState('');
  const [dni, setDni] = useState('');
  const [email, setEmail] = useState('');
  const [telefono, setTelefono] = useState('');
  const [fechaNacimiento, setFechaNacimiento] = useState('');
  const [clienteEditando, setClienteEditando] = useState(null);
  const [error, setError] = useState('');
  const [mensaje, setMensaje] = useState('');
  const navigate = useNavigate();

  const cargarClientes = async () => {
    try {
      const [perfil, data] = await Promise.all([
        getPerfilService(),
        getClientesService(),
      ]);
      setRol(perfil.rol);
      setClientes(data);
    } catch {
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
      const datosCliente = {
        nombre,
        apellido,
        dni,
        email,
        telefono,
        fecha_nacimiento: fechaNacimiento,
      };

      if (clienteEditando) {
        await updateClienteService(clienteEditando.id_cliente, datosCliente);
        setMensaje('Cliente actualizado exitosamente.');
      } else {
        await createClienteService(datosCliente);
        setMensaje('Cliente creado exitosamente.');
      }

      limpiarFormulario();
      await cargarClientes();
    } catch (err) {
      if (err.response?.status === 403) {
        setError('No tenés permisos de ADMIN para guardar clientes.');
      } else if (err.response?.status === 409) {
        setError(
          err.response?.data?.detail || 'Ya existe un cliente con ese DNI.'
        );
      } else if (err.response?.status === 422) {
        setError('Faltan campos obligatorios o el formato es incorrecto.');
      } else {
        setError(
          clienteEditando
            ? 'Error al actualizar el cliente.'
            : 'Error al crear el cliente.'
        );
      }
    }
  };

  const limpiarFormulario = () => {
    setNombre('');
    setApellido('');
    setDni('');
    setEmail('');
    setTelefono('');
    setFechaNacimiento('');
    setClienteEditando(null);
  };

  const editarCliente = (cliente) => {
    setError('');
    setMensaje('');
    setClienteEditando(cliente);
    setNombre(cliente.nombre);
    setApellido(cliente.apellido);
    setDni(cliente.dni);
    setEmail(cliente.email);
    setTelefono(cliente.telefono);
    setFechaNacimiento(cliente.fecha_nacimiento);
  };

  const toggleEstadoCliente = async (cliente) => {
    if (
      cliente.estado &&
      !window.confirm(
        `¿Confirmás la desactivación de ${cliente.nombre} ${cliente.apellido}?`
      )
    ) {
      return;
    }

    setError('');
    setMensaje('');
    try {
      await updateClienteService(cliente.id_cliente, {
        estado: !cliente.estado,
      });
      setMensaje(
        `Cliente ${cliente.estado ? 'desactivado' : 'activado'} exitosamente.`
      );
      await cargarClientes();
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          'No se pudo actualizar el estado del cliente.'
      );
    }
  };

  return (
    <div className="clientes-container">
      <button onClick={() => navigate('/dashboard')} className="btn-back">
        ← Volver al Dashboard
      </button>

      <h2>Gestión de Clientes</h2>

      {/* Formulario de Alta */}
      {rol === 'ADMIN' && (
        <div className="form-card">
          <h3>
            {clienteEditando ? 'Editar Cliente' : 'Registrar Nuevo Cliente'}
          </h3>
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
            <button type="submit">
              {clienteEditando ? 'Guardar Cambios' : 'Guardar Cliente'}
            </button>
            {clienteEditando && (
              <button
                type="button"
                className="btn-cancel"
                onClick={limpiarFormulario}
              >
                Cancelar Edición
              </button>
            )}
          </form>
          {mensaje && <p className="mensaje-exito">{mensaje}</p>}
          {error && <p className="mensaje-error">{error}</p>}
        </div>
      )}

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
            <th>Estado</th>
            {rol === 'ADMIN' && <th>Acciones</th>}
          </tr>
        </thead>
        <tbody>
          {clientes.map((c) => (
            <tr key={c.id_cliente}>
              <td>{c.id_cliente}</td>
              <td>{c.nombre}</td>
              <td>{c.apellido}</td>
              <td>{c.dni}</td>
              <td>{c.email}</td>
              <td>{c.telefono}</td>
              <td>{c.estado ? 'Activo' : 'Inactivo'}</td>
              {rol === 'ADMIN' && (
                <td>
                  <button
                    type="button"
                    className="btn-toggle"
                    onClick={() => editarCliente(c)}
                  >
                    Editar
                  </button>{' '}
                  <button
                    type="button"
                    className={c.estado ? 'btn-danger' : 'btn-toggle'}
                    onClick={() => toggleEstadoCliente(c)}
                  >
                    {c.estado ? 'Desactivar' : 'Activar'}
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