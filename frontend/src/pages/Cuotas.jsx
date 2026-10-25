import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  getCuotasService,
  createCuotaService,
  getClientesService,
  getServiciosService,
  registrarPagoService,
  getPagosService,
} from '../services/dataService';
import { getPerfilService } from '../services/authService';
import './Cuotas.css';

export const Cuotas = () => {
  const [usuario, setUsuario] = useState(null);
  const [cuotas, setCuotas] = useState([]);
  const [pagos, setPagos] = useState([]);
  const [clientes, setClientes] = useState([]);
  const [servicios, setServicios] = useState([]);

  // Estados para emitir cuota (ADMIN)
  const [idCliente, setIdCliente] = useState('');
  const [idServicio, setIdServicio] = useState('');
  const [periodo, setPeriodo] = useState('2026-10');
  const [importe, setImporte] = useState('');
  const [fechaVencimiento, setFechaVencimiento] = useState('');

  // Estados para registrar cobro (Pago + Strategy)
  const [cuotaSeleccionada, setCuotaSeleccionada] = useState(null);
  const [montoPago, setMontoPago] = useState('');
  const [medioPago, setMedioPago] = useState('EFECTIVO');
  const [comprobanteRef, setComprobanteRef] = useState('');

  const [error, setError] = useState('');
  const [mensaje, setMensaje] = useState('');
  const navigate = useNavigate();

  const cargarTodo = async () => {
    try {
      const perfil = await getPerfilService();
      setUsuario(perfil);

      const promesas = [getCuotasService(), getPagosService()];
      if (perfil.rol !== 'CLIENTE') {
        promesas.push(getClientesService(), getServiciosService());
      }

      const [cuotasData, pagosData, clientesData, serviciosData] =
        await Promise.all(promesas);

      setCuotas(cuotasData);
      setPagos(pagosData);
      if (clientesData) setClientes(clientesData);
      if (serviciosData) setServicios(serviciosData.filter((s) => s.estado));
    } catch (err) {
      setError('Error al cargar la información de cuotas y pagos.');
    }
  };

  useEffect(() => {
    cargarTodo();
  }, []);

  // Al elegir un servicio en el formulario de emisión, autocompleta su precio base
  const handleServicioChange = (e) => {
    const selectedId = e.target.value;
    setIdServicio(selectedId);
    const serv = servicios.find((s) => String(s.id_servicio) === String(selectedId));
    if (serv) {
      setImporte(serv.precio);
    }
  };

  const handleEmitirCuota = async (e) => {
    e.preventDefault();
    setError('');
    setMensaje('');

    try {
      await createCuotaService({
        id_cliente: Number(idCliente),
        id_servicio: Number(idServicio),
        periodo,
        importe: Number(importe),
        fecha_vencimiento: fechaVencimiento,
      });
      setMensaje('Cuota emitida exitosamente.');
      setIdCliente('');
      setIdServicio('');
      setImporte('');
      setFechaVencimiento('');
      cargarTodo();
    } catch (err) {
      if (err.response?.status === 403) {
        setError('Solo el rol ADMIN puede emitir cuotas.');
      } else if (err.response?.status === 422) {
        setError('Formato inválido. Verificá que el período sea YYYY-MM (ej. 2026-10).');
      } else {
        setError('Error al emitir la cuota (verificá que no esté duplicada para ese período).');
      }
    }
  };

  const abrirFormularioCobro = (cuota) => {
    setError('');
    setMensaje('');
    setCuotaSeleccionada(cuota);
    setMontoPago(cuota.saldo_pendiente ?? cuota.importe);
    setMedioPago('EFECTIVO');
    setComprobanteRef('');
  };

  // Vista previa del Patrón Strategy en el Frontend (Espejo del Backend)
  const calcularVistaPreviaStrategy = (montoBase, medio) => {
    const num = Number(montoBase) || 0;
    if (medio === 'EFECTIVO') return (num * 0.9).toFixed(2);
    if (medio === 'TARJETA') return (num * 1.1).toFixed(2);
    return num.toFixed(2);
  };

  const handleRegistrarPago = async (e) => {
    e.preventDefault();
    if (!cuotaSeleccionada) return;
    setError('');
    setMensaje('');

    try {
      const resp = await registrarPagoService({
        id_cuota: cuotaSeleccionada.id_cuota,
        monto: Number(montoPago),
        medio_pago: medioPago,
        comprobante_ref: comprobanteRef || null,
      });

      const montoCobrado = resp.monto_cobrado_con_estrategia ?? montoPago;
      setMensaje(
        `Pago registrado con éxito. Monto final cobrado con estrategia (${medioPago}): $${Number(
          montoCobrado
        ).toFixed(2)}`
      );
      setCuotaSeleccionada(null);
      cargarTodo();
    } catch (err) {
      setError(
        err.response?.data?.detail || 'Error al procesar el pago de la cuota.'
      );
    }
  };

  return (
    <div className="cuotas-container">
      <button onClick={() => navigate('/dashboard')} className="btn-back">
        ← Volver al Dashboard
      </button>

      <h2>Gestión de Cuotas y Cobros</h2>

      {mensaje && <p className="mensaje-exito">{mensaje}</p>}
      {error && <p className="mensaje-error">{error}</p>}

      {/* 1. Formulario de Emisión de Cuota (Solo ADMIN) */}
      {usuario?.rol === 'ADMIN' && (
        <div className="form-card">
          <h3>Emitir Nueva Cuota Mensual</h3>
          <form onSubmit={handleEmitirCuota} className="inline-form">
            <select
              value={idCliente}
              onChange={(e) => setIdCliente(e.target.value)}
              required
            >
              <option value="">-- Seleccionar Cliente --</option>
              {clientes.map((c) => (
                <option key={c.id_cliente} value={c.id_cliente}>
                  {c.nombre} {c.apellido} (DNI: {c.dni})
                </option>
              ))}
            </select>

            <select
              value={idServicio}
              onChange={handleServicioChange}
              required
            >
              <option value="">-- Seleccionar Servicio/Plan --</option>
              {servicios.map((s) => (
                <option key={s.id_servicio} value={s.id_servicio}>
                  {s.nombre} (${Number(s.precio).toFixed(2)})
                </option>
              ))}
            </select>

            <input
              type="text"
              placeholder="Período (YYYY-MM)"
              pattern="\d{4}-(0[1-9]|1[0-2])"
              title="Formato requerido: YYYY-MM (ej. 2026-10)"
              value={periodo}
              onChange={(e) => setPeriodo(e.target.value)}
              required
            />

            <input
              type="number"
              step="0.01"
              min="1"
              placeholder="Importe ($)"
              value={importe}
              onChange={(e) => setImporte(e.target.value)}
              required
            />

            <input
              type="date"
              value={fechaVencimiento}
              onChange={(e) => setFechaVencimiento(e.target.value)}
              required
            />

            <button type="submit">Emitir Cuota</button>
          </form>
        </div>
      )}

      {/* 2. Panel de Cobro de Cuota Seleccionada (Patrón Strategy) */}
      {cuotaSeleccionada && (
        <div className="form-card cobro-card">
          <h3>
            Registrar Cobro - Cuota #{cuotaSeleccionada.id_cuota} (Período{' '}
            {cuotaSeleccionada.periodo})
          </h3>
          <p>
            <strong>Cliente:</strong>{' '}
            {cuotaSeleccionada.cliente_nombre
              ? `${cuotaSeleccionada.cliente_nombre} ${cuotaSeleccionada.cliente_apellido}`
              : `ID #${cuotaSeleccionada.id_cliente}`}{' '}
            | <strong>Saldo Pendiente:</strong> $
            {Number(
              cuotaSeleccionada.saldo_pendiente ?? cuotaSeleccionada.importe
            ).toFixed(2)}
          </p>

          <form onSubmit={handleRegistrarPago} className="inline-form">
            <input
              type="number"
              step="0.01"
              min="1"
              max={cuotaSeleccionada.saldo_pendiente ?? cuotaSeleccionada.importe}
              placeholder="Monto a imputar ($)"
              value={montoPago}
              onChange={(e) => setMontoPago(e.target.value)}
              required
            />

            <select
              value={medioPago}
              onChange={(e) => setMedioPago(e.target.value)}
            >
              <option value="EFECTIVO">Efectivo (10% Descuento)</option>
              <option value="TRANSFERENCIA">Transferencia (Precio Lista)</option>
              <option value="MERCADO_PAGO">Mercado Pago (Precio Lista)</option>
              <option value="TARJETA">Tarjeta (10% Recargo)</option>
            </select>

            <input
              type="text"
              placeholder="Comprobante / Referencia (opcional)"
              value={comprobanteRef}
              onChange={(e) => setComprobanteRef(e.target.value)}
            />

            <button type="submit">Confirmar Cobro</button>
            <button
              type="button"
              className="btn-cancel"
              onClick={() => setCuotaSeleccionada(null)}
            >
              Cancelar
            </button>
          </form>

          <p className="strategy-preview">
            <strong>Monto real a abonar según estrategia ({medioPago}):</strong> $
            {calcularVistaPreviaStrategy(montoPago, medioPago)}
          </p>
        </div>
      )}

      {/* 3. Tabla de Cuotas */}
      <h3>Listado de Cuotas</h3>
      <table className="tabla-clientes">
        <thead>
          <tr>
            <th>ID</th>
            <th>Cliente</th>
            <th>Servicio</th>
            <th>Período</th>
            <th>Vencimiento</th>
            <th>Importe Total</th>
            <th>Saldo Pendiente</th>
            <th>Estado</th>
            {usuario?.rol !== 'CLIENTE' && <th>Acción</th>}
          </tr>
        </thead>
        <tbody>
          {cuotas.map((c) => {
            const saldo = Number(c.saldo_pendiente ?? c.importe);
            return (
              <tr key={c.id_cuota}>
                <td>{c.id_cuota}</td>
                <td>
                  {c.cliente_nombre
                    ? `${c.cliente_nombre} ${c.cliente_apellido}`
                    : `Cliente #${c.id_cliente}`}
                </td>
                <td>{c.servicio_nombre || `Servicio #${c.id_servicio}`}</td>
                <td>{c.periodo}</td>
                <td>{c.fecha_vencimiento}</td>
                <td>${Number(c.importe).toFixed(2)}</td>
                <td>${saldo.toFixed(2)}</td>
                <td>
                  <span className={`badge-estado estado-${c.estado.toLowerCase()}`}>
                    {c.estado}
                  </span>
                </td>
                {usuario?.rol !== 'CLIENTE' && (
                  <td>
                    {c.estado !== 'PAGADA' && saldo > 0 ? (
                      <button
                        type="button"
                        onClick={() => abrirFormularioCobro(c)}
                      >
                        Cobrar
                      </button>
                    ) : (
                      <span>Completada</span>
                    )}
                  </td>
                )}
              </tr>
            );
          })}
        </tbody>
      </table>

      {/* 4. Historial de Pagos */}
      <h3 style={{ marginTop: '2rem' }}>Historial de Pagos Registrados</h3>
      <table className="tabla-clientes">
        <thead>
          <tr>
            <th>ID Pago</th>
            <th>Cuota / Período</th>
            <th>Cliente</th>
            <th>Servicio</th>
            <th>Monto Imputado</th>
            <th>Medio de Pago</th>
            <th>Comprobante</th>
            <th>Fecha</th>
          </tr>
        </thead>
        <tbody>
          {pagos.map((p) => (
            <tr key={p.id_pago}>
              <td>{p.id_pago}</td>
              <td>
                #{p.id_cuota} {p.periodo ? `(${p.periodo})` : ''}
              </td>
              <td>
                {p.cliente_nombre
                  ? `${p.cliente_nombre} ${p.cliente_apellido}`
                  : '-'}
              </td>
              <td>{p.servicio_nombre || '-'}</td>
              <td>${Number(p.monto).toFixed(2)}</td>
              <td>{p.medio_pago}</td>
              <td>{p.comprobante_ref || '-'}</td>
              <td>{new Date(p.fecha_pago).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};