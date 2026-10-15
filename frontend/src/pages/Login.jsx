import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { loginService } from '../services/authService';

export const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      await loginService(email, password);
      // Redirige automáticamente al dashboard
      navigate('/dashboard');
    } catch (err) {
      if (err.response?.status === 401) {
        setError('Credenciales incorrectas');
      } else {
        setError('Error al conectar con el servidor');
      }
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: '50px auto', padding: '20px' }}>
      <h2>Iniciar Sesión - BYPay</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Email:</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            style={{ width: '100%', marginBottom: '10px', padding: '8px' }}
          />
        </div>
        <div>
          <label>Contraseña:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            style={{ width: '100%', marginBottom: '10px', padding: '8px' }}
          />
        </div>
        <button type="submit" style={{ padding: '10px 15px' }}>
          Ingresar
        </button>
      </form>
      {error && <p style={{ color: 'red', marginTop: '10px' }}>{error}</p>}
    </div>
  );
};