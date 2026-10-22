import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getUsuariosService, createUsuarioService } from '../services/dataService';
import './Usuarios.css';

export const Usuarios = () => {
  const [usuarios, setUsuarios] = useState([]);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [rol, setRol] = useState('CLIENTE');
  const [error, setError] = useState('');
  const [mensaje, setMensaje] = useState('');
  const navigate = useNavigate();

  const cargarUsuarios = async () => {
    try {
      const data = await getUsuariosService();
      setUsuarios(data);
    } catch (err) {
      setError('Error al obtener la lista de usuarios');
    }
  };

  useEffect(() => {
    cargarUsuarios();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setMensaje('');

    try {
      await createUsuarioService({ email, password, rol });
      setMensaje('Usuario creado exitosamente');
      setEmail('');
      setPassword('');
      setRol('CLIENTE');
      cargarUsuarios();
    } catch (err) {
      if (err.response?.status === 403) {
        setError('No tenés permisos de ADMIN para registrar usuarios.');
      } else if (err.response?.status === 400) {
        setError('El email ya se encuentra registrado.');
      } else {
        setError('Error al crear el usuario');
      }
    }
  };

  return (
    <div className="usuarios-container">
      <button onClick={() => navigate('/dashboard')} className="btn-back">
        ← Volver al Dashboard
      </button>

      <h2>Gestión de Usuarios</h2>

      {/* Formulario de Alta por el Admin */}
      <div className="form-card">
        <h3>Registrar Nuevo Usuario</h3>
        <form onSubmit={handleSubmit} className="inline-form">
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
          <button type="submit">Guardar Usuario</button>
        </form>
        {mensaje && <p className="mensaje-exito">{mensaje}</p>}
        {error && <p className="mensaje-error">{error}</p>}
      </div>

      {/* Tabla de Listado */}
      <h3>Listado de Usuarios</h3>
      <table className="tabla-clientes">
        <thead>
          <tr>
            <th>ID</th>
            <th>Email</th>
            <th>Rol</th>
            <th>Estado</th>
          </tr>
        </thead>
        <tbody>
          {usuarios.map((u) => (
            <tr key={u.id || u.id_usuario}>
              <td>{u.id || u.id_usuario}</td>
              <td>{u.email}</td>
              <td>{u.rol}</td>
              <td>{u.activo ? 'Activo' : 'Inactivo'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};