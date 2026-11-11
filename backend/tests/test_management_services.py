import unittest
from datetime import date, datetime
from decimal import Decimal
from unittest.mock import Mock

from fastapi import HTTPException
from psycopg2.errors import UniqueViolation

from backend.app.models.cuota import EstadoCuota
from backend.app.schemas.cliente import ClienteCreate
from backend.app.schemas.cuota import CuotaCreate
from backend.app.schemas.pago import PagoCreate
from backend.app.services.cliente_service import ClienteService
from backend.app.services.cuota_service import CuotaService
from backend.app.services.pago_service import PagoService
from backend.app.schemas.usuario import UsuarioUpdate
from backend.app.services.usuario_service import UsuarioService


class TestManagementServices(unittest.TestCase):
    def test_cliente_duplica_dni_responde_conflicto(self):
        service = ClienteService.__new__(ClienteService)
        service.cliente_repo = Mock()
        service.cliente_repo.crear.side_effect = UniqueViolation()
        cliente = ClienteCreate(
            nombre="Ana",
            apellido="Prueba",
            dni="12345678",
            telefono="1122334455",
            email="ana@example.com",
            fecha_nacimiento=date(1990, 1, 1),
        )

        with self.assertRaises(HTTPException) as context:
            service.registrar_cliente(cliente)

        self.assertEqual(context.exception.status_code, 409)

    def test_usuario_duplica_email_al_editar_responde_conflicto(self):
        service = UsuarioService.__new__(UsuarioService)
        service.usuario_repo = Mock()
        service.usuario_repo.obtener_por_id.return_value = {"id_usuario": 1}
        service.usuario_repo.actualizar.side_effect = UniqueViolation()
        usuario = UsuarioUpdate(email="repetido@example.com")

        with self.assertRaises(HTTPException) as context:
            service.actualizar_usuario(1, usuario)

        self.assertEqual(context.exception.status_code, 409)

    def test_cuota_duplicada_responde_conflicto(self):
        service = CuotaService.__new__(CuotaService)
        service.cliente_repo = Mock()
        service.cliente_repo.obtener_por_id.return_value = {"id_cliente": 1}
        service.servicio_repo = Mock()
        service.servicio_repo.obtener_por_id.return_value = {"id_servicio": 2}
        service.cuota_repo = Mock()
        service.cuota_repo.crear.side_effect = UniqueViolation()
        cuota = CuotaCreate(
            id_cliente=1,
            id_servicio=2,
            periodo="2026-11",
            importe=Decimal("1000.00"),
            fecha_vencimiento=date(2026, 11, 10),
        )

        with self.assertRaises(HTTPException) as context:
            service.registrar_cuota(cuota)

        self.assertEqual(context.exception.status_code, 409)

    def test_anular_cuota_actualiza_estado_sin_borrar(self):
        service = CuotaService.__new__(CuotaService)
        service.cuota_repo = Mock()
        service.cuota_repo.obtener_por_id.return_value = {
            "id_cuota": 3,
            "id_cliente": 1,
            "id_servicio": 2,
            "periodo": "2026-11",
            "importe": Decimal("1000.00"),
            "fecha_vencimiento": date(2026, 11, 10),
            "estado": EstadoCuota.PAGADA.value,
        }
        service.pago_repo = Mock()
        service.pago_repo.obtener_por_cuota.return_value = [
            {
                "id_pago": 4,
                "id_cuota": 3,
                "id_usuario": 1,
                "monto": Decimal("1000.00"),
                "fecha_pago": datetime(2026, 11, 1),
                "medio_pago": "EFECTIVO",
                "comprobante_ref": None,
            }
        ]
        service.cuota_repo.actualizar.return_value = {"estado": "ANULADA"}

        service.anular_cuota(3)

        service.cuota_repo.actualizar.assert_called_once_with(
            3, {"estado": EstadoCuota.ANULADA.value}
        )
        service.pago_repo.obtener_por_cuota.assert_called_once_with(3)
        service.cuota_repo.eliminar.assert_not_called()

    def test_no_permite_pagar_cuota_anulada(self):
        service = PagoService.__new__(PagoService)
        service.pago_repo = Mock()
        service.cuota_service = Mock()
        service.cuota_service.obtener_cuota_por_id.return_value = {
            "estado": EstadoCuota.ANULADA.value,
        }
        pago = PagoCreate(
            id_cuota=3,
            monto=Decimal("100.00"),
            medio_pago="EFECTIVO",
        )

        with self.assertRaises(HTTPException) as context:
            service.registrar_pago(pago, 1)

        self.assertEqual(context.exception.status_code, 400)
        service.pago_repo.crear.assert_not_called()


if __name__ == "__main__":
    unittest.main()
