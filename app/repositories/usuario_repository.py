from typing import List, Optional
from psycopg2.extras import RealDictCursor
from app.config.database import DatabaseConnection
from app.repositories.base_repository import BaseRepository

class UsuarioRepository(BaseRepository):
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
        """Método específico de UsuarioRepository (no está en BaseRepository)"""
        conn = self.db.get_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT id_usuario, email, password, nombre, apellido, rol, estado FROM usuarios WHERE email = %s",
                (email,)
            )
            return cursor.fetchone()

    def obtener_todos(self) -> List[dict]:
        query = """
            SELECT id_usuario, email, nombre, apellido, rol, estado
            FROM usuarios
            ORDER BY id_usuario
        """
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
        raise NotImplementedError("Actualizar usuarios todavía no está implementado.")

    def eliminar(self, id_usuario: int) -> bool:
        raise NotImplementedError("Eliminar usuarios todavía no está implementado.")