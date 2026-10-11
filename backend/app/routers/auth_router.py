from fastapi import APIRouter, Depends, status
from app.config.security import obtener_usuario_actual
from app.schemas.auth import LoginRequest, TokenResponse, TokenData
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Autenticación"])
auth_service = AuthService()

@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def login(datos_login: LoginRequest):
    return auth_service.login(datos_login)

@router.get("/me", response_model=TokenData, status_code=status.HTTP_200_OK)
def obtener_mi_perfil(usuario_actual: TokenData = Depends(obtener_usuario_actual)):
    return usuario_actual