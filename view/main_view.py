import streamlit as st
from fpdf import FPDF
import base64
from streamlit_option_menu import option_menu
from settings import LOGO_HTML_CONFIG



def navegation_sidebar(gui_controler):
    with st.sidebar:
        opcion_seleccionada = option_menu("Navegación",
                                          ["Ver eventos creados", "Crear evento Bar",
                                           "Crear evento Filantrópico", "Crear evento Teatro",
                                           "Comprar boletas", "Generar reporte"], orientation="vertical")
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
    preventa_estado_input = st.checkbox("Preventa", value=True)

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
    patrocinadores = []
    for i in range(num_patrocinadores):
        nombre_patrocinador = st.text_input(f"Nombre del patrocinador {i+1}")
        aporte_patrocinador = st.number_input(f"Aporte del patrocinador {i+1}", min_value=0.0)
        patrocinadores.append({"nombre": nombre_patrocinador, "aporte": aporte_patrocinador})

    num_artistas = st.number_input("Número de artistas participantes", min_value=1, value=1)
    artistas = []
    for i in range(num_artistas):
        nombre_artista = st.text_input(f"Nombre del artista {i+1}")
        artistas.append({"nombre": nombre_artista, "tarifa": 0})

    if st.button("Guardar"):
        gui_controler.gestion_controler.crear_evento_filantropico(nombre_evento, fecha_evento, hora_apertura,
                                                                  hora_show, ubicacion, ciudad, direccion,
                                                                  patrocinadores, artistas,aforo)
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
    num_categorias = st.number_input("Número de categorías",
                                     min_value=1,
                                     value=1)
    aforo = st.number_input("Aforo", min_value=1, value=1)

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

    if hora_apertura >= hora_show:
        st.warning("La hora de apertura debe ser anterior a la hora del show")
    elif total_cortesias > aforo:
        st.warning("El total de cortesías debe ser menor o igual al aforo")
    elif st.button("Guardar"):
        gui_controler.gestion_controler.crear_evento_bar(
            nombre_evento, fecha_evento, hora_apertura, hora_show, ubicacion,
            ciudad, direccion, categorias, comediantes,
            porcentaje_reduccion_preventa, aforo, total_cortesias)
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
        gui_controler.gestion_controler.crear_evento_teatro(
            nombre_evento, fecha_evento, hora_apertura, hora_show, ubicacion,
            ciudad, direccion, categorias, artistas, costo_alquiler,
            porcentaje_reduccion_preventa, aforo, total_cortesias)
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
                st.success("¡Compra realizada exitosamente!")

                for i in range(cantidad_boletas):
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Helvetica", size=12)
                    pdf.cell(200, 10, txt=f"Boleta {i + 1}", ln=True, align='C')
                    pdf.cell(200, 10, txt=f"Nombre del comprador: {nombre_comprador}", ln=True)
                    pdf.cell(200, 10, txt=f"Teléfono: {telefono}", ln=True)
                    pdf.cell(200, 10, txt=f"Correo electrónico: {correo}", ln=True)
                    pdf.cell(200, 10, txt=f"Dirección: {direccion}", ln=True)
                    pdf.cell(200, 10, txt=f"¿Dónde nos conoció?: {donde_conocio}", ln=True)
                    pdf.cell(200, 10, txt=f"Evento: {evento_seleccionado}", ln=True)
                    pdf.cell(200, 10, txt=f"Categoría: {categoria}", ln=True)
                    pdf.cell(200, 10, txt=f"Método de pago: {metodo_pago}", ln=True)

                    # Guardar el PDF en memoria
                    pdf_output = pdf.output(dest='S').encode('latin1')
                    pdf_base64 = base64.b64encode(pdf_output).decode('latin1')

                    # Crear enlace de descarga (lo voy a volver un botoncito)
                    href = f'<a href="data:application/octet-stream;base64,{pdf_base64}" download="boleta_{nombre_comprador.replace(" ", "")}{i + 1}.pdf">Descargar Boleta {i + 1}</a>'
                    st.markdown(href, unsafe_allow_html=True)

def dibujar_generar_reporte(gui_controler):
    st.subheader("Generar reporte")
    tipo_reporte = st.radio("Selecciona el tipo de reporte", ["Reporte de Ventas, Reporte Financiero, Reporte de los Compradores, Reporte de los Artistas"])
    if tipo_reporte == "Reporte de los Artistas" :
        st.subheader("Elige el artista")
        artista_seleccionado = st.selectbox("Artistas", gui_controler.get_artistas())
        if artista_seleccionado != "":
            st.button("Generar reporte del artista", on_click=gui_controler.guardar_reporte(tipo_reporte,
                                                                                            artista_seleccionado, None))
    elif tipo_reporte == "Reporte de Ventas":
        st.subheader("Elige el evento")
        tipo_evento = st.selectbox("Tipo de evento", ["Bar, Teatro"])
        evento_seleccionado = gui_controler.get_nombres_eventos(tipo_evento)
        if evento_seleccionado != "":
            if st.button(f"Generar {tipo_reporte} para {evento_seleccionado}"):
                gui_controler.generar_reporte(tipo_reporte, evento_seleccionado, tipo_evento)

    else:
        st.subheader("Elige el evento")
        tipo_evento = st.selectbox("Tipo de evento", ["Bar, Filantropico, Teatro"])
        evento_seleccionado = gui_controler.get_nombres_eventos(tipo_evento)
        if evento_seleccionado != "":
            if st.button(f"Generar {tipo_reporte} para {evento_seleccionado}"):
                gui_controler.generar_reporte(tipo_reporte, evento_seleccionado, tipo_evento)

