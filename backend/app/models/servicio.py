from decimal import Decimal

class Servicio:
    def __init__(
        self, 
        id_servicio: int, 
        nombre: str, 
        precio: Decimal, 
        descripcion: str, 
        estado: bool = True
    ):
        self.id_servicio = id_servicio
        self.nombre = nombre
        self.precio = Decimal(str(precio))
        self.precio_base = self.precio  
        self.descripcion = descripcion
        self.estado = estado

    def activar(self) -> None:
        self.estado = True

    def desactivar(self) -> None:
        self.estado = False
