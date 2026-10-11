from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict
from backend.app.schemas.auth import RolUsuario

class UsuarioBase(BaseModel):
    email: EmailStr
    nombre: str
    apellido: str   
    rol: RolUsuario

class UsuarioCreate(UsuarioBase):
    password: str
    id_cliente: Optional[int] = None


class UsuarioUpdate(BaseModel):
    email: Optional[EmailStr] = None
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    rol: Optional[RolUsuario] = None
    password: Optional[str] = None
    estado: Optional[bool] = None


class UsuarioResponse(UsuarioBase):
    id_usuario: int
    estado: bool
    id_cliente: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)