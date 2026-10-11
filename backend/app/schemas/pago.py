from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class PagoBase(BaseModel):
    id_cuota: int
    monto: Decimal = Field(gt=0)
    medio_pago: str
    comprobante_ref: Optional[str] = None

class PagoCreate(PagoBase):
    pass

class PagoResponse(PagoBase):
    id_pago: int
    id_usuario: int
    fecha_pago: datetime

    model_config = ConfigDict(from_attributes=True)