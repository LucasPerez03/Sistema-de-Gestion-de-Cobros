import unittest
from datetime import timedelta

from fastapi import HTTPException
from jose import jwt

from app.config.security import create_access_token, get_current_user
from app.config.settings import settings
from app.schemas.auth import TokenData


class TestSecurity(unittest.TestCase):
    def test_create_access_token_y_decode(self):
        token = create_access_token(
            {"id_usuario": 1, "sub": "usuario@bypay.com", "rol": "admin"},
            timedelta(minutes=5),
        )

        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        self.assertEqual(payload["id_usuario"], 1)
        self.assertEqual(payload["sub"], "usuario@bypay.com")
        self.assertEqual(payload["rol"], "admin")
        self.assertIn("exp", payload)

    def test_get_current_user_rejects_token_invalido(self):
        with self.assertRaises(HTTPException) as context:
            get_current_user("token-invalido")

        self.assertEqual(context.exception.status_code, 401)

    def test_get_current_user_returns_token_data(self):
        token = create_access_token(
            {"id_usuario": 2, "sub": "otro@bypay.com", "rol": "cliente"},
        )

        current_user = get_current_user(token)

        self.assertIsInstance(current_user, TokenData)
        self.assertEqual(current_user.id_usuario, 2)
        self.assertEqual(current_user.email, "otro@bypay.com")
        self.assertEqual(current_user.rol, "cliente")


if __name__ == "__main__":
    unittest.main()
