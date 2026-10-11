from typing import List, Optional
from fastapi import HTTPException, status
from app.repositories.servicio_repository import ServicioRepository
from app.schemas.servicio import ServicioCreate, ServicioUpdate


class ServicioService:
    def __init__(self):
        self.servicio_repo = ServicioRepository()

    def obtener_servicios(self) -> List[dict]:
        return self.servicio_repo.obtener_todos()

    def obtener_servicio_por_id(self, id_servicio: int) -> dict:
        servicio = self.servicio_repo.obtener_por_id(id_servicio)
        if not servicio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Servicio con ID {id_servicio} no encontrado",
            )
        return servicio

    def registrar_servicio(self, datos_servicio: ServicioCreate) -> dict:
        datos = datos_servicio.model_dump()
        datos["estado"] = True
        return self.servicio_repo.crear(datos)

    def actualizar_servicio(self, id_servicio: int, datos_servicio: ServicioUpdate) -> dict:
        self.obtener_servicio_por_id(id_servicio)
        datos_dict = datos_servicio.model_dump(exclude_unset=True)
        return self.servicio_repo.actualizar(id_servicio, datos_dict)

    def eliminar_servicio(self, id_servicio: int) -> bool:
        self.obtener_servicio_por_id(id_servicio)
        return self.servicio_repo.eliminar(id_servicio)