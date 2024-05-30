import streamlit as st

from view.reporte import (generar_reporte_artistas, generar_reporte_ventas, generar_reporte_financiero_bar,
                          generar_reporte_financiero_teatro, generar_reporte_financiero_filantropico,
                          generar_reporte_compradores)
from model.events.Event_bar import EventBar 
from model.events.Event_philanthropic import EventPhilanthropic
from model.events.Event_theater import EventTheater
from model.Artist import Artist
from model.User import User


class GestionController:
    def __init__(self):
        self.events_bar = {}
        self.events_theater = {}
        self.events_philanthropic = {}
        self.artist = {}
        self.users = {}
        self.letra = "a"

    def guardar_user_info(self, nombre_comprador, telefono, correo, direccion,id_boletas):
        if nombre_comprador not in self.users.keys():
            self.users[nombre_comprador] = User(telefono, correo, direccion, id_boletas, nombre_comprador)
        else:
            self.users[nombre_comprador].id_boletas.append(id_boletas)

    def generar_reporte_artistas(self, nombre_artista):
        artista = self.artist[nombre_artista]
        eventos_list = artista.get_eventos()
        info_evento = {}
        for evento in eventos_list:
            info_evento[evento] = [evento.get_info()]
        generar_reporte_artistas(nombre_artista, info_evento)

    def generar_reporte_ventas(self, nombre_evento, tipo_evento):
        evento = None
        if tipo_evento == 'bar':
            evento = self.events_bar[nombre_evento]
        elif tipo_evento == 'theater':
            evento = self.events_theater[nombre_evento]
        vendidas, ingresos_preventa, ingresos_regular = evento.get_boleteria_info()
        generar_reporte_ventas(vendidas, ingresos_preventa, ingresos_regular, nombre_evento)

    def generar_reporte_financiero(self, nombre_evento, tipo_evento):
        if tipo_evento == 'bar':
            evento = self.events_bar[nombre_evento]
            ingresos_metodo_pago, ingresos_categorias, pago_artistas = evento.get_financiero_info()
            generar_reporte_financiero_bar(ingresos_metodo_pago, ingresos_categorias, pago_artistas, nombre_evento)
        elif tipo_evento == 'theater':
            evento = self.events_theater[nombre_evento]
            ingresos_metodo_pago, ingresos_categorias, alquiler = evento.get_financiero_info()
            generar_reporte_financiero_teatro(ingresos_metodo_pago, ingresos_categorias,alquiler,nombre_evento)
        else:
            evento = self.events_philanthropic[nombre_evento]
            patrocinadores = evento.get_financiero_info()
            generar_reporte_financiero_filantropico(patrocinadores, nombre_evento)

    def generar_reporte_compradores(self, nombre_evento, tipo_evento):
        compradores_list = []
        for comprador in self.users:
            id_boletas_list = comprador.id_boletas
            if nombre_evento in id_boletas_list.keys():
                compradores_list.append(comprador)
        generar_reporte_compradores(compradores_list, nombre_evento)

    def guardar_artistas(self, artistas, nombre_evento):
        artista_name_list = []
        artista_dict = {}
        for artista in artistas:
            flag = False
            artista_name_list.append(artista["nombre"])
            artista_dict[artista["nombre"]] = artista["tarifa"]
            for artista_guardado in self.artist.values():
                if artista_guardado.nombre == artista["nombre"]:
                    artista_guardado.add_event(nombre_evento)
                    flag = True
            if not flag:
                self.artist[artista["nombre"]] = (Artist(artista["nombre"], nombre_evento))
        return artista_name_list, artista_dict

    def mostrar_categorias(self, nombre_evento, tipo):
        if tipo == "Bar":
            evento = self.events_bar[nombre_evento]
        else:
            evento = self.events_theater[nombre_evento]
        porcentaje = 1
        if evento:
            if evento.estado_preventa:
                porcentaje = evento.porcentaje_preventa
            return (evento.categorias, porcentaje, evento.aforo, evento.get_total_tickets_add(),
                    evento.total_cortesias, evento.get_cortesias_vendidas())
        else:
            return None


    def get_info_clientes(self, nombre_evento):
        clientes = list(self.users.values())
        info_clientes = []
        for cliente in clientes:
            if cliente.tiene_evento(nombre_evento):
                dic = {
                    "nombre": cliente.nombre,
                    "cantidad": cliente.get_cantidad_boletas(nombre_evento),
                }
                info_clientes.append(dic)
        return info_clientes
    def guardar_boletas(self, nombre_comprador, tipo, evento_seleccionado, cantidad_boletas,
                        donde_conocio, metodo_pago, categoria):
        evento = None
        id_list = {}
        id_list[evento_seleccionado] = []
        if tipo == "Bar":
            evento = self.events_bar[evento_seleccionado]
        elif tipo == "Teatro":
            evento = self.events_theater[evento_seleccionado]
        precio = evento.categorias[categoria]
        if evento.estado_preventa:
            fase = "Preventa"
            precio -= precio*evento.porcentaje_preventa
        else:
            fase = "Regular"
        id_initial = evento.get_total_tickets_add()
        for i in range(cantidad_boletas):
            id_list[evento_seleccionado].append(id_initial + i)
            evento.add_boleta(nombre_comprador, metodo_pago, categoria,
                              fase, precio, donde_conocio, id_initial+i, evento_seleccionado)
        if evento.get_total_tickets_add() == evento.aforo:
            evento.update_status("Cerrado")
        return id_list

    def get_ubicacion(self, tipo, nombre_evento):
        if tipo == "Bar":
            evento = self.events_bar[nombre_evento]
        elif tipo == "Teatro":
            evento = self.events_theater[nombre_evento]
        else:
            evento = self.events_philanthropic[nombre_evento]
        return evento.ubicacion

    def editar_evento_bar(self, nombre_pasado, fecha_evento_nuevo,
                          hora_apertura_nuevo, hora_show_nuevo, ubicacion_nuevo, ciudad_nuevo,
                          direccion_nuevo, estado_nuevo, preventa, aforo_nuevo):
        evento = self.events_bar[nombre_pasado]
        if aforo_nuevo < evento.get_total_tickets_add():
            st.warning("El aforo no puede ser menor  la cantidad de boletas que ya se han vendido")
        elif evento.estado_preventa() > 0 and estado_nuevo == "Cancelado":
            st.warning("No se puede cancelar un evento con boleteria vendida")
        else:
            evento.update(nombre_pasado, fecha_evento_nuevo, hora_apertura_nuevo,
                          hora_show_nuevo, ubicacion_nuevo, ciudad_nuevo, direccion_nuevo, estado_nuevo, preventa, aforo_nuevo)

    def editar_evento_teatro(self, nombre_pasado, fecha_evento_nuevo, hora_apertura_nuevo, hora_show_nuevo,
                             ubicacion_nuevo, ciudad_nuevo, direccion_nuevo, estado_nuevo, costo_alquiler_nuevo, aforo_nuevo):
        evento = self.events_theater[nombre_pasado]
        if aforo_nuevo < evento.get_total_tickets_add():
            st.warning("El aforo no puede ser menor  la cantidad de boletas que ya se han vendido")
        elif evento.estado_preventa() > 0 and estado_nuevo == "Cancelado":
            st.warning("No se puede cancelar un evento con boleteria vendida")
        else:
            evento.update(nombre_pasado, fecha_evento_nuevo, hora_apertura_nuevo, hora_show_nuevo,
                          ubicacion_nuevo, ciudad_nuevo, direccion_nuevo, estado_nuevo, costo_alquiler_nuevo, aforo_nuevo)

    def editar_evento_filantropico(self,nombre_pasado, fecha_evento_nuevo,
                          hora_apertura_nuevo, hora_show_nuevo, ubicacion_nuevo, ciudad_nuevo,
                          direccion_nuevo, estado_nuevo, aforo_nuevo):
        evento = self.events_philanthropic[nombre_pasado]
        if aforo_nuevo < evento.get_total_tickets_add():
            st.warning("El aforo no puede ser menor  la cantidad de boletas que ya se han vendido")
        elif evento.estado_preventa() > 0 and estado_nuevo == "Cancelado":
            st.warning("No se puede cancelar un evento con boleteria vendida")
        else:
            evento.update(nombre_pasado, fecha_evento_nuevo, hora_apertura_nuevo,
                          hora_show_nuevo, ubicacion_nuevo, ciudad_nuevo, direccion_nuevo, estado_nuevo, aforo_nuevo)

    def crear_evento_bar(self, nombre_evento, fecha_evento, hora_apertura,
                         hora_show, ubicacion, ciudad, direccion, categorias, artistas, porcentaje_preventa, aforo, total_cortesias):
        aux, artista_dict = self.guardar_artistas(artistas, nombre_evento)
        evento = EventBar(nombre_evento, fecha_evento, hora_apertura, hora_show,
                          ubicacion, ciudad, direccion, categorias, artista_dict, porcentaje_preventa, aforo, total_cortesias)
        self.events_bar[nombre_evento] = evento

    def get_events(self, tipo):
        if tipo == "Bar":
            eventos = self.events_bar
        elif tipo == "Filantrópico":
            eventos= self.events_philanthropic
        else:
            eventos = self.events_theater

        if eventos:
            return eventos
        else:
            st.write("No se han encontrado eventos")
            return None

    def crear_evento_filantropico(self, nombre_evento, fecha_evento, hora_apertura,
                                  hora_show, ubicacion, ciudad, direccion, patrocinadores, artistas,aforo):
        artista_name_list, aux = self.guardar_artistas(artistas, nombre_evento)
        self.events_philanthropic[nombre_evento] = \
            (EventPhilanthropic(nombre_evento, fecha_evento, hora_apertura, hora_show,
                                ubicacion, ciudad, direccion, artista_name_list, patrocinadores,aforo))

    def crear_evento_teatro(self, nombre_evento, fecha_evento, hora_apertura, hora_show,
                            ubicacion, ciudad, direccion, categorias, artistas, costo_alquiler, porcentaje_preventa,
                            aforo, total_cortesias):
        artista_name_list, aux = self.guardar_artistas(artistas, nombre_evento)
        self.events_theater[nombre_evento] = \
            (EventTheater(nombre_evento, fecha_evento, hora_apertura, hora_show,
                          ubicacion, ciudad, direccion, categorias, artista_name_list, costo_alquiler,
                          porcentaje_preventa, aforo, total_cortesias))


