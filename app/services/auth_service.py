from datetime import timedelta
from fastapi import HTTPException, status

from app.config.security import create_access_token
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.usuario_service import UsuarioService


class AuthService:
    def __init__(self):
        self.usuario_repo = UsuarioRepository()
        self.usuario_service = UsuarioService()

    def login(self, datos_login: LoginRequest) -> TokenResponse:
        usuario = self.usuario_repo.obtener_por_email(str(datos_login.email))
        if not usuario or not self.usuario_service._verificar_password(
            datos_login.password, usuario["password"]
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email o contraseña incorrectos.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = create_access_token(
            {
                "id_usuario": usuario["id_usuario"],
                "sub": usuario["email"],
                "rol": usuario["rol"],
            },
            timedelta(minutes=120),
        )

        return TokenResponse(access_token=access_token)
