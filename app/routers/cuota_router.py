from typing import List
from fastapi import APIRouter, status
from app.schemas.cuota import CuotaCreate, CuotaResponse
from app.services.cuota_service import CuotaService

router = APIRouter(prefix="/cuotas", tags=["Cuotas"])
cuota_service = CuotaService()

@router.get("/", response_model=List[CuotaResponse], status_code=status.HTTP_200_OK)
def listar_cuotas():
    return cuota_service.obtener_cuotas()

@router.get("/cliente/{id_cliente}", response_model=List[CuotaResponse], status_code=status.HTTP_200_OK)
def obtener_cuotas_por_cliente(id_cliente: int):
    return cuota_service.obtener_cuotas_por_cliente(id_cliente)

@router.get("/{id_cuota}", response_model=CuotaResponse, status_code=status.HTTP_200_OK)
def obtener_cuota(id_cuota: int):
    return cuota_service.obtener_cuota_por_id(id_cuota)

@router.post("/", response_model=CuotaResponse, status_code=status.HTTP_201_CREATED)
def registrar_cuota(cuota: CuotaCreate):
    return cuota_service.registrar_cuota(cuota)