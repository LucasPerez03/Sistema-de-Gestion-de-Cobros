from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class ClienteBase(BaseModel):
    nombre: str
    apellido: str
    dni: str 
    telefono: str
    email: EmailStr
    fecha_nacimiento: date

class ClienteCreate(ClienteBase):
    pass

class ClienteResponse(ClienteBase):
    id_cliente: int 
    fecha_alta: Optional[date] = None
    estado: bool

    class Config:
        from_attributes = True

