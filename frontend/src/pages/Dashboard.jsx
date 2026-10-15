import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getPerfilService, logoutService } from '../services/authService';

export const Dashboard = () => {
  const [usuario, setUsuario] = useState(null);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    // Obtenemos los datos del usuario logueado 
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

  if (error) return <p>{error}</p>;
  if (!usuario) return <p>Cargando datos del usuario...</p>;

  return (
    <div style={{ padding: '20px', fontFamily: 'sans-serif' }}>
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h1>BYPay - Panel Principal</h1>
        <button onClick={handleLogout} style={{ padding: '8px 16px', cursor: 'pointer' }}>
          Cerrar Sesión
        </button>
      </header>

      <div style={{ background: '#f4f4f4', padding: '15px', borderRadius: '8px', marginBottom: '20px' }}>
        <h3>Bienvenido/a, {usuario.nombre || usuario.email}</h3>
        <p><strong>Email:</strong> {usuario.email}</p>
        <p><strong>Rol:</strong> {usuario.rol}</p>
      </div>

      <nav>
        <ul>
          <li>Gestión de Clientes</li>
          <li>Gestión de Cuotas</li>
          <li>Registrar Pagos</li>
        </ul>
      </nav>
    </div>
  );
};