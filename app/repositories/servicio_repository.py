from typing import List, Optional

from psycopg2.extras import RealDictCursor

from app.config.database import DatabaseConnection
from app.repositories.base_repository import BaseRepository


class ServicioRepository(BaseRepository):
    def __init__(self):
        self.db = DatabaseConnection()

    def obtener_por_id(self, id_servicio: int) -> Optional[dict]:
        conn = self.db.get_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT * FROM servicios WHERE id_servicio = %s",
                (id_servicio,),
            )
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
        raise NotImplementedError("Actualizar servicios todavía no está implementado.")

    def eliminar(self, id_servicio: int) -> bool:
        raise NotImplementedError("Eliminar servicios todavía no está implementado.")
