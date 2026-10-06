from pydantic import BaseModel
from typing import Optional

class ServicioBase(BaseModel):
    nombre: str
    precio: float
    descripcion: Optional[str] = None


class ServicioCreate(ServicioBase):
    pass


class ServicioResponse(ServicioBase):
    id_servicio: int
    estado: bool

    class Config:
        from_attributes = True
