from abc import ABC, abstractmethod
from typing import List, Optional
from contextlib import contextmanager
from psycopg2.extras import RealDictCursor


class BaseRepository(ABC):

    @staticmethod
    def _preparar_actualizacion(
        datos: dict, campos_permitidos: set[str]
    ) -> tuple[list[str], dict]:
        datos_validos = {
            clave: valor
            for clave, valor in datos.items()
            if clave in campos_permitidos and valor is not None
        }
        asignaciones = [
            f"{clave} = %({clave})s" for clave in datos_validos
        ]
        return asignaciones, datos_validos
    
    @abstractmethod
    def obtener_por_id(self, id_entidad: int) -> Optional[dict]:
        pass

    @abstractmethod
    def obtener_todos(self) -> List[dict]:
        pass

    @abstractmethod
    def crear(self, datos: dict) -> dict:
        pass

    @abstractmethod
    def actualizar(self, id_entidad: int, datos: dict) -> Optional[dict]:
        pass

    @abstractmethod
    def eliminar(self, id_entidad: int) -> bool:
        pass
    @contextmanager
    def transaccion(conn):
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                yield cursor
            conn.commit()
        except Exception:
            conn.rollback()
            raise