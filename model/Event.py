from model.Boleteria import Boleteria
class Event:
    def __init__(self, nombre, fecha, hora_apertura, hora_show, ubicacion, ciudad, direccion, artistas, aforo_):
        self.nombre = nombre
        self.fecha = fecha
        self.hora_apertura = hora_apertura
        self.hora_show = hora_show
        self.ubicacion = ubicacion
        self.ciudad = ciudad
        self.direccion = direccion
        self.estado = "Por realizar"
        self.artistas = artistas
        self.boleteria = Boleteria()
        self.aforo = aforo_

    def add_boleta(self, nombre_comprador, metodo_pago, categoria, fase, precio, donde_conocio, id_ticket, nombre_evento):
        self.boleteria.add_ticket(nombre_comprador, metodo_pago, categoria, fase, precio, donde_conocio, id_ticket, nombre_evento)

    def get_total_tickets_add(self):
        return self.boleteria.get_total_tickets_add()

    def get_cortesias_vendidas(self):
        return  self.boleteria.courtesies_sold


