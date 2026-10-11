from typing import List

from fastapi import APIRouter, status, Depends
from backend.app.schemas.servicio import ServicioCreate, ServicioResponse
from backend.app.services.servicio_service import ServicioService
from backend.app.config.security import obtener_usuario_actual, requerir_rol
from backend.app.schemas.auth import TokenData

router = APIRouter(prefix="/servicios", tags=["Servicios"])
servicio_service = ServicioService()

@router.get("/", response_model=List[ServicioResponse], status_code=status.HTTP_200_OK)
def listar_servicios(usuario_actual: TokenData = Depends(obtener_usuario_actual)):
    return servicio_service.obtener_servicios()

@router.get("/{id_servicio}", response_model=ServicioResponse, status_code=status.HTTP_200_OK)
def obtener_servicio(id_servicio: int, usuario_actual: TokenData = Depends(obtener_usuario_actual)):
    return servicio_service.obtener_servicio_por_id(id_servicio)

@router.post("/", response_model=ServicioResponse, status_code=status.HTTP_201_CREATED)
def registrar_servicio(servicio: ServicioCreate, usuario_actual: TokenData = Depends(requerir_rol["ADMIN"])):
    return servicio_service.registrar_servicio(servicio)

