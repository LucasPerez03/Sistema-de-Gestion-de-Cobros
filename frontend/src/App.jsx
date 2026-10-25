import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Login } from './pages/Login';
import { Dashboard } from './pages/Dashboard';
import { Clientes } from './pages/Clientes';
import { Usuarios } from './pages/Usuarios';
import { Servicios } from './pages/Servicios';
import { Cuotas } from './pages/Cuotas';

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