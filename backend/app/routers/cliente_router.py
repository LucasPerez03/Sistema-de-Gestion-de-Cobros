from typing import List
from fastapi import APIRouter, Depends, status
from app.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteResponse
from app.services.cliente_service import ClienteService
from app.config.security import obtener_usuario_actual
from app.schemas.auth import TokenData

router = APIRouter(prefix="/clientes", tags=["Clientes"])
cliente_service = ClienteService()

@router.get("/", response_model=List[ClienteResponse], status_code=status.HTTP_200_OK)
def listar_clientes(usuario_actual: TokenData = Depends(obtener_usuario_actual)):
    return cliente_service.obtener_clientes()

@router.get("/{id_cliente}", response_model=ClienteResponse, status_code=status.HTTP_200_OK)
def obtener_cliente(
    id_cliente: int,
    usuario_actual: TokenData = Depends(obtener_usuario_actual)
):
    return cliente_service.obtener_cliente_por_id(id_cliente)

@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
def registrar_cliente(
    cliente: ClienteCreate,
    usuario_actual: TokenData = Depends(obtener_usuario_actual)
):
    return cliente_service.registrar_cliente(cliente)

@router.put("/{id_cliente}", response_model=ClienteResponse, status_code=status.HTTP_200_OK)
def actualizar_cliente(
    id_cliente: int,
    cliente: ClienteUpdate,
    usuario_actual: TokenData = Depends(obtener_usuario_actual)
):
    return cliente_service.actualizar_cliente(id_cliente, cliente)

@router.delete("/{id_cliente}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_cliente(
    id_cliente: int,
    usuario_actual: TokenData = Depends(obtener_usuario_actual)
):
    cliente_service.eliminar_cliente(id_cliente)