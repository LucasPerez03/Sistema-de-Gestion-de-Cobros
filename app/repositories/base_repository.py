from abc import ABC, abstractmethod
from typing import List, Optional

class BaseRepository(ABC):
   

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
