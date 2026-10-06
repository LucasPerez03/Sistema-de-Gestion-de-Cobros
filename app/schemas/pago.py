from datetime import date
from typing import Optional

from pydantic import BaseModel


class PagoCreate(BaseModel):
    id_cuota: int
    monto: float
    medio_pago: str
    comprobante_ref: Optional[str] = None


class PagoResponse(BaseModel):
    id_pago: int
    id_usuario: int
    fecha_pago: date

    class Config:
        from_attributes = True
