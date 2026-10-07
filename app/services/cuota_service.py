from datetime import date
from typing import List, Optional
from fastapi import HTTPException, status
from app.repositories.cliente_repository import ClienteRepository
from app.repositories.cuota_repository import CuotaRepository
from app.repositories.servicio_repository import ServicioRepository
from app.schemas.cuota import CuotaCreate


class CuotaService:
    def __init__(self):
        self.cuota_repo = CuotaRepository()
        self.cliente_repo = ClienteRepository()
        self.servicio_repo = ServicioRepository()

    def obtener_cuotas(self) -> List[dict]:
        return self.cuota_repo.obtener_todos()

    def obtener_cuota_por_id(self, id_cuota: int) -> dict:
        cuota = self.cuota_repo.obtener_por_id(id_cuota)
        if not cuota:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cuota con ID {id_cuota} no encontrada",
            )
        return cuota

    def obtener_cuotas_por_cliente(self, id_cliente: int) -> List[dict]:
        cliente = self.cliente_repo.obtener_por_id(id_cliente)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente con ID {id_cliente} no encontrado",
            )
        return self.cuota_repo.obtener_por_cliente(id_cliente)

   
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
        datos["estado"] = "PENDIENTE"
        return self.cuota_repo.crear(datos)

    def actualizar_cuota(
        self, id_cuota: int, datos_cuota: dict
    ) -> Optional[dict]:
        raise NotImplementedError("Actualizar cuotas todavía no está implementado.")

    def eliminar_cuota(self, id_cuota: int) -> bool:
        raise NotImplementedError("Eliminar cuotas todavía no está implementado.")
