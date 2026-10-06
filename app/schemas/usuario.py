from pydantic import BaseModel, EmailStr
from typing import Optional

class UsuarioBase(BaseModel):
    email: EmailStr 
    nombre: str
    apellido: str
    rol: str

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioResponse(UsuarioBase):
    id_usuario: int
    estado: bool

    class Config:
        from_atributes = True