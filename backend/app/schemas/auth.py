from typing import Optional
from pydantic import BaseModel, EmailStr
from backend.app.models.usuario import RolUsuario

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    id_usuario: int
    email: EmailStr
    rol: RolUsuario
    id_cliente: Optional[int] = None