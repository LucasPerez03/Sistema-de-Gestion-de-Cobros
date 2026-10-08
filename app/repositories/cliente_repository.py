from typing import List, Optional
from psycopg2.extras import RealDictCursor
from app.config.database import DatabaseConnection
from app.repositories.base_repository import BaseRepository

class ClienteRepository(BaseRepository):
    def __init__(self):
        self.db = DatabaseConnection()

    def obtener_por_id(self, id_cliente: int ) -> Optional[dict]:
        conn = self.db.get_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM clientes WHERE id_cliente = %s", (id_cliente,))
            return cursor.fetchone()

    def obtener_todos(self) -> List[dict]:
        conn = self.db.get_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM clientes WHERE estado = TRUE ORDER BY id_cliente")
            return cursor.fetchall()

    def crear(self, datos: dict) -> dict:
        query = """
            INSERT INTO clientes (nombre, apellido, dni, telefono, email, fecha_nacimiento)
            VALUES (%(nombre)s, %(apellido)s, %(dni)s, %(telefono)s, %(email)s, %(fecha_nacimiento)s)
            RETURNING *
        """
        conn = self.db.get_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, datos)
            nuevo_cliente = cursor.fetchone()
            conn.commit()
            return nuevo_cliente

    def actualizar(self, id_cliente: int, datos: dict) -> Optional[dict]:
        raise NotImplementedError("Actualizar clientes todavia no esta implementado.")

    def eliminar(self, id_cliente: int) -> bool:
        raise NotImplementedError("Eliminar clientes todavia no esta implementado")
