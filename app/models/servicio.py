class Servicio: 
    def __init__(self, id_servicio, nombre, precio, descripcion, estado=True):
        self.id_servicio = id_servicio
        self.nombre = nombre
        self.precio = precio
        self.descripcion = descripcion
        self.estado = estado
