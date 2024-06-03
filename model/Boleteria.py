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
        if categoria == "cortesia":
            self.courtesies_sold += 1
        else:
            self.tickets_sold += 1

    def get_boletas_info(self):
        boletas_info = []
        for ticket in list(self.tickets.values()):
            aux = {
                "preventa": ticket.fase == "Preventa",
                "precio": ticket.precio,
                "categoria": ticket.categoria
                }
            boletas_info.append(aux)
        return boletas_info

    def get_ingreso(self):
        ingreso = 0
        for ticket in self.tickets.values():
            ingreso += ticket.precio
        return ingreso

