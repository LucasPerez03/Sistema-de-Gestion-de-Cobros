from pydantic import BaseModel, EmailStr
from app.schemas.auth import RolUsuario
class UsuarioBase(BaseModel):
    email: EmailStr 
    nombre: str
    apellido: str
    rol: RolUsuario 

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioResponse(UsuarioBase):
    id_usuario: int
    estado: bool

    class Config:
        from_atributes = True