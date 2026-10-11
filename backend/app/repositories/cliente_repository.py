from typing import List, Optional
from psycopg2.extras import RealDictCursor
from backend.app.config.database import DatabaseConnection
from backend.app.repositories.base_repository import BaseRepository

class ClienteRepository(BaseRepository):
    _CAMPOS_ACTUALIZABLES = {
        "nombre", "apellido", "dni", "telefono", "email",
        "fecha_nacimiento", "estado",
    }

    def __init__(self):
        self.db = DatabaseConnection()

    def obtener_por_id(self, id_cliente: int) -> Optional[dict]:
        conn = self.db.get_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM clientes WHERE id_cliente = %s", (id_cliente,))
            return cursor.fetchone()

    def obtener_todos(self) -> List[dict]:
        conn = self.db.get_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM clientes ORDER BY id_cliente DESC")
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
        campos, parametros = self._preparar_actualizacion(
            datos, self._CAMPOS_ACTUALIZABLES
        )
        if not campos:
            return self.obtener_por_id(id_cliente)

        query = f"""
            UPDATE clientes 
            SET {", ".join(campos)}
            WHERE id_cliente = %(id_cliente)s
            RETURNING *
        """
        parametros["id_cliente"] = id_cliente
        conn = self.db.get_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, parametros)
            cliente_actualizado = cursor.fetchone()
            conn.commit()
            return cliente_actualizado

    def eliminar(self, id_cliente: int) -> bool:
        query = "UPDATE clientes SET estado = FALSE WHERE id_cliente = %s RETURNING id_cliente"
        conn = self.db.get_connection()
        with conn.cursor() as cursor:
            cursor.execute(query, (id_cliente,))
            eliminado = cursor.fetchone() is not None
            conn.commit()
            return eliminado