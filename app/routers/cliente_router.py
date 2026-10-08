from typing import List
from fastapi import APIRouter, Depends, status

from app.schemas.cliente import ClienteCreate, ClienteResponse
from app.services.cliente_service import ClienteService
from app.config.security import obtener_usuario_actual
from app.schemas.auth import TokenData

router = APIRouter(prefix="/clientes", tags=["Clientes"])
cliente_service = ClienteService()

@router.get("/", response_model=List[ClienteResponse], status_code=status.HTTP_200_OK)
def listar_clientes():
    return cliente_service.obtener_clientes()

@router.get("/{id_cliente}", response_model=ClienteResponse, status_code=status.HTTP_200_OK)
def obtener_cliente(id_cliente: int):
    return cliente_service.obtener_cliente_por_id(id_cliente)

@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
def registrar_cliente(cliente: ClienteCreate):
    return cliente_service.registrar_cliente(cliente)
