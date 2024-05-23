

class User:
    def __init__(self, telefono, correo, direccion, id_boletas, nombre):
        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo
        self.direccion = direccion
        self.id_boletas = [id_boletas]
