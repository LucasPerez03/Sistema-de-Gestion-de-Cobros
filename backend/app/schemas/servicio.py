from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class ServicioBase(BaseModel):
    nombre: str
    precio: Decimal = Field(gt=0)
    descripcion: Optional[str] = None

class ServicioCreate(ServicioBase):
    pass

class ServicioUpdate(BaseModel):
    nombre: Optional[str] = None
    precio: Optional[Decimal] = None
    descripcion: Optional[str] = None
    estado: Optional[bool] = None

class ServicioResponse(ServicioBase):
    id_servicio: int
    estado: bool

    model_config = ConfigDict(from_attributes=True)