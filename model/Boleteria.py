from model.Boleta import Boleta


class Boleteria:
    def __init__(self):
        self.tickets = {}
        self.courtesies_sold = 0
        self.tickets_sold = 0

    def buscar(self, id):
        if id in self.tickets.keys():
            return True

    def get_total_tickets_add(self):
        return self.courtesies_sold + self.tickets_sold

    def add_ticket(self, nombre_comprador, metodo_pago, categoria, fase, precio, donde_conocio, id_ticket, nombre_evento):
        self.tickets[id_ticket] = (Boleta(nombre_comprador, metodo_pago, categoria, fase, precio,
                                          donde_conocio, nombre_evento))

        self.tickets_sold += 1


