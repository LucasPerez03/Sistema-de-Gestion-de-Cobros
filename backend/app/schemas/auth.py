from enum import Enum

from pydantic import BaseModel, EmailStr


class RolUsuario(str, Enum):
    ADMIN = "ADMIN"
    ENTRENADOR = "ENTRENADOR"
    CLIENTE = "CLIENTE"


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

