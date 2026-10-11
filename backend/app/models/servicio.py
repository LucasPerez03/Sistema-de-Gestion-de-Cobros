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
        self.descripcion = descripcion
        self.estado = estado