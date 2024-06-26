from model.Event import Event

class EventPhilanthropic(Event):
    def __init__(self, nombre, fecha, hora_apertura, hora_show, ubicacion, ciudad, direccion,
                 artistas, sponsor_list, aforo):
        super().__init__(nombre, fecha, hora_apertura, hora_show, ubicacion, ciudad, direccion, artistas, aforo)
        self.sponsors = sponsor_list
        self.tipo = "filantropico"

    def update(self, nombre_nuevo, fecha_evento_nuevo, hora_apertura_nuevo,
               hora_show_nuevo, ubicacion_nuevo, ciudad_nuevo, direccion_nuevo, estado_nuevo, aforo_nuevo):
        if fecha_evento_nuevo != self.fecha:
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
        self.estado = estado_nuevo
        self.aforo = aforo_nuevo

    def get_total_pagado_artistas(self):
        total = 0
        for artista in list(self.artistas.values()):
            total += artista
        return total