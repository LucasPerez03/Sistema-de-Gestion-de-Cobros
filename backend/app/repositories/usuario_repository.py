from typing import List, Optional
from psycopg2.extras import RealDictCursor
from backend.app.config.database import DatabaseConnection
from backend.app.repositories.base_repository import BaseRepository

class UsuarioRepository(BaseRepository):
    _CAMPOS_ACTUALIZABLES = {
        "email", "password", "nombre", "apellido", "rol", "estado",
    }

    def __init__(self):
        self.db = DatabaseConnection()

    def obtener_por_id(self, id_usuario: int) -> Optional[dict]:
        conn = self.db.get_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT id_usuario, email, password, nombre, apellido, rol, estado FROM usuarios WHERE id_usuario = %s",
                (id_usuario,)
            )
            return cursor.fetchone()

    def obtener_por_email(self, email: str) -> Optional[dict]:
        conn = self.db.get_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT id_usuario, email, password, nombre, apellido, rol, estado FROM usuarios WHERE email = %s",
                (email,)
            )
            return cursor.fetchone()

    def obtener_todos(self) -> List[dict]:
        query = "SELECT id_usuario, email, nombre, apellido, rol, estado FROM usuarios ORDER BY id_usuario"
        conn = self.db.get_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def crear(self, datos: dict) -> dict:
        query = """
            INSERT INTO usuarios (email, password, nombre, apellido, rol, estado)
            VALUES (%(email)s, %(password)s, %(nombre)s, %(apellido)s, %(rol)s, %(estado)s)
            RETURNING id_usuario, email, nombre, apellido, rol, estado
        """
        conn = self.db.get_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, datos)
            nuevo_usuario = cursor.fetchone()
            conn.commit()

        if nuevo_usuario is None:
            raise RuntimeError("No se pudo crear el usuario.")

        return nuevo_usuario

    def actualizar(self, id_usuario: int, datos: dict) -> Optional[dict]:
        campos, parametros = self._preparar_actualizacion(
            datos, self._CAMPOS_ACTUALIZABLES
        )
        if not campos:
            return self.obtener_por_id(id_usuario)

        query = f"""
            UPDATE usuarios 
            SET {", ".join(campos)}
            WHERE id_usuario = %(id_usuario)s
            RETURNING id_usuario, email, nombre, apellido, rol, estado
        """
        parametros["id_usuario"] = id_usuario
        conn = self.db.get_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, parametros)
            usuario_actualizado = cursor.fetchone()
            conn.commit()
            return usuario_actualizado

    def eliminar(self, id_usuario: int) -> bool:
        query = "UPDATE usuarios SET estado = FALSE WHERE id_usuario = %s RETURNING id_usuario"
        conn = self.db.get_connection()
        with conn.cursor() as cursor:
            cursor.execute(query, (id_usuario,))
            eliminado = cursor.fetchone() is not None
            conn.commit()
            return eliminado