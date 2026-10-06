from datetime import date
from typing import List

from pydantic import BaseModel

from app.schemas.pago import PagoResponse


class CuotaCreate(BaseModel):
    id_cliente: int
    id_servicio: int
    periodo: str
    importe: float
    fecha_vencimiento: date


class CuotaResponse(BaseModel):
    id_cuota: int
    estado: str
    pagos: List[PagoResponse] = []

    class Config:
        from_attributes = True
