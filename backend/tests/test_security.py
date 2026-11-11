import unittest
from datetime import timedelta
from unittest.mock import patch

from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from jose import jwt

from backend.app.config.security import create_access_token, get_current_user, requerir_rol
from backend.app.config.settings import settings
from backend.app.schemas.auth import RolUsuario, TokenData


class TestSecurity(unittest.TestCase):
    def _autenticar(self, token):
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
        return get_current_user(credentials)

    def test_create_access_token_y_decode(self):
        token = create_access_token(
            {"id_usuario": 1, "sub": "usuario@bypay.com", "rol": RolUsuario.ADMIN.value},
            timedelta(minutes=5),
        )

        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        self.assertEqual(payload["id_usuario"], 1)
        self.assertEqual(payload["sub"], "usuario@bypay.com")
        self.assertEqual(payload["rol"], RolUsuario.ADMIN.value)
        self.assertIn("exp", payload)

    def test_get_current_user_rejects_token_invalido(self):
        with self.assertRaises(HTTPException) as context:
            self._autenticar("token-invalido")

        self.assertEqual(context.exception.status_code, 401)

    @patch("backend.app.config.security.UsuarioRepository")
    def test_get_current_user_returns_token_data(self, usuario_repository):
        token = create_access_token(
            {"id_usuario": 2, "sub": "otro@bypay.com", "rol": RolUsuario.ADMIN.value},
        )
        usuario_repository.return_value.obtener_por_id.return_value = {
            "id_usuario": 2,
            "email": "otro@bypay.com",
            "rol": RolUsuario.CLIENTE.value,
            "id_cliente": 12,
            "estado": True,
        }

        current_user = self._autenticar(token)

        self.assertIsInstance(current_user, TokenData)
        self.assertEqual(current_user.id_usuario, 2)
        self.assertEqual(current_user.email, "otro@bypay.com")
        self.assertEqual(current_user.rol, RolUsuario.CLIENTE)
        self.assertEqual(current_user.id_cliente, 12)

    @patch("backend.app.config.security.UsuarioRepository")
    def test_get_current_user_rechaza_usuario_inactivo(self, usuario_repository):
        token = create_access_token(
            {"id_usuario": 2, "sub": "otro@bypay.com", "rol": RolUsuario.CLIENTE.value},
        )
        usuario_repository.return_value.obtener_por_id.return_value = {
            "id_usuario": 2,
            "email": "otro@bypay.com",
            "rol": RolUsuario.CLIENTE.value,
            "id_cliente": 12,
            "estado": False,
        }

        with self.assertRaises(HTTPException) as context:
            self._autenticar(token)

        self.assertEqual(context.exception.status_code, 401)

    def test_requerir_rol_rechaza_rol_no_permitido(self):
        dependency = requerir_rol([RolUsuario.ADMIN])
        usuario = TokenData(
            id_usuario=1,
            email="usuario@bypay.com",
            rol=RolUsuario.CLIENTE,
        )

        with self.assertRaises(HTTPException) as context:
            dependency(usuario)

        self.assertEqual(context.exception.status_code, 403)

    def test_requerir_rol_individual_rechaza_rol_no_permitido(self):
        dependency = requerir_rol(RolUsuario.ADMIN)
        usuario = TokenData(
            id_usuario=1,
            email="usuario@bypay.com",
            rol=RolUsuario.CLIENTE,
        )

        with self.assertRaises(HTTPException) as context:
            dependency(usuario)

        self.assertEqual(context.exception.status_code, 403)


if __name__ == "__main__":
    unittest.main()
