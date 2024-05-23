from model.Boleta import Boleta


class Boleteria:
    def __init__(self):
        self.tickets = {}
        self.courtesies_sold = 0
        self.tickets_sold = 0

    def buscar(self, id):
        if id in self.tickets.keys():
            return True

    def add_ticket(self, nombre_comprador, metodo_pago, categoria, fase, precio, donde_conocio, id_ticket):
        self.tickets[id_ticket] = (Boleta(nombre_comprador, metodo_pago, categoria,fase, precio, donde_conocio))

