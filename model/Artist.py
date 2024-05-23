

class Artist:
    def __init__(self, nombre,evento):
        self.nombre = nombre
        self.eventos = [evento]
    def agregar_evento(self, evento):
        self.eventos.append(evento)
