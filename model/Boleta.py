

class Boleta:
    def __init__(self, nombre_comprador, metodo_pago, categoria, fase, precio,donde_conocio, nombre_evento):
        self.nombre_evento = nombre_evento
        self.nombre_comprador = nombre_comprador
        self.metodo_pago = metodo_pago
        self.categoria = categoria
        self.fase = fase
        self.precio = precio
        self.donde_conocio = donde_conocio
        self.disponible_para_uso = True