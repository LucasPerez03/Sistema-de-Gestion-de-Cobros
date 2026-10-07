from typing import List, Optional
from fastapi import HTTPException, status
from app.repositories.cliente_repository import ClienteRepository
from app.schemas.cliente import ClienteCreate


class ClienteService:
    def __init__(self):
        self.cliente_repo = ClienteRepository()

    def obtener_clientes(self) -> List[dict]:
        return self.cliente_repo.obtener_todos()

    def obtener_cliente_por_id(self, id_cliente: int) -> dict:
        cliente = self.cliente_repo.obtener_por_id(id_cliente)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente con ID {id_cliente} no encontrado",
            )
        return cliente

    def registrar_cliente(self, datos_cliente: ClienteCreate) -> dict:
        datos = datos_cliente.model_dump()
        datos["estado"] = True
        return self.cliente_repo.crear(datos)

    def actualizar_cliente(self, id_cliente: int, datos_cliente: dict) -> Optional[dict]:
        raise NotImplementedError("Actualizar clientes todavía no está implementado.")

    def eliminar_cliente(self, id_cliente: int) -> bool:
        raise NotImplementedError("Eliminar clientes todavía no está implementado.")
