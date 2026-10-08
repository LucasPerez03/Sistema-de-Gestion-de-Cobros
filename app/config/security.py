from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from app.config.settings import settings
from app.schemas.auth import TokenData

# Esquema OAuth2 Bearer para la interfaz de Swagger UI
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Genera un JWT firmado con los valores de settings."""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    """Valida el token JWT en endpoints protegidos."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales o el token ha expirado.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        id_usuario: int = payload.get("id_usuario")
        email: str = payload.get("sub")
        rol: str = payload.get("rol")

        if email is None or id_usuario is None:
            raise credentials_exception

        return TokenData(id_usuario=id_usuario, email=email, rol=rol)
    except (JWTError, TypeError, ValueError):
        raise credentials_exception


def crear_token_acceso(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Alias backward-compatible para la versión existente."""
    return create_access_token(data, expires_delta)


def obtener_usuario_actual(token: str = Depends(oauth2_scheme)) -> TokenData:
    """Alias backward-compatible para la versión existente."""
    return get_current_user(token)