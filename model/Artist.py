

class Artist:
    def __init__(self, nombre, evento):
        self.nombre = nombre
        self.eventos = [evento]

    def add_event(self, evento):
        self.eventos.append(evento)
