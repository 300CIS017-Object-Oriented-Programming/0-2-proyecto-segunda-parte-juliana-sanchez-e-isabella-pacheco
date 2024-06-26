import streamlit as st
from controllers.gestion_controler import  GestionController
from view.main_view import (draw_admin_page, dibujar_eventos_creados, dibujar_crear_evento_bar,
                            dibujar_crear_evento_filantropico, dibujar_crear_evento_teatro,
                            dibujar_comprar_boletas, dibujar_generar_reporte, dibujar_verificar_asistencia, dibujar_dashboard)


class GUIController:
    def __init__(self):
        if 'my_state' not in st.session_state:
            self.run_page = 'main'
            self.gestion_controler = GestionController()
            st.session_state['my_state'] = self
        else:
            self.gestion_controler = st.session_state.my_state.gestion_controler
            self.run_page = st.session_state.my_state.run_page

    def main(self):
        if self.run_page == 'main':
            draw_admin_page(self)

    def get_artistas(self):
        artistas_names = self.gestion_controler.artist.keys()
        return list(artistas_names)

    def sidebar_option_menu(self, opcion_seleccionada):
        if opcion_seleccionada == "Ver eventos creados":
            dibujar_eventos_creados(self)
        elif opcion_seleccionada == "Crear evento Bar":
            dibujar_crear_evento_bar(self)
        elif opcion_seleccionada == "Crear evento Filantrópico":
            dibujar_crear_evento_filantropico(self)
        elif opcion_seleccionada == "Crear evento Teatro":
            dibujar_crear_evento_teatro(self)
        elif opcion_seleccionada == "Comprar boletas":
            dibujar_comprar_boletas(self)
        elif opcion_seleccionada == "Generar reporte":
            dibujar_generar_reporte(self)
        elif opcion_seleccionada == "Verificar asistencia":
            dibujar_verificar_asistencia(self)
        else:
            dibujar_dashboard(self)


    def generar_reporte(self, tipo_reporte, nombre, tipo):
        if tipo_reporte == "Reporte de los Artistas":
            self.gestion_controler.generar_reporte_artistas(tipo, nombre)
        elif tipo_reporte == "Reporte de Ventas":
            self.gestion_controler.generar_reporte_ventas()
        elif tipo_reporte == "Reporte Financiero":
            self.gestion_controler.generar_reporte_financiero(tipo, nombre)
        else:
            self.gestion_controler.generar_reporte_compradores()

    def get_nombres_eventos(self, opcion_seleccionada):
        if opcion_seleccionada == "Bar":
            eventos_name_list = self.gestion_controler.events_bar.keys()
        elif opcion_seleccionada == "Teatro":
            eventos_name_list = self.gestion_controler.events_theater.keys()
        else:
            eventos_name_list = self.gestion_controler.events_philanthropic.keys()

        nombres_eventos = list(eventos_name_list)

        if not nombres_eventos:
            st.warning(f"No hay eventos disponibles para el tipo '{opcion_seleccionada}'.")
            return None

        evento_seleccionado = st.selectbox("Selecciona el evento:", nombres_eventos)
        return evento_seleccionado

    def comprar_categoria(self, nombre_evento, opcion_seleccionada, cantidad_boletas):
        categoria_elegida = None
        if opcion_seleccionada != "Filantrópico":
            st.subheader("Selecciona la categoría:")
            categorias, porcentaje, aforo, vendidas, cortesia_total, cortesias_vendidas = (
                self.gestion_controler.mostrar_categorias(nombre_evento, opcion_seleccionada))

            nombre_categorias = list(categorias.keys())
            if cortesia_total <= cortesias_vendidas:
                if "cortesia" in nombre_categorias:
                    nombre_categorias.remove("cortesia")
            categoria_elegida = st.selectbox("Categoría:", nombre_categorias)
            # Obtener el costo de la categoría seleccionada
            costo_categoria = categorias[categoria_elegida]
            total = cantidad_boletas * costo_categoria
            total -= total * porcentaje
            if porcentaje > 0:
                st.write(f"Se le está aplicando un {porcentaje * 100}% de descuento por estar comprando en preventa")
            st.write(f"Total a pagar: ${total}")
        else:
            st.write("Entrada gratuita")
            return "Filantrópico"  # DEBUG (CORREGIR)

        if categoria_elegida != "cortesia" and cantidad_boletas + vendidas > aforo:
            st.warning("Se están tratando de comprar más boletas de las disponibles")
            return None
        elif categoria_elegida == "cortesia" and cantidad_boletas + cortesias_vendidas > cortesia_total:
            st.warning("Se están tratando de comprar más cortesías de las disponibles")
            return None

        return categoria_elegida

    def get_ubicacion(self, nombre_evento, tipo):
        return self.gestion_controler.get_ubicacion(tipo, nombre_evento)

    def guardar_info_boletas(self, nombre_comprador, telefono, correo, direccion, evento_seleccionado,
                            cantidad_boletas, donde_conocio, metodo_pago, categoria, tipo):
        id_boletas = self.gestion_controler.guardar_boletas(nombre_comprador, tipo, evento_seleccionado,
                                                            cantidad_boletas, donde_conocio, metodo_pago, categoria)
        self.gestion_controler.guardar_user_info(evento_seleccionado, nombre_comprador, telefono, correo, direccion, id_boletas)

    def get_info_clientes(self, nombre_evento):
        info_clientes = self.gestion_controler.get_info_clientes(nombre_evento)
        return info_clientes

    def filtrar_eventos_guardados(self, opcion_seleccionada):
        eventos_filtrados = self.gestion_controler.get_events(opcion_seleccionada)
        list_names = []
        if eventos_filtrados:
            for evento in eventos_filtrados.values():
                st.write("Nombre:", evento.nombre)
                st.write("Ubicación:", evento.ubicacion)
                st.write("Fecha:", evento.fecha)
                st.write("Estado:", evento.estado)
                st.write("Aforo:", evento.aforo)
                st.write("Boletas vendidas:", evento.get_total_tickets_add())
                if opcion_seleccionada == "Bar" or opcion_seleccionada == "Teatro":
                    st.write("Cortesias Disponibles:", evento.total_cortesias - evento.get_cortesias_vendidas())
                # Verificar si el estado del evento es "realizado"
                if evento.estado != "Realizado" and evento.estado != "Cancelado":
                    list_names.append(evento.nombre)
                    # Mostrar botón de editar

                else:
                    st.write("El evento ya está realizado y no se puede editar.")
                st.write("---")
        return list_names

    def get_event_info(self, tipo, nombre):
        eventos = self.gestion_controler.get_events(tipo)
        event_info = None
        if eventos:
            evento = eventos[nombre]
            alquiler = 0
            if tipo == "teatro":
                alquiler = evento.alquiler
            event_info = {
                "nombre": evento.nombre,
                "ubicacion": evento.ubicacion,
                "fecha": evento.fecha,
                "estado": evento.estado,
                "hora_apertura": evento.hora_apertura,
                "hora_show": evento.hora_show,
                "alquiler": alquiler,
                "ciudad": evento.ciudad,
                "direccion": evento.direccion,
                "aforo": evento.aforo,
                "preventa": evento.estado_preventa == "Preventa"
            }
            print(evento.estado_preventa == "Preventa")
        return event_info

