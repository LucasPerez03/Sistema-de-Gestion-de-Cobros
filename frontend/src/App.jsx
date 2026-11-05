import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Login } from './pages/Login/Login';
import { Dashboard } from './pages/Dashboard/Dashboard';
import { Clientes } from './pages/Clientes/Clientes';
import { Usuarios } from './pages/Usuarios/Usuarios';
import { Servicios } from './pages/Servicios/Servicios';
import { Cuotas } from './pages/Cuotas/Cuotas';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/clientes" element={<Clientes />} />
        <Route path="/usuarios" element={<Usuarios />} />
        <Route path="/servicios" element={<Servicios />} />
        <Route path="/cuotas" element={<Cuotas />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;