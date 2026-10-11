from datetime import date
from typing import List, Optional
from pydantic import BaseModel

from backend.app.schemas.pago import PagoResponse

class CuotaBase(BaseModel):
    id_cliente: int
    id_servicio: int
    periodo: date
    importe: float
    fecha_vencimiento: date

class CuotaCreate(CuotaBase):
    pass

class CuotaResponse(BaseModel):
    id_cuota: int
    estado: str
    pagos: List[PagoResponse] = []

    class Config:
        from_attributes = True
