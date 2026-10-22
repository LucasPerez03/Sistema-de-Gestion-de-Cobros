from typing import List
from fastapi import APIRouter, status, Depends
from backend.app.schemas.pago import PagoCreate, PagoResponse
from backend.app.services.pago_service import PagoService
from backend.app.config.security import obtener_usuario_actual
from backend.app.schemas.auth import RolUsuario, TokenData

router = APIRouter(prefix="/pagos", tags=["Pagos"])
pago_service = PagoService()

@router.get("/", response_model=List[PagoResponse], status_code=status.HTTP_200_OK)
def listar_pagos(usuario_actual: TokenData = Depends(obtener_usuario_actual)):
    if usuario_actual.rol == RolUsuario.CLIENTE:
        if not usuario_actual.id_cliente:
            return []
        return pago_service.obtener_pagos_por_cliente(usuario_actual.id_cliente)
    return pago_service.obtener_historial_pagos()

@router.post("/", response_model=PagoResponse, status_code=status.HTTP_201_CREATED)
def registrar_pago(
    pago: PagoCreate,
    usuario_actual: TokenData = Depends(obtener_usuario_actual)
):
    return pago_service.registrar_pago(pago, id_usuario_cobrador=usuario_actual.id_usuario)