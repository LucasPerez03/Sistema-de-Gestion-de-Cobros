from typing import List, Optional
from psycopg2.extras import RealDictCursor
from backend.app.config.database import DatabaseConnection
from backend.app.repositories.base_repository import BaseRepository

class ServicioRepository(BaseRepository):
    _CAMPOS_ACTUALIZABLES = {"nombre", "precio", "descripcion", "estado"}

    def __init__(self):
        self.db = DatabaseConnection()

    def obtener_por_id(self, id_servicio: int) -> Optional[dict]:
        conn = self.db.get_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM servicios WHERE id_servicio = %s", (id_servicio,))
            return cursor.fetchone()

    def obtener_todos(self) -> List[dict]:
        conn = self.db.get_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM servicios ORDER BY id_servicio")
            return cursor.fetchall()

    def crear(self, datos: dict) -> dict:
        query = """
            INSERT INTO servicios (nombre, precio, descripcion, estado)
            VALUES (%(nombre)s, %(precio)s, %(descripcion)s, %(estado)s)
            RETURNING *
        """
        conn = self.db.get_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, datos)
            servicio = cursor.fetchone()
            conn.commit()

        if servicio is None:
            raise RuntimeError("No se pudo crear el servicio.")

        return servicio

    def actualizar(self, id_servicio: int, datos: dict) -> Optional[dict]:
        campos, parametros = self._preparar_actualizacion(
            datos, self._CAMPOS_ACTUALIZABLES
        )
        if not campos:
            return self.obtener_por_id(id_servicio)

        query = f"""
            UPDATE servicios 
            SET {", ".join(campos)}
            WHERE id_servicio = %(id_servicio)s
            RETURNING *
        """
        parametros["id_servicio"] = id_servicio
        conn = self.db.get_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, parametros)
            servicio_actualizado = cursor.fetchone()
            conn.commit()
            return servicio_actualizado

    def eliminar(self, id_servicio: int) -> bool:
        query = "UPDATE servicios SET estado = FALSE WHERE id_servicio = %s RETURNING id_servicio"
        conn = self.db.get_connection()
        with conn.cursor() as cursor:
            cursor.execute(query, (id_servicio,))
            eliminado = cursor.fetchone() is not None
            conn.commit()
            return eliminado