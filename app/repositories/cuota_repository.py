from typing import List, Optional

from psycopg2.extras import RealDictCursor

from app.config.database import DatabaseConnection
from app.repositories.base_repository import BaseRepository


class CuotaRepository(BaseRepository):
    def __init__(self):
        self.db = DatabaseConnection()

    def obtener_por_id(self, id_cuota: int) -> Optional[dict]:
        conn = self.db.get_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT * FROM cuotas WHERE id_cuota = %s",
                (id_cuota,),
            )
            return cursor.fetchone()

    def obtener_todos(self) -> List[dict]:
        conn = self.db.get_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM cuotas ORDER BY id_cuota")
            return cursor.fetchall()

    def obtener_por_cliente(self, id_cliente: int) -> List[dict]:
        conn = self.db.get_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT * FROM cuotas WHERE id_cliente = %s ORDER BY id_cuota",
                (id_cliente,),
            )
            return cursor.fetchall()

    def crear(self, datos: dict) -> dict:
        query = """
            INSERT INTO cuotas (
                id_cliente, id_servicio, periodo, importe,
                fecha_vencimiento, estado
            )
            VALUES (
                %(id_cliente)s, %(id_servicio)s, %(periodo)s, %(importe)s,
                %(fecha_vencimiento)s, %(estado)s
            )
            RETURNING *
        """
        conn = self.db.get_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, datos)
            cuota = cursor.fetchone()
            conn.commit()

        if cuota is None:
            raise RuntimeError("No se pudo crear la cuota.")

        return cuota

    def actualizar(self, id_cuota: int, datos: dict) -> Optional[dict]:
        raise NotImplementedError("Actualizar cuotas todavía no está implementado.")

    def eliminar(self, id_cuota: int) -> bool:
        raise NotImplementedError("Eliminar cuotas todavía no está implementado.")
