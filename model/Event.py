from model.Boleteria import Boleteria
class Event:
    def __init__(self, nombre, fecha, hora_apertura, hora_show, ubicacion, ciudad, direccion, artistas):
        self.nombre = nombre
        self.fecha = fecha
        self.hora_apertura = hora_apertura
        self.hora_show = hora_show
        self.ubicacion = ubicacion
        self.ciudad = ciudad
        self.direccion = direccion
        self.estado = "Por realizar"
        self.artistas = artistas
        self.boleteria = Boleteria

    def add_boleta(self, nombre_comprador, metodo_pago, categoria, fase, precio, donde_conocio, id_ticket):
        self.boleteria.add_ticket(nombre_comprador, metodo_pago, categoria, fase, precio, donde_conocio, id_ticket)

    def actualizar(self, nombre=None, fecha=None, hora_apertura=None, hora_show=None, ubicacion=None, ciudad=None,
                   direccion=None, estado=None, categoria=None, artistas=None, costo_alquiler=None, tipo=None):
        if nombre is not None:
            self.nombre = nombre
        if fecha is not None:
            self.fecha = fecha
        if hora_apertura is not None:
            self.hora_apertura = hora_apertura
        if hora_show is not None:
            self.hora_show = hora_show
        if ubicacion is not None:
            self.ubicacion = ubicacion
        if ciudad is not None:
            self.ciudad = ciudad
        if direccion is not None:
            self.direccion = direccion
        if estado is not None:
            self.estado = estado
        if categoria is not None:
            self.categoria = categoria
        if artistas is not None:
            self.artistas = artistas
        if costo_alquiler is not None:
            self.costo_alquiler = costo_alquiler
        if tipo is not None:
            self.tipo = tipo
