class Event:
    def __init__(self, nombre_evento, fecha_evento, hora_apertura, hora_show,
                 ubicacion, ciudad, direccion, categorias, artista_dict, porcentaje_preventa):
        self.nombre_evento = nombre_evento
        self.fecha_evento = fecha_evento
        self.hora_apertura = hora_apertura
        self.hora_show = hora_show
        self.ubicacion = ubicacion
        self.ciudad = ciudad
        self.direccion = direccion
        self.categorias = categorias
        self.artista_dict = artista_dict
        self.porcentaje_preventa = porcentaje_preventa

class EventBar(Event):
    def __init__(self, nombre_evento, fecha_evento, hora_apertura, hora_show,
                 ubicacion, ciudad, direccion, categorias, artista_dict, porcentaje_preventa):
        super().__init__(nombre_evento, fecha_evento, hora_apertura, hora_show,
                         ubicacion, ciudad, direccion, categorias, artista_dict, porcentaje_preventa)
        # Aquí puedes agregar propiedades o métodos específicos para EventBar
        self.tipo_evento = 'Bar'

class EventManager:
    def __init__(self):
        self.events_bar = {}

    def add_event(self, nombre_evento, fecha_evento, hora_apertura, hora_show,
                  ubicacion, ciudad, direccion, categorias, artista_dict, porcentaje_preventa):
        event = EventBar(
            nombre_evento, fecha_evento, hora_apertura, hora_show,
            ubicacion, ciudad, direccion, categorias, artista_dict, porcentaje_preventa
        )
        self.events_bar[nombre_evento] = event

    def get_event(self, nombre_evento):
        return self.events_bar.get(nombre_evento, None)

# Ejemplo de uso:
manager = EventManager()

# Agregar un evento
manager.add_event(
    "Concierto 2024", "2024-06-01", "18:00", "20:00",
    "Estadio", "New York", "123 Calle Principal", ["Música", "En Vivo"],
    {"artista_principal": "Nombre del Artista"}, 50
)

# Verificar si el evento se ha guardado correctamente
evento = manager.get_event("Concierto 2024")
if evento:
    print(f"Evento guardado: {evento.nombre_evento}")
else:
    print("El evento no se ha guardado.")
