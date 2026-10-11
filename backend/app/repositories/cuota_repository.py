from typing import List, Optional
from psycopg2.extras import RealDictCursor
from backend.app.config.database import DatabaseConnection
from backend.app.repositories.base_repository import BaseRepository

class CuotaRepository(BaseRepository):
    _CAMPOS_ACTUALIZABLES = {
        "id_cliente", "id_servicio", "periodo", "importe",
        "fecha_vencimiento", "estado",
    }

    def __init__(self):
        self.db = DatabaseConnection()

    def obtener_por_id(self, id_cuota: int) -> Optional[dict]:
        conn = self.db.get_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM cuotas WHERE id_cuota = %s", (id_cuota,))
            return cursor.fetchone()

    def obtener_todos(self) -> List[dict]:
        conn = self.db.get_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM cuotas ORDER BY fecha_vencimiento DESC")
            return cursor.fetchall()

    def obtener_por_cliente(self, id_cliente: int) -> List[dict]:
        conn = self.db.get_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT * FROM cuotas WHERE id_cliente = %s ORDER BY fecha_vencimiento DESC",
                (id_cliente,)
            )
            return cursor.fetchall()

    def crear(self, datos: dict) -> dict:
        query = """
            INSERT INTO cuotas (id_cliente, id_servicio, periodo, importe, fecha_vencimiento, estado)
            VALUES (%(id_cliente)s, %(id_servicio)s, %(periodo)s, %(importe)s, %(fecha_vencimiento)s, %(estado)s)
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
        campos, parametros = self._preparar_actualizacion(
            datos, self._CAMPOS_ACTUALIZABLES
        )
        if not campos:
            return self.obtener_por_id(id_cuota)

        query = f"""
            UPDATE cuotas 
            SET {", ".join(campos)}
            WHERE id_cuota = %(id_cuota)s
            RETURNING *
        """
        parametros["id_cuota"] = id_cuota
        conn = self.db.get_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, parametros)
            cuota_actualizada = cursor.fetchone()
            conn.commit()
            return cuota_actualizada

    def eliminar(self, id_cuota: int) -> bool:
        query = """
            DELETE FROM cuotas AS cuota
            WHERE cuota.id_cuota = %s
              AND NOT EXISTS (
                  SELECT 1 FROM pagos WHERE pagos.id_cuota = cuota.id_cuota
              )
            RETURNING cuota.id_cuota
        """
        conn = self.db.get_connection()
        with conn.cursor() as cursor:
            cursor.execute(query, (id_cuota,))
            eliminado = cursor.fetchone() is not None
            conn.commit()
            return eliminado