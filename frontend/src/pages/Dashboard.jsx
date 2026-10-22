import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getPerfilService, logoutService } from '../services/authService';
import './Dashboard.css';

export const Dashboard = () => {
  const [usuario, setUsuario] = useState(null);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchPerfil = async () => {
      try {
        const data = await getPerfilService();
        setUsuario(data);
      } catch (err) {
        setError('Sesión expirada o no autorizada');
        logoutService();
        navigate('/login');
      }
    };

    fetchPerfil();
  }, [navigate]);

  const handleLogout = () => {
    logoutService();
    navigate('/login');
  };

  if (error) return <p className="mensaje-error">{error}</p>;
  if (!usuario) return <p>Cargando datos del usuario...</p>;

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>BYPay - Panel Principal</h1>
        <button onClick={handleLogout} className="btn-logout">
          Cerrar Sesión
        </button>
      </header>

      <div className="user-card">
        <h3>Bienvenido/a, {usuario.nombre || usuario.email}</h3>
        <p><strong>Email:</strong> {usuario.email}</p>
        <p><strong>Rol:</strong> {usuario.rol}</p>
      </div>

      <nav>
        <ul className="nav-list">
          <li className="nav-item" onClick={() => navigate('/clientes')}>
            Gestión de Clientes
          </li>
          {usuario.rol === 'ADMIN' && (
            <li className="nav-item" onClick={() => navigate('/usuarios')}>
              Gestión de Usuarios
            </li>
          )}
          <li className="nav-item">Gestión de Cuotas</li>
          <li className="nav-item">Registrar Pagos</li>
        </ul>
      </nav>
    </div>
  );
};