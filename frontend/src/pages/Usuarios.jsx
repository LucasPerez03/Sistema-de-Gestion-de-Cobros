import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  getUsuariosService,
  createUsuarioService,
  getClientesService,
} from '../services/dataService';
import './Usuarios.css';

export const Usuarios = () => {
  const [usuarios, setUsuarios] = useState([]);
  const [clientes, setClientes] = useState([]);
  const [nombre, setNombre] = useState('');
  const [apellido, setApellido] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [rol, setRol] = useState('CLIENTE');
  const [idCliente, setIdCliente] = useState('');
  const [error, setError] = useState('');
  const [mensaje, setMensaje] = useState('');
  const navigate = useNavigate();

  const cargarDatos = async () => {
    try {
      const [usuariosData, clientesData] = await Promise.all([
        getUsuariosService(),
        getClientesService(),
      ]);
      setUsuarios(usuariosData);
      setClientes(clientesData);
    } catch (err) {
      if (err.response?.status === 403) {
        setError('Acceso denegado: Se requiere rol de Administrador.');
      } else {
        setError('Error al obtener la lista de usuarios.');
      }
    }
  };

  useEffect(() => {
    cargarDatos();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setMensaje('');

    const payload = {
      nombre,
      apellido,
      email,
      password,
      rol,
      id_cliente: rol === 'CLIENTE' && idCliente ? Number(idCliente) : null,
    };

    try {
      await createUsuarioService(payload);
      setMensaje('Usuario creado exitosamente');
      setNombre('');
      setApellido('');
      setEmail('');
      setPassword('');
      setRol('CLIENTE');
      setIdCliente('');
      cargarDatos();
    } catch (err) {
      if (err.response?.status === 403) {
        setError('No tenés permisos de ADMIN para registrar usuarios.');
      } else if (err.response?.status === 400) {
        setError(err.response?.data?.detail || 'El email ya se encuentra registrado.');
      } else if (err.response?.status === 422) {
        setError('Datos inválidos. Verificá los campos ingresados.');
      } else {
        setError('Error al crear el usuario.');
      }
    }
  };

  return (
    <div className="usuarios-container">
      <button onClick={() => navigate('/dashboard')} className="btn-back">
        ← Volver al Dashboard
      </button>

      <h2>Gestión de Usuarios</h2>

      <div className="form-card">
        <h3>Registrar Nuevo Usuario</h3>
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
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Contraseña"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <select value={rol} onChange={(e) => setRol(e.target.value)}>
            <option value="CLIENTE">Cliente</option>
            <option value="ENTRENADOR">Entrenador</option>
            <option value="ADMIN">Administrador</option>
          </select>

          {rol === 'CLIENTE' && (
            <select
              value={idCliente}
              onChange={(e) => setIdCliente(e.target.value)}
            >
              <option value="">-- Vincular con Cliente (Opcional) --</option>
              {clientes.map((c) => (
                <option key={c.id_cliente} value={c.id_cliente}>
                  {c.nombre} {c.apellido} (DNI: {c.dni})
                </option>
              ))}
            </select>
          )}

          <button type="submit">Guardar Usuario</button>
        </form>
        {mensaje && <p className="mensaje-exito">{mensaje}</p>}
        {error && <p className="mensaje-error">{error}</p>}
      </div>

      <h3>Listado de Usuarios</h3>
      <table className="tabla-clientes">
        <thead>
          <tr>
            <th>ID</th>
            <th>Nombre Completo</th>
            <th>Email</th>
            <th>Rol</th>
            <th>ID Cliente</th>
            <th>Estado</th>
          </tr>
        </thead>
        <tbody>
          {usuarios.map((u) => (
            <tr key={u.id_usuario}>
              <td>{u.id_usuario}</td>
              <td>{u.nombre} {u.apellido}</td>
              <td>{u.email}</td>
              <td>{u.rol}</td>
              <td>{u.id_cliente || '-'}</td>
              <td>{u.estado ? 'Activo' : 'Inactivo'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};