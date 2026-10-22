import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { loginService } from '../services/authService';
import './Login.css';

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
    <div className="login-container">
      <h2>Iniciar Sesión - BYPay</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Email:</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label>Contraseña:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">Ingresar</button>
      </form>
      {error && <p className="mensaje-error">{error}</p>}
    </div>
  );
};