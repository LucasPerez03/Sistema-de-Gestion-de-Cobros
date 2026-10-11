from typing import List, Optional

import bcrypt
from fastapi import HTTPException, status

from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.usuario import UsuarioCreate


class UsuarioService:
    def __init__(self):
        self.usuario_repo = UsuarioRepository()

    def _hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def _verificar_password(self, plainpassword: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plainpassword.encode("utf-8"), hashed_password.encode("utf-8"))

    def registrar_usuario(self, datos_usuario: UsuarioCreate) -> dict:
        usuario_existente = self.usuario_repo.obtener_por_email(datos_usuario.email)
        if usuario_existente: 
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya se encuentra registrado en el sistema."
            )

        datos_dict = datos_usuario.model_dump()
        datos_dict["password"] = self._hash_password(datos_usuario.password)

        datos_dict["estado"] = True

        nuevo_usuario = self.usuario_repo.crear(datos_dict)
        return nuevo_usuario

    def obtener_usuarios(self) -> List[dict]:
        return self.usuario_repo.obtener_todos()

    def obtener_usuario_por_id(self, id_usuario: int) -> dict:
        usuario = self.usuario_repo.obtener_por_id(id_usuario)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {id_usuario} no encontrado"
            )
        return usuario