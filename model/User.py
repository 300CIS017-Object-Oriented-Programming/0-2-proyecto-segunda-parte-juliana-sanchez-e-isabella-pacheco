

class User:
    def __init__(self, telefono, correo, direccion, id_boletas, nombre):
        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo
        self.direccion = direccion
        self.id_boletas = id_boletas

    def tiene_evento(self, nombre_evento):
        eventos = list(self.id_boletas.keys())
        for boleta in eventos:
            if nombre_evento == boleta:
                return True
        return False

    def add_ids(self, info, nombre_evento):
        self.id_boletas[nombre_evento].append(info)

    def get_cantidad_boletas(self, nombre_evento):
        i = 0
        print(self.id_boletas)
        eventos = list(self.id_boletas.keys())
        print(eventos)
        for evento in eventos:
            if nombre_evento == evento:
                i += self.id_boletas[evento][-1] + 1
        return i

