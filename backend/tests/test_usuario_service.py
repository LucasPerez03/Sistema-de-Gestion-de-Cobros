import unittest

from app.services.usuario_service import UsuarioService


class TestUsuarioService(unittest.TestCase):
    def setUp(self):
        self.service = UsuarioService()

    def test_hash_y_verificacion_de_password(self):
        password = "MiPassword123"

        hashed = self.service._hash_password(password)

        self.assertTrue(self.service._verificar_password(password, hashed))
        self.assertFalse(self.service._verificar_password("OtraPassword123", hashed))
        self.assertNotEqual(password, hashed)


if __name__ == "__main__":
    unittest.main()
