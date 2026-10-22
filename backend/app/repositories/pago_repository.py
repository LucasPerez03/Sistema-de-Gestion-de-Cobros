from typing import List, Optional
from psycopg2.extras import RealDictCursor
from backend.app.config.database import DatabaseConnection

class PagoRepository:
    def __init__(self):
        self.db = DatabaseConnection()

    def obtener_todos(self) -> List[dict]:
        """Trae el historial completo de pagos (para ADMIN y ENTRENADOR)"""
        query = """
            SELECT 
                p.*,
                c.periodo,
                cl.nombre AS cliente_nombre,
                cl.apellido AS cliente_apellido,
                s.nombre AS servicio_nombre
            FROM pagos p
            JOIN cuotas c ON p.id_cuota = c.id_cuota
            JOIN clientes cl ON c.id_cliente = cl.id_cliente
            JOIN servicios s ON c.id_servicio = s.id_servicio
            ORDER BY p.fecha_pago DESC
        """
        conn = self.db.get_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def obtener_por_cliente(self, id_cliente: int) -> List[dict]:
        """Trae el historial de pagos de un cliente específico (para el rol CLIENTE)"""
        query = """
            SELECT 
                p.*,
                c.periodo,
                s.nombre AS servicio_nombre
            FROM pagos p
            JOIN cuotas c ON p.id_cuota = c.id_cuota
            JOIN servicios s ON c.id_servicio = s.id_servicio
            WHERE c.id_cliente = %s
            ORDER BY p.fecha_pago DESC
        """
        conn = self.db.get_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, (id_cliente,))
            return cursor.fetchall()

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