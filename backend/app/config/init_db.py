from backend.app.config.settings import settings
from backend.app.models.usuario import RolUsuario
from backend.app.repositories.usuario_repository import UsuarioRepository
from backend.app.services.usuario_service import UsuarioService

def init_admin() -> None:
    """Crea el usuario ADMIN inicial de forma idempotente si no existe."""
    usuario_repo = UsuarioRepository()
    usuario_service = UsuarioService()

    admin_existente = usuario_repo.obtener_por_email(settings.FIRST_SUPERUSER_EMAIL)
    if not admin_existente:
        password_hash = usuario_service._hash_password(settings.FIRST_SUPERUSER_PASSWORD)
        usuario_repo.crear({
            "email": settings.FIRST_SUPERUSER_EMAIL,
            "password": password_hash,
            "nombre": settings.FIRST_SUPERUSER_NOMBRE,
            "apellido": settings.FIRST_SUPERUSER_APELLIDO,
            "rol": RolUsuario.ADMIN.value,
            "estado": True,
            "id_cliente": None,
        })
        print(f"Usuario ADMIN inicial creado: {settings.FIRST_SUPERUSER_EMAIL}")