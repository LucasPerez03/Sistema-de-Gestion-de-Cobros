from datetime import datetime, timedelta, timezone
from typing import Optional, Union, List
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials  # <-- Cambiado

from backend.app.config.settings import settings
from backend.app.schemas.auth import RolUsuario, TokenData

# Usamos HTTPBearer para que Swagger pida el Bearer Token en un campo simple
security_scheme = HTTPBearer()


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


def get_current_user(auth: HTTPAuthorizationCredentials = Depends(security_scheme)) -> TokenData:
    """Valida el token JWT en endpoints protegidos."""
    token = auth.credentials  # <-- Extraemos el string del token del header Bearer

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

        if email is None or id_usuario is None or rol is None:
            raise credentials_exception

        try:
            rol_usuario = RolUsuario(rol)
        except ValueError:
            raise credentials_exception

        return TokenData(id_usuario=id_usuario, email=email, rol=rol_usuario)
    except (JWTError, TypeError, ValueError):
        raise credentials_exception


# Aliases explícitos
crear_token_acceso = create_access_token
obtener_usuario_actual = get_current_user


def requerir_rol(roles_permitidos: Union[RolUsuario, List[RolUsuario]]):
    """
    Dependencia para verificar que el usuario tenga un rol autorizado.
    Acepta tanto un rol individual (RolUsuario.ADMIN) como una lista de roles.
    """
    if isinstance(roles_permitidos, RolUsuario):
        roles_permitidos = [roles_permitidos]

    def verificador_rol(
        usuario_actual: TokenData = Depends(obtener_usuario_actual),
    ) -> TokenData:
        if usuario_actual.rol not in roles_permitidos:
            roles = ", ".join(rol.value for rol in roles_permitidos)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acceso denegado: Se requiere uno de los siguientes roles: {roles}",
            )
        return usuario_actual

    return verificador_rol