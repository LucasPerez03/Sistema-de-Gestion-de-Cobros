from typing import List

from fastapi import APIRouter, status
from app.schemas.servicio import ServicioCreate, ServicioResponse
from app.services.servicio_service import ServicioService

router = APIRouter(prefix="/servicios", tags=["Servicios"])
servicio_service = ServicioService()


@router.get("/", response_model=List[ServicioResponse], status_code=status.HTTP_200_OK)
def listar_servicios():
    return servicio_service.obtener_servicios()


@router.get("/{id_servicio}", response_model=ServicioResponse, status_code=status.HTTP_200_OK)
def obtener_servicio(id_servicio: int):
    return servicio_service.obtener_servicio_por_id(id_servicio)


@router.post("/", response_model=ServicioResponse, status_code=status.HTTP_201_CREATED)
def registrar_servicio(servicio: ServicioCreate):
    return servicio_service.registrar_servicio(servicio)

