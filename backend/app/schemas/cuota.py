from datetime import date
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field
from backend.app.schemas.pago import PagoResponse

class CuotaBase(BaseModel):
    id_cliente: int
    id_servicio: int
    periodo: str  # Ej: "2026-10"
    importe: Decimal = Field(gt=0)
    fecha_vencimiento: date

class CuotaCreate(CuotaBase):
    pass

class CuotaResponse(CuotaBase):
    id_cuota: int
    estado: str
    pagos: List[PagoResponse] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)