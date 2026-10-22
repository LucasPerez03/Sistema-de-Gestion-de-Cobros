from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from backend.app.models.pago import MedioPago

class PagoBase(BaseModel):
    id_cuota: int
    monto: Decimal = Field(gt=0)
    medio_pago: MedioPago
    comprobante_ref: Optional[str] = None

class PagoCreate(PagoBase):
    pass

class PagoResponse(PagoBase):
    id_pago: int
    id_usuario: int
    fecha_pago: datetime
    monto_cobrado_con_estrategia: Optional[Decimal] = None
    periodo: Optional[str] = None
    cliente_nombre: Optional[str] = None
    cliente_apellido: Optional[str] = None
    servicio_nombre: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)