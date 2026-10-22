import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { registerService } from '../services/authService';
import './Register.css';

export const Register = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [rol, setRol] = useState('CLIENTE');
  const [error, setError] = useState('');
  const [mensaje, setMensaje] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setMensaje('');

    try {
      await registerService({ email, password, rol });
      setMensaje('Registro exitoso. Redirigiendo al login...');
      setTimeout(() => navigate('/login'), 2000);
    } catch (err) {
      if (err.response?.status === 400) {
        setError('El email ya se encuentra registrado.');
      } else {
        setError('Error al registrar usuario.');
      }
    }
  };

  return (
    <div className="register-container">
      <h2>Crear Cuenta - BYPay</h2>
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
        <div className="form-group">
          <label>Rol:</label>
          <select value={rol} onChange={(e) => setRol(e.target.value)}>
            <option value="CLIENTE">Cliente</option>
            <option value="ENTRENADOR">Entrenador</option>
          </select>
        </div>
        <button type="submit">Registrarse</button>
      </form>

      {mensaje && <p className="mensaje-exito">{mensaje}</p>}
      {error && <p className="mensaje-error">{error}</p>}

      <p className="login-link">
        ¿Ya tenés cuenta? <Link to="/login">Iniciá sesión acá</Link>
      </p>
    </div>
  );
};