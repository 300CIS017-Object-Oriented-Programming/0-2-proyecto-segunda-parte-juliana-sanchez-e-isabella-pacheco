import pytest
from controllers.gestion_controler import GestionController
def test_probar_evento():
    gestion_controler = GestionController()

    gestion_controler.crear_evento_bar("NOMBRE", "FECHA", "HORA_APER", "HORA_SHOW",
                                       "UBICACION", "CALI",  "Direccion", {}, {}, 0, 0, 0)

    ciudad = gestion_controler.events_bar["NOMBRE"].ciudad
    assert ciudad == "CALI"

def test_probar_evento2():
    gestion_controler = GestionController()
    gestion_controler.crear_evento_teatro("EVENTITO", "FECHA", "HORA_APER", "HORA_SHOW",
                                       "UBICACION", "CALI", "Direccion", {}, {}, 100, 0, 0, 0)

    pago = gestion_controler.events_theater["EVENTITO"].alquiler_price
    assert pago == 100