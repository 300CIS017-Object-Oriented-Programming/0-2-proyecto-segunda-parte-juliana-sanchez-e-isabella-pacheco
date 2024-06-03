import streamlit as st
from streamlit_option_menu import option_menu

from controllers import gui_controler
from settings import LOGO_HTML_CONFIG, IMAGE_PATH_TICKETS, URL_IMAGES
import time
import os
import random
import string
import zipfile
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt


def dibujar_dashboard(gui_controler):
    st.subheader("Dashboard")

    # Selección de intervalo de fechas
    fecha_inicio = st.date_input("Fecha de inicio")
    fecha_fin = st.date_input("Fecha de fin")

    if fecha_inicio > fecha_fin:
        st.error("La fecha de inicio no puede ser posterior a la fecha de fin.")
        return

    # Obtener eventos creados en el intervalo seleccionado
    eventos_bar = [evento for evento in gui_controler.gestion_controler.events_bar.values() if fecha_inicio <= evento.fecha <= fecha_fin]
    eventos_filantropicos = [evento for evento in gui_controler.gestion_controler.events_philanthropic.values() if fecha_inicio <= evento.fecha <= fecha_fin]
    eventos_teatro = [evento for evento in gui_controler.gestion_controler.events_theater.values() if fecha_inicio <= evento.fecha <= fecha_fin]


    if eventos_bar or eventos_filantropicos or eventos_teatro:
        st.write("Eventos creados en el intervalo seleccionado:")
        for evento in eventos_bar:
            st.write(f"Nombre: {evento.nombre}, Tipo: Bar, Ingresos: {evento.get_ingreso()}")
        for evento in eventos_filantropicos:
            st.write(f"Nombre: {evento.nombre}, Tipo: Filantrópico, Ingresos: {evento.get_ingreso()}")
        for evento in eventos_teatro:
            st.write(f"Nombre: {evento.nombre}, Tipo: Teatro, Ingresos: {evento.get_ingreso()}")
    else:
        st.write("No hay eventos creados en el intervalo seleccionado.")


    nombres_eventos = [evento.nombre for evento in eventos_bar + eventos_filantropicos + eventos_teatro]
    ingresos_eventos = [evento.get_ingreso() for evento in eventos_bar + eventos_filantropicos + eventos_teatro]

    plt.bar(nombres_eventos, ingresos_eventos)
    plt.xlabel("Evento")
    plt.ylabel("Ingresos")
    plt.title("Ingresos por Evento")
    plt.xticks(rotation=45, ha='right')
    st.pyplot(plt)


    tipos_eventos = ["Bar", "Filantrópico", "Teatro"]
    num_eventos = [len(eventos_bar), len(eventos_filantropicos), len(eventos_teatro)]

    plt.bar(tipos_eventos, num_eventos)
    plt.xlabel("Tipo de Evento")
    plt.ylabel("Número de Eventos")
    plt.title("Número de Eventos por Tipo")
    st.pyplot(plt)

def navegation_sidebar(gui_controler):
    with st.sidebar:
        opcion_seleccionada = option_menu("Navegación",
                                          ["Ver eventos creados", "Crear evento Bar",
                                           "Crear evento Filantrópico", "Crear evento Teatro",
                                           "Comprar boletas", "Generar reporte", "Verificar asistencia", "Dashboard"], orientation="vertical")
    gui_controler.sidebar_option_menu(opcion_seleccionada)


