from fastapi import APIRouter, status, Depends
from app.schemas.pago import PagoCreate, PagoResponse
from app.services.pago_service import PagoService
from app.config.security import obtener_usuario_actual
from app.schemas.auth import TokenData

router = APIRouter(prefix="/pagos", tags=["Pagos"])
pago_service = PagoService()

@router.post("/", response_model=PagoResponse, status_code=status.HTTP_201_CREATED)
def registrar_pago(
    pago: PagoCreate,
    usuario_actual: TokenData = Depends(obtener_usuario_actual)
):
    return pago_service.registrar_pago(pago, id_usuario_cobrador=usuario_actual.id_usuario)