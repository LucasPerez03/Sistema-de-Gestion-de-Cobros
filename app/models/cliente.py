class Cliente:
    def __init__(self, id_cliente, nombre, apellido, dni, email, telefono, fecha_nacimiento, fecha_alta=None, estado=True):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.email = email
        self.telefono = telefono
        self.fecha_nacimiento = fecha_nacimiento
        self.fecha_alta = fecha_alta
        self.estado = estado

    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"
    