def draw_admin_page(gui_controler):
    st.markdown(LOGO_HTML_CONFIG, unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;'>Bienvenido a Gonzalo Shows</h1>", unsafe_allow_html=True) 
    st.markdown("<h3 style='font-weight:500;text-align: center;'>"
                "Gracias por usar nuestro software, ¿Qué deseas hacer?</h2>", unsafe_allow_html=True)
    navegation_sidebar(gui_controler)


def dibujar_eventos_creados(gui_controler):
    st.subheader("Eventos Creados")

    col1, col2 = st.columns(2)

    with col1:
        tipo_evento_seleccionado = st.radio("Selecciona el tipo de evento:",
                                        ["Filantrópico", "Bar", "Teatro"])
        list_nombres = gui_controler.filtrar_eventos_guardados(tipo_evento_seleccionado)

    with col2:
        # Selectbox con los nombres obtenidos de list_nombres
        nombre = st.selectbox("Escoge el evento a Editar", list_nombres)
        event_info = gui_controler.get_event_info(tipo_evento_seleccionado, nombre)
        if event_info is not None:
            dibujar_editar_evento(gui_controler, event_info,
                                  tipo_evento_seleccionado)
        else:
            st.warning(
                "No se encontró información para el evento seleccionado. Por favor, elige otro evento :("
            )



def dibujar_editar_evento(gui_controler, evento, tipo):
    nombre = evento["nombre"]
    st.subheader(f"Editar Evento {nombre}")

    # Campos de entrada para editar la información del evento

    fecha_evento_input = st.date_input("Fecha del evento", value=evento["fecha"], key="fecha_evento")

    hora_apertura_input = st.time_input("Hora de apertura", value=evento["hora_apertura"], key="hora_apertura_evento")

    hora_show_input = st.time_input("Hora del show", value=evento["hora_show"], key="hora_show_evento")

    ubicacion_input = st.text_input("Ubicación del evento", value=evento["ubicacion"], key="ubicacion_evento")

    ciudad_input = st.text_input("Ciudad del evento", value=evento["ciudad"], key="ciudad_evento")

    direccion_input = st.text_input("Dirección", value=evento["direccion"], key="direccion_evento")

    aforo_input = st.number_input("Aforo", value=evento["aforo"], key="aforo_evento")

    estado_input = st.selectbox("Estado del evento", ["Realizado", "Por realizar", "Cancelado", "Aplazado", "Cerrado"],
                          index=["Realizado", "Por realizar", "Cancelado", "Aplazado", "Cerrado"].index(
                              evento["estado"].capitalize()), key="estado_evento")

    if tipo != "Filantropico":
        preventa_estado_input = st.checkbox("Preventa", value=evento["preventa"])

    # Solo permitir editar el costo del alquiler para eventos de tipo "Teatro"
    if tipo == "Teatro":
        costo_alquiler_input = st.number_input("Costo alquiler", value=float(evento["alquiler"]), min_value=0.0)
        evento["alquiler"] = costo_alquiler_input

    # Guardar los cambios si se hace clic en el botón
    submit_button = st.button(label="Guardar cambios")
    if submit_button:
        if tipo == "Teatro":
            gui_controler.gestion_controler.editar_evento_teatro(nombre, fecha_evento_input,
                                               hora_apertura_input, hora_show_input, ubicacion_input, ciudad_input,
                                               direccion_input, estado_input, costo_alquiler_input, preventa_estado_input, aforo_input)
        elif tipo == "Bar":
            gui_controler.gestion_controler.editar_evento_bar(nombre, fecha_evento_input,
                                            hora_apertura_input, hora_show_input, ubicacion_input, ciudad_input,
                                            direccion_input, estado_input, preventa_estado_input, aforo_input)
            st.write("Bar guardado")
        else:
            gui_controler.gestion_controler.editar_evento_filantropico(nombre, fecha_evento_input,
                                                     hora_apertura_input, hora_show_input, ubicacion_input, ciudad_input,
                                                     direccion_input, estado_input, aforo_input)

        st.success("¡Evento actualizado exitosamente!")



def dibujar_crear_evento_filantropico(gui_controler):
    st.subheader("Crear Evento Filantrópico")

    nombre_evento = st.text_input("Nombre del evento")
    fecha_evento = st.date_input("Fecha del evento")
    hora_apertura = st.time_input("Hora de apertura")
    hora_show = st.time_input("Hora del show")
    ubicacion = st.text_input("Ubicación del evento")
    ciudad = st.text_input("Ciudad del evento")
    direccion = st.text_input("Dirección")
    num_patrocinadores = st.number_input("Número de patrocinadores", min_value=1, value=1)
    aforo = st.number_input("Aforo", min_value=1, value=1)
    patrocinadores = {}
    for i in range(num_patrocinadores):
        nombre_patrocinador = st.text_input(f"Nombre del patrocinador {i+1}")
        aporte_patrocinador = st.number_input(f"Aporte del patrocinador {i+1}", min_value=0.0)
        patrocinadores[nombre_patrocinador] = aporte_patrocinador

    num_artistas = st.number_input("Número de artistas participantes", min_value=1, value=1)
    artistas = []
    for i in range(num_artistas):
        nombre_artista = st.text_input(f"Nombre del artista {i+1}")
        tarifa_comediante = st.number_input(f"Tarifa del comediante {i + 1}",
                                            min_value=0.0)
        artistas.append({"nombre": nombre_artista, "tarifa": tarifa_comediante})

    if hora_apertura > hora_show:
        st.warning("La hora de apertura debe ser anterior a la hora del show")
    elif st.button("Guardar"):
        if gui_controler.gestion_controler.crear_evento_filantropico(nombre_evento, fecha_evento, hora_apertura,
                                                                  hora_show, ubicacion, ciudad, direccion,
                                                                  patrocinadores, artistas,aforo):
            st.success("¡Evento guardado exitosamente!")

def dibujar_crear_evento_bar(gui_controler):
    st.subheader("Crear Evento Bar")

    nombre_evento = st.text_input("Nombre del evento")
    fecha_evento = st.date_input("Fecha del evento")
    hora_apertura = st.time_input("Hora de apertura")
    hora_show = st.time_input("Hora del show")
    ubicacion = st.text_input("Ubicación del evento")
    ciudad = st.text_input("Ciudad del evento")
    direccion = st.text_input("Dirección")
    porcentaje_reduccion_preventa = st.number_input(
        "Porcentaje de reducción durante la preventa",
        min_value=0.0,
        value=0.0)

    aforo = st.number_input("Aforo", min_value=1, value=1)
    num_categorias = st.number_input("Número de categorías",
                                     min_value=1,
                                     value=1)
    categorias = {}
    for i in range(num_categorias):
        nombre_categoria = st.text_input(f"Nombre de la categoría {i+1}")
        costo_categoria = st.number_input(f"Costo de la categoría {i+1}",
                                          min_value=0.0)
        categorias[nombre_categoria] = costo_categoria

    cortesias = st.checkbox("Agregar cortesías", value=True)
    if cortesias:
        total_cortesias = st.number_input("Total de cortesías",
                                          min_value=1,
                                          value=1)
        categorias["cortesia"] = 0
    else:
        total_cortesias = 0

    num_comediantes = st.number_input("Número de comediantes participantes",
                                      min_value=1,
                                      value=1)
    comediantes = []
    for i in range(num_comediantes):
        nombre_comediante = st.text_input(f"Nombre"
                                          f" del comediante {i+1}")
        tarifa_comediante = st.number_input(f"Tarifa del comediante {i+1}",
                                            min_value=0.0)
        comediantes.append({
            "nombre": nombre_comediante,
            "tarifa": tarifa_comediante
        })

    if hora_apertura > hora_show:
        st.warning("La hora de apertura debe ser anterior a la hora del show")
    elif total_cortesias > aforo:
        st.warning("El total de cortesías debe ser menor o igual al aforo")
    elif st.button("Guardar"):
        if gui_controler.gestion_controler.crear_evento_bar(
            nombre_evento, fecha_evento, hora_apertura, hora_show, ubicacion,
            ciudad, direccion, categorias, comediantes,
            porcentaje_reduccion_preventa, aforo, total_cortesias):
            st.success("¡Evento guardado exitosamente!")


def dibujar_crear_evento_teatro(gui_controler):
    st.subheader("Crear Evento Teatro")

    nombre_evento = st.text_input("Nombre del evento")
    fecha_evento = st.date_input("Fecha del evento")
    hora_apertura = st.time_input("Hora de apertura")
    hora_show = st.time_input("Hora del show")
    ubicacion = st.text_input("Ubicación del evento")
    ciudad = st.text_input("Ciudad del evento")
    direccion = st.text_input("Dirección")
    porcentaje_reduccion_preventa = st.number_input(
        "Porcentaje de reducción durante la preventa",
        min_value=0.0,
        value=0.0)
    num_categorias = st.number_input("Número de categorías",
                                     min_value=1,
                                     value=1)
    aforo = st.number_input("Aforo", min_value=1, value=1)
    categorias = {}
    for i in range(num_categorias):
        nombre_categoria = st.text_input(f"Nombre de la categoría {i + 1}")
        costo_categoria = st.number_input(f"Costo de la categoría {i + 1}",
                                          min_value=0.0)
        categorias[nombre_categoria] = costo_categoria

    cortesias = st.checkbox("Agregar cortesías", value=True)
    if cortesias:
        total_cortesias = st.number_input("Total de cortesías",
                                          min_value=1,
                                          value=1)
        categorias["cortesia"] = 0
    else:
        total_cortesias = 0

    num_artistas = st.number_input("Número de artistas participantes",
                                   min_value=1,
                                   value=1)
    artistas = []
    for i in range(num_artistas):
        nombre_artista = st.text_input(f"Nombre del artista {i+1}")
        artistas.append({"nombre": nombre_artista, "tarifa": 0})

    costo_alquiler = st.number_input(
        "Costo de alquiler",
        min_value=0.0)  # Agregar campo para el costo de alquiler

    if hora_apertura >= hora_show:
        st.warning("La hora de apertura debe ser anterior a la hora del show")
    elif total_cortesias > aforo:
        st.warning("El total de cortesías debe ser menor o igual al aforo")
    elif st.button("Guardar"):
        if gui_controler.gestion_controler.crear_evento_teatro(
            nombre_evento, fecha_evento, hora_apertura, hora_show, ubicacion,
            ciudad, direccion, categorias, artistas, costo_alquiler,
            porcentaje_reduccion_preventa, aforo, total_cortesias):
            st.success("¡Evento guardado exitosamente!")

def dibujar_comprar_boletas(gui_controler):
    st.subheader("Comprar Boletas")

    # Información del cliente
    nombre_comprador = st.text_input("Nombre del comprador")
    telefono = st.text_input("Teléfono")
    correo = st.text_input("Correo electrónico")
    direccion = st.text_input("Dirección")
    donde_conocio = st.text_input("¿Dónde nos conoció?")
    cantidad_boletas = st.number_input("¿Cuántas boletas comprará?", min_value=1, value=1)

    # Selección del tipo de evento
    tipo_evento = st.selectbox("Selecciona el tipo de evento:", ["Bar", "Filantrópico", "Teatro"])

    # Seleccion nombre Evento
    evento_seleccionado = gui_controler.get_nombres_eventos(tipo_evento)

    # Seleccion categoria
    if evento_seleccionado:
        categoria = gui_controler.comprar_categoria(evento_seleccionado, tipo_evento, cantidad_boletas)
        if categoria is not None:
            metodo_pago = st.selectbox("Método de pago", ["Tarjeta de crédito", "Transferencia bancaria", "Efectivo"])

            if st.button("Comprar"):
                gui_controler.guardar_info_boletas(nombre_comprador, telefono, correo, direccion, evento_seleccionado,
                                                  cantidad_boletas, donde_conocio, metodo_pago, categoria, tipo_evento)
                ubicacion = gui_controler.get_ubicacion(evento_seleccionado, tipo_evento)
                info_cliente = {
                    "nombre": nombre_comprador,
                    "telefono": telefono,
                    "correo": correo,
                    "donde_conocio": donde_conocio,
                    "cantidad_boletas": cantidad_boletas,
                    "evento": evento_seleccionado,
                    "metodo_pago": metodo_pago
                }

                st.success("¡Compra realizada exitosamente!")

                generar_pdf_compra(info_cliente, ubicacion)


def generar_codigo(length=8):
    """Genera un código alfanumérico único."""
    return ''.join(
        random.choices(string.ascii_letters + string.digits, k=length))


def generar_pdf_compra(info_cliente, ubicacion):
    try:
        os.makedirs("compras", exist_ok=True)
        pdf_files = []

        for i in range(info_cliente["cantidad_boletas"]):
            codigo = generar_codigo()
            pdf_path = f"compras/{codigo}.pdf"
            c = canvas.Canvas(pdf_path, pagesize=letter)
            c.setFont("Helvetica-Bold", 12)
            c.drawString(100, 730, f"Datos de la Compra #{i + 1}:")
            c.setFont("Helvetica", 10)
            c.drawString(100, 710, f"Nombre del comprador: {info_cliente['nombre']}")
            c.drawString(100, 690, f"Teléfono: {info_cliente['telefono']}")
            c.drawString(100, 670, f"Correo electrónico: {info_cliente['correo']}")
            c.drawString(100, 650, f"Dónde nos conoció: {info_cliente['donde_conocio']}")
            c.drawString(100, 630, f"Evento: {info_cliente['evento']}")
            c.drawString(100, 610, f"Ubicación: {ubicacion}")
            c.drawString(100, 590, f"Método de pago: {info_cliente['metodo_pago']}")
            c.drawString(100, 570, f"Código único: {codigo}")
            c.save()
            pdf_files.append(pdf_path)

        # Create a ZIP file with all PDFs
        with zipfile.ZipFile("compras/comprobantes.zip", "w") as zipf:
            for pdf_file in pdf_files:
                zipf.write(pdf_file, os.path.basename(pdf_file))


        st.write("Descargar todas las boletas:")
        st.download_button(label="Descargar Boletas",
                           data=open("compras/comprobantes.zip", "rb").read(),
                           file_name="comprobantes.zip",
                           mime="application/zip")

        for i, pdf_file in enumerate(pdf_files):
            st.write(f"Descargar Boleta #{i + 1}:")
            st.download_button(label=f"Descargar Boleta #{i + 1}",
                               data=open(pdf_file, "rb").read(),
                               file_name=os.path.basename(pdf_file),
                               mime="application/pdf")

    except Exception as e:
        st.error(f"Ocurre un error en: {str(e)}")

def dibujar_generar_reporte(gui_controler):
    st.subheader("Generar reporte")
    tipo_reporte = st.radio("Selecciona el tipo de reporte", ["Reporte de Ventas", "Reporte Financiero", "Reporte de los Compradores", "Reporte de los Artistas"])
    if tipo_reporte == "Reporte de los Artistas":
        st.subheader("Elige el evento")
        tipo_evento = st.selectbox("Selecciona el tipo de evento:", ["Bar", "Filantrópico", "Teatro"])
        evento_seleccionado = gui_controler.get_nombres_eventos(tipo_evento)
        gui_controler.generar_reporte(tipo_reporte, evento_seleccionado, tipo_evento)
    elif tipo_reporte == "Reporte de Ventas":
        gui_controler.generar_reporte(tipo_reporte, None, None)

    elif tipo_reporte == "Reporte de los Compradores":
        gui_controler.generar_reporte(tipo_reporte, None, None)
    else:
        st.subheader("Elige el evento")
        tipo_evento = st.selectbox("Selecciona el tipo de evento:", ["Bar", "Filantrópico", "Teatro"])
        evento_seleccionado = gui_controler.get_nombres_eventos(tipo_evento)
        gui_controler.generar_reporte(tipo_reporte, evento_seleccionado, tipo_evento)


def dibujar_verificar_asistencia(gui_controler):
    st.subheader("Verificar Asistencia")
    tipo_evento_seleccionado = st.radio("Selecciona el tipo de evento:",
                                        ["Filantrópico", "Bar", "Teatro"])
    nombres_eventos = gui_controler.get_nombres_eventos(tipo_evento_seleccionado)
    evento_seleccionado = st.selectbox("Selecciona el evento:",
                                       nombres_eventos, key="nombre_asistencia")

    clientes = gui_controler.get_info_clientes(evento_seleccionado)

    asistentes_por_evento = {}

    if clientes:
        nombres_clientes = []
        for cliente in clientes:
            nombres_clientes.append(cliente["nombre"])

        nombres_clientes.append("Todos")
        cliente_seleccionado = st.selectbox("Selecciona el cliente:",
                                            nombres_clientes)

        state_key = f"checkboxes_{evento_seleccionado}_{cliente_seleccionado}"
        selected_checkboxes = st.session_state.get(state_key, [])

        num_checkboxes_marcados = len(selected_checkboxes)
        if num_checkboxes_marcados > 0:
            st.write(
                f"{cliente_seleccionado} tiene {num_checkboxes_marcados} asistencias ya confirmadas."
            )

        if cliente_seleccionado != "Todos":

            cliente = next((c for c in clientes
                            if c["nombre"] == cliente_seleccionado), None)
            if cliente:
                st.write(
                    f"Comprador: {cliente['nombre']} - Evento: {evento_seleccionado}"
                )

                checkboxes_disponibles = [
                    i for i in range(1, cliente["cantidad"] + 1)
                    if i not in selected_checkboxes
                ]
                if checkboxes_disponibles:
                    for i in checkboxes_disponibles:
                        checkbox_label = f"Boleta {i}"

                        checkbox_state = st.checkbox(checkbox_label,
                                                     key=f"{state_key}_{i}")
                        if checkbox_state:

                            asistentes_por_evento[
                                evento_seleccionado] = asistentes_por_evento.get(
                                evento_seleccionado, 0) + 1

                            if i not in selected_checkboxes:
                                selected_checkboxes.append(i)
                        elif i in selected_checkboxes:
                            # Si el checkbox está deseleccionado pero estaba seleccionado previamente, eliminarlo de la lista guardada
                            selected_checkboxes.remove(i)
        else:
            st.write(
                "No se puede mostrar la lista de checkboxes para todos los clientes."
            )

        # Guardar la lista de checkboxes seleccionados en el estado de la sesión
        st.session_state[state_key] = selected_checkboxes
    else:
        st.write("No hay compradores registrados para este evento.")