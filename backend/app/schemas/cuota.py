from datetime import date
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field
from backend.app.models.cuota import EstadoCuota
from backend.app.schemas.pago import PagoResponse

class CuotaBase(BaseModel):
    id_cliente: int
    id_servicio: int
    periodo: str = Field(pattern=r"^\d{4}-(0[1-9]|1[0-2])$", description="Formato YYYY-MM")
    importe: Decimal = Field(gt=0)
    fecha_vencimiento: date

class CuotaCreate(CuotaBase):
    pass

class CuotaResponse(CuotaBase):
    id_cuota: int
    estado: EstadoCuota
    saldo_pendiente: Optional[Decimal] = None
    cliente_nombre: Optional[str] = None
    cliente_apellido: Optional[str] = None
    cliente_dni: Optional[str] = None
    servicio_nombre: Optional[str] = None
    pagos: List[PagoResponse] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)