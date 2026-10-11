from abc import ABC, abstractmethod
from enum import Enum

class RolUsuario(str, Enum):
    ADMIN = "ADMIN"
    ENTRENADOR = "ENTRENADOR"
    CLIENTE = "CLIENTE"

class Usuario(ABC):
    def __init__(self, id_usuario: int, email: str, password_hash: str, nombre: str, apellido: str, rol: RolUsuario, estado: bool = True):
        self.id_usuario = id_usuario
        self.email = email
        self.password_hash = password_hash
        self.nombre = nombre
        self.apellido = apellido
        self.rol = rol
        self.estado = estado

    @abstractmethod
    def obtener_menu(self) -> list[str]:
        pass


class Admin(Usuario):
    def __init__(self, id_usuario: int, email: str, password_hash: str, nombre: str, apellido: str, estado: bool = True):
        super().__init__(id_usuario, email, password_hash, nombre, apellido, RolUsuario.ADMIN, estado)

    def obtener_menu(self) -> list[str]:
        return ["Gestionar Usuarios", "Gestionar Servicios", "Registrar Pago", "Ver Reportes"]


class Entrenador(Usuario):
    def __init__(self, id_usuario: int, email: str, password_hash: str, nombre: str, apellido: str, estado: bool = True):
        super().__init__(id_usuario, email, password_hash, nombre, apellido, RolUsuario.ENTRENADOR, estado)

    def obtener_menu(self) -> list[str]:
        return ["Consultar Clientes", "Registrar Pago", "Ver Cuotas"]


class ClienteUsuario(Usuario):
    def __init__(self, id_usuario: int, email: str, password_hash: str, nombre: str, apellido: str, id_cliente: int | None = None, estado: bool = True):
        super().__init__(id_usuario, email, password_hash, nombre, apellido, RolUsuario.CLIENTE, estado)
        self.id_cliente = id_cliente

    def obtener_menu(self) -> list[str]:
        return ["Ver Mis Cuotas", "Ver Historial de Pagos"]