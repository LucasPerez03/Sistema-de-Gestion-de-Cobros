from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict

class ClienteBase(BaseModel):
    nombre: str
    apellido: str
    dni: str
    telefono: str
    email: EmailStr
    fecha_nacimiento: date

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    dni: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None
    fecha_nacimiento: Optional[date] = None
    estado: Optional[bool] = None

class ClienteResponse(ClienteBase):
    id_cliente: int
    fecha_alta: Optional[date] = None
    estado: bool

    model_config = ConfigDict(from_attributes=True)