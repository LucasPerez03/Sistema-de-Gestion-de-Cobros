from typing import List
from decimal import Decimal
from fastapi import HTTPException, status
from backend.app.models.cuota import Cuota, EstadoCuota
from backend.app.models.pago import Pago
from backend.app.repositories.cliente_repository import ClienteRepository
from backend.app.repositories.cuota_repository import CuotaRepository
from backend.app.repositories.pago_repository import PagoRepository
from backend.app.repositories.servicio_repository import ServicioRepository
from backend.app.schemas.cuota import CuotaCreate


class CuotaService:
    def __init__(self):
        self.cuota_repo = CuotaRepository()
        self.cliente_repo = ClienteRepository()
        self.servicio_repo = ServicioRepository()
        self.pago_repo = PagoRepository()

    def construir_entidad_cuota(self, cuota_dict: dict) -> Cuota:
        """Reconstruye el objeto de dominio Cuota con su composición de Pagos"""
        cuota_obj = Cuota(
            id_cuota=cuota_dict["id_cuota"],
            id_cliente=cuota_dict["id_cliente"],
            id_servicio=cuota_dict["id_servicio"],
            periodo=cuota_dict["periodo"],
            importe=Decimal(str(cuota_dict["importe"])),
            fecha_vencimiento=cuota_dict["fecha_vencimiento"],
            estado=cuota_dict["estado"],
        )
        pagos_db = self.pago_repo.obtener_por_cuota(cuota_obj.id_cuota)
        for p in pagos_db:
            cuota_obj.agregar_pago(
                Pago(
                    id_pago=p["id_pago"],
                    id_cuota=p["id_cuota"],
                    id_usuario=p["id_usuario"],
                    monto=Decimal(str(p["monto"])),
                    fecha_pago=p["fecha_pago"],
                    medio_pago=p["medio_pago"],
                    comprobante_ref=p.get("comprobante_ref"),
                )
            )
        return cuota_obj

    def obtener_cuotas(self) -> List[dict]:
        cuotas = self.cuota_repo.obtener_todos()
        for c in cuotas:
            entidad = self.construir_entidad_cuota(c)
            c["saldo_pendiente"] = entidad.calcular_saldo()
        return cuotas

    def obtener_cuota_por_id(self, id_cuota: int) -> dict:
        cuota = self.cuota_repo.obtener_por_id(id_cuota)
        if not cuota:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cuota con ID {id_cuota} no encontrada",
            )
        entidad = self.construir_entidad_cuota(cuota)
        cuota["saldo_pendiente"] = entidad.calcular_saldo()
        return cuota

    def obtener_cuotas_por_cliente(self, id_cliente: int) -> List[dict]:
        cliente = self.cliente_repo.obtener_por_id(id_cliente)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente con ID {id_cliente} no encontrado",
            )
        cuotas = self.cuota_repo.obtener_por_cliente(id_cliente)
        for c in cuotas:
            entidad = self.construir_entidad_cuota(c)
            c["saldo_pendiente"] = entidad.calcular_saldo()
        return cuotas

    def registrar_cuota(self, datos_cuota: CuotaCreate) -> dict:
        cliente = self.cliente_repo.obtener_por_id(datos_cuota.id_cliente)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente con ID {datos_cuota.id_cliente} no encontrado",
            )

        servicio = self.servicio_repo.obtener_por_id(datos_cuota.id_servicio)
        if not servicio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Servicio con ID {datos_cuota.id_servicio} no encontrado",
            )

        datos = datos_cuota.model_dump()
        datos["estado"] = EstadoCuota.PENDIENTE.value
        return self.cuota_repo.crear(datos)

    def eliminar_cuota(self, id_cuota: int) -> bool:
        self.obtener_cuota_por_id(id_cuota)
        return self.cuota_repo.eliminar(id_cuota)