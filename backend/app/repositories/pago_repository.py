from typing import List

from psycopg2.extras import RealDictCursor

from backend.app.config.database import DatabaseConnection


class PagoRepository:
    def __init__(self):
        self.db = DatabaseConnection()

    def obtener_por_cuota(self, id_cuota: int) -> List[dict]:
        conn = self.db.get_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT * FROM pagos WHERE id_cuota = %s ORDER BY fecha_pago DESC",
                (id_cuota,),
            )
            return cursor.fetchall()

    def crear(self, datos: dict) -> dict:
        query = """
            INSERT INTO pagos (
                id_cuota, id_usuario, monto, fecha_pago, medio_pago, comprobante_ref
            )
            VALUES (
                %(id_cuota)s, %(id_usuario)s, %(monto)s, CURRENT_TIMESTAMP,
                %(medio_pago)s, %(comprobante_ref)s
            )
            RETURNING *
        """
        conn = self.db.get_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, datos)
            nuevo_pago = cursor.fetchone()
            conn.commit()

        if nuevo_pago is None:
            raise RuntimeError("No se pudo registrar el pago.")

        return nuevo_pago