from abc import ABC, abstractmethod

class Usuario(ABC):
    def __init__(self, id_usuario, email, password ,nombre, apellido, rol, estado=True):
        self.id_usuario = id_usuario
        self.email = email
        self.password = password
        self.nombre = nombre
        self.apellido = apellido
        self.rol = rol
        self.estado = estado

@abstractmethod 
def obtener_menu(self):
    pass

class Admin(Usuario):
    def __init__(self, id_usuario, email, password, nombre, apellido, estado=True):
        super().__init__(id_usuario, email, password, nombre, apellido, 'ADMIN', estado)

    def obtener_menu(self):
        return ["Gestionar Usuarios", "Gestionar Servicios", "Registrar Pago", "Ver Reportes"]