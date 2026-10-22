from typing import List
from fastapi import APIRouter, status, Depends
from backend.app.schemas.cuota import CuotaCreate, CuotaResponse
from backend.app.services.cuota_service import CuotaService
from backend.app.config.security import obtener_usuario_actual, requerir_rol
from backend.app.schemas.auth import RolUsuario, TokenData

router = APIRouter(prefix="/cuotas", tags=["Cuotas"])
cuota_service = CuotaService()

@router.get("/", response_model=List[CuotaResponse], status_code=status.HTTP_200_OK)
def listar_cuotas(usuario_actual: TokenData = Depends(obtener_usuario_actual)):
    if usuario_actual.rol == RolUsuario.CLIENTE:
        if not usuario_actual.id_cliente:
            return []
        return cuota_service.obtener_cuotas_por_cliente(usuario_actual.id_cliente)
    return cuota_service.obtener_cuotas()

@router.get("/cliente/{id_cliente}", response_model=List[CuotaResponse], status_code=status.HTTP_200_OK)
def obtener_cuotas_por_cliente(
    id_cliente: int, 
    usuario_actual: TokenData = Depends(obtener_usuario_actual)
):
    return cuota_service.obtener_cuotas_por_cliente(id_cliente)

@router.get("/{id_cuota}", response_model=CuotaResponse, status_code=status.HTTP_200_OK)
def obtener_cuota(
    id_cuota: int, 
    usuario_actual: TokenData = Depends(obtener_usuario_actual)
):
    return cuota_service.obtener_cuota_por_id(id_cuota)

@router.post("/", response_model=CuotaResponse, status_code=status.HTTP_201_CREATED)
def registrar_cuota(
    cuota: CuotaCreate,
    usuario_actual: TokenData = Depends(requerir_rol(RolUsuario.ADMIN))
):
    return cuota_service.registrar_cuota(cuota)

@router.delete("/{id_cuota}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_cuota(
    id_cuota: int,
    usuario_actual: TokenData = Depends(requerir_rol(RolUsuario.ADMIN))
):
    cuota_service.eliminar_cuota(id_cuota)