from fastapi import APIRouter, Depends, status

from app.config.security import get_current_user
from app.schemas.auth import LoginRequest, TokenResponse, TokenData
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Autenticación"])
auth_service = AuthService()


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def login(datos_login: LoginRequest):
    return auth_service.login(datos_login)


@router.get("/me", response_model=TokenData, status_code=status.HTTP_200_OK)
def obtener_usuario_actual(usuario_actual: TokenData = Depends(get_current_user)):
    return usuario_actual
