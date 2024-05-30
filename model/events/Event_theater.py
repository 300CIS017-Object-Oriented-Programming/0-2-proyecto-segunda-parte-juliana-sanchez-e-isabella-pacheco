from model.Event import Event

class EventTheater(Event):
    def __init__(self, nombre, fecha, hora_apertura, hora_show, ubicacion, ciudad, direccion, categorias,
                 artistas, alquiler, porcentaje_preventa, aforo) -> None:
        super().__init__(nombre, fecha, hora_apertura, hora_show, ubicacion, ciudad, direccion, artistas, aforo)
        self.alquiler_price = alquiler
        self.categorias = categorias
        self.porcentaje_preventa = porcentaje_preventa/100
        self.estado_preventa = True

    def update(self, nombre_nuevo, fecha_evento_nuevo, hora_apertura_nuevo, hora_show_nuevo, ubicacion_nuevo,
               ciudad_nuevo, direccion_nuevo, estado_nuevo, costo_alquiler_nuevo, preventa, aforo_nuevo):
        if self.fecha != fecha_evento_nuevo:
            self.estado = "Aplazado"
        else:
            self.estado = estado_nuevo
        self.nombre = nombre_nuevo
        self.fecha = fecha_evento_nuevo
        self.hora_apertura = hora_apertura_nuevo
        self.hora_show = hora_show_nuevo
        self.ubicacion = ubicacion_nuevo
        self.ciudad = ciudad_nuevo
        self.direccion = direccion_nuevo
        self.alquiler_price = costo_alquiler_nuevo
        self.estado_preventa = preventa
        self.aforo = aforo_nuevo