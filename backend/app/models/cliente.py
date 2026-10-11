from datetime import date
from typing import Optional

class Cliente:
    def __init__(
        self, 
        id_cliente: int, 
        nombre: str, 
        apellido: str, 
        dni: str, 
        email: str, 
        telefono: str, 
        fecha_nacimiento: date, 
        fecha_alta: Optional[date] = None, 
        estado: bool = True
    ):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.email = email
        self.telefono = telefono
        self.fecha_nacimiento = fecha_nacimiento
        self.fecha_alta = fecha_alta or date.today()
        self.estado = estado

    def nombre_completo(self) -> str:
        return f"{self.nombre} {self.apellido}"