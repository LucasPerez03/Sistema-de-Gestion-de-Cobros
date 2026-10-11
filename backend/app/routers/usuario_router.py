from typing import List
from fastapi import APIRouter, Depends, status
from app.config.security import obtener_usuario_actual, requerir_rol
from app.schemas.auth import TokenData
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioResponse
from app.services.usuario_service import UsuarioService

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])
usuario_service = UsuarioService()

@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def registrar_usuario(
    usuario: UsuarioCreate,
    usuario_actual: TokenData = Depends(requerir_rol("ADMIN"))
):
    return usuario_service.registrar_usuario(usuario)

@router.get("/", response_model=List[UsuarioResponse], status_code=status.HTTP_200_OK)
def listar_usuarios(usuario_actual: TokenData = Depends(requerir_rol("ADMIN"))):
    return usuario_service.obtener_usuarios()

@router.get("/{id_usuario}", response_model=UsuarioResponse, status_code=status.HTTP_200_OK)
def obtener_usuario(
    id_usuario: int,
    usuario_actual: TokenData = Depends(obtener_usuario_actual)
):
    return usuario_service.obtener_usuario_por_id(id_usuario)

@router.put("/{id_usuario}", response_model=UsuarioResponse, status_code=status.HTTP_200_OK)
def actualizar_usuario(
    id_usuario: int,
    usuario: UsuarioUpdate,
    usuario_actual: TokenData = Depends(requerir_rol("ADMIN"))
):
    return usuario_service.actualizar_usuario(id_usuario, usuario)

@router.delete("/{id_usuario}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(
    id_usuario: int,
    usuario_actual: TokenData = Depends(requerir_rol("ADMIN"))
):
    usuario_service.eliminar_usuario(id_usuario)