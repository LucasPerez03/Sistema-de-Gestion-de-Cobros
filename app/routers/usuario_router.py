from typing import List
from fastapi import APIRouter, Depends, status

from app.config.security import get_current_user
from app.schemas.auth import TokenData
from app.schemas.usuario import UsuarioCreate, UsuarioResponse
from app.services.usuario_service import UsuarioService

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])
usuario_service = UsuarioService()


@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def registrar_usuario(usuario: UsuarioCreate):
    return usuario_service.registrar_usuario(usuario)


@router.get(
    "/",
    response_model=List[UsuarioResponse],
    status_code=status.HTTP_200_OK,
)
def listar_usuarios(usuario_actual: TokenData = Depends(get_current_user)):
    del usuario_actual
    return usuario_service.obtener_usuarios()


@router.get("/{id_usuario}", response_model=UsuarioResponse, status_code=status.HTTP_200_OK)
def obtener_usuario(id_usuario: int):
    return usuario_service.obtener_usuario_por_id(id_usuario)