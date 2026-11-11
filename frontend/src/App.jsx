import { useEffect, useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { getPerfilService } from './services/authService';
import { Login } from './pages/Login/Login';
import { Dashboard } from './pages/Dashboard/Dashboard';
import { Clientes } from './pages/Clientes/Clientes';
import { Usuarios } from './pages/Usuarios/Usuarios';
import { Servicios } from './pages/Servicios/Servicios';
import { Cuotas } from './pages/Cuotas/Cuotas';

const PrivateRoute = ({ children }) => {
  const token = localStorage.getItem('token');

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  return children;
};

const PublicRoute = ({ children }) => {
  const token = localStorage.getItem('token');

  if (token) {
    return <Navigate to="/dashboard" replace />;
  }

  return children;
};

const RoleRoute = ({ allowedRoles, children }) => {
  const [role, setRole] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    let active = true;
    getPerfilService()
      .then((profile) => {
        if (active) setRole(profile.rol);
      })
      .catch(() => {
        if (active) setError('No se pudo verificar tu rol.');
      });

    return () => {
      active = false;
    };
  }, []);

  if (error) return <p className="mensaje-error">{error}</p>;
  if (!role) return <p>Cargando permisos...</p>;
  if (!allowedRoles.includes(role)) {
    return <Navigate to="/dashboard" replace />;
  }

  return children;
};

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route
          path="/login"
          element={
            <PublicRoute>
              <Login />
            </PublicRoute>
          }
        />

        <Route
          path="/dashboard"
          element={
            <PrivateRoute>
              <Dashboard />
            </PrivateRoute>
          }
        />
        <Route
          path="/clientes"
          element={
            <PrivateRoute>
              <RoleRoute allowedRoles={['ADMIN', 'ENTRENADOR']}>
                <Clientes />
              </RoleRoute>
            </PrivateRoute>
          }
        />
        <Route
          path="/usuarios"
          element={
            <PrivateRoute>
              <RoleRoute allowedRoles={['ADMIN']}>
                <Usuarios />
              </RoleRoute>
            </PrivateRoute>
          }
        />
        <Route
          path="/servicios"
          element={
            <PrivateRoute>
              <RoleRoute allowedRoles={['ADMIN', 'ENTRENADOR']}>
                <Servicios />
              </RoleRoute>
            </PrivateRoute>
          }
        />
        <Route
          path="/cuotas"
          element={
            <PrivateRoute>
              <Cuotas />
            </PrivateRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;