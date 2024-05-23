import streamlit as st
from streamlit_option_menu import option_menu
from settings import LOGO_HTML_CONFIG



def navegation_sidebar(gui_controler):
    with st.sidebar:
        opcion_seleccionada = option_menu("Navegación",
                                          ["Ver eventos creados", "Crear evento Bar",
                                           "Crear evento Filantrópico", "Crear evento Teatro",
                                           "Comprar boletas", "Generar reporte Ventas", "Generar reporte Artistas",
                                           "Generar reporte Compradores"], orientation="vertical")
    gui_controler.sidebar_option_menu(opcion_seleccionada)


def draw_admin_page(gui_controler):
    st.markdown(LOGO_HTML_CONFIG, unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;'>Bienvenido a Gonzalo Shows</h1>", unsafe_allow_html=True) 
    st.markdown("<h3 style='font-weight:500;text-align: center;'>"
                "Gracias por usar nuestro software, ¿Qué deseas hacer?</h2>", unsafe_allow_html=True)
    navegation_sidebar(gui_controler)


def dibujar_eventos_creados(gui_controler):
    st.subheader("Eventos Creados")

    # Crear un menú interno para filtrar los eventos por tipo
    tipo_evento_seleccionado = st.radio("Selecciona el tipo de evento:", ["Filantrópico", "Bar", "Teatro"])

    # Filtrar los eventos según el tipo seleccionado
    gui_controler.filtrar_eventos_guardados(tipo_evento_seleccionado)


def dibujar_editar_evento(gui_controler, evento, tipo):
    st.subheader(f"Editar Evento {evento['nombre']}")

    # Campos de entrada para editar la información del evento
    nombre_evento = st.empty()
    nombre_evento_input = nombre_evento.text_input("Nombre del evento", value=evento["nombre"])

    fecha_evento = st.empty()
    fecha_evento_input = fecha_evento.date_input("Fecha del evento", value=evento["fecha"])

    hora_apertura = st.empty()
    hora_apertura_input = hora_apertura.time_input("Hora de apertura", value=evento["hora_apertura"])

    hora_show = st.empty()
    hora_show_input = hora_show.time_input("Hora del show", value=evento["hora_show"])

    ubicacion = st.empty()
    ubicacion_input = ubicacion.text_input("Ubicación del evento", value=evento["ubicacion"])

    ciudad = st.empty()
    ciudad_input = ciudad.text_input("Ciudad del evento", value=evento["ciudad"])

    direccion = st.empty()
    direccion_input = direccion.text_input("Dirección", value=evento["direccion"])

    estado = st.empty()
    estado_input = estado.selectbox("Estado del evento", ["Realizado", "Por realizar", "Cancelado", "Aplazado", "Cerrado"], index=["Realizado", "Por realizar", "Cancelado", "Aplazado", "Cerrado"].index(evento["estado"].capitalize()))
    
    # Solo permitir editar el costo del alquiler para eventos de tipo "Teatro"
    if tipo == "Teatro":
        costo_alquiler = st.empty()
        costo_alquiler_input = costo_alquiler.number_input("Costo alquiler", value=float(evento["alquiler"]), min_value=0.0)

    # Guardar los cambios si se hace clic en el botón
    if st.button("Guardar cambios"):
        if tipo == "Teatro":
            gui_controler.gestion_controler.editar_evento_teatro(evento["nombre"], nombre_evento_input, fecha_evento_input,
                                               hora_apertura_input, hora_show_input, ubicacion_input, ciudad_input,
                                               direccion_input, estado_input, costo_alquiler_input)
        elif tipo == "Bar":
            gui_controler.gestion_controler.editar_evento_bar(evento["nombre"], nombre_evento_input, fecha_evento_input,
                                            hora_apertura_input, hora_show_input, ubicacion_input, ciudad_input,
                                            direccion_input, estado_input)
        else:
            gui_controler.gestion_controler.editar_evento_filantropico(evento["nombre"], nombre_evento_input, fecha_evento_input,
                                                     hora_apertura_input, hora_show_input, ubicacion_input, ciudad_input,
                                                     direccion_input, estado_input)

        st.success("¡Evento actualizado exitosamente!")
        st.experimental_rerun()  # Recargar la página para reflejar los cambios


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
                                                                  patrocinadores, artistas)
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
    porcentaje_reduccion_preventa = st.number_input("Porcentaje de reduccion durante la preventa", min_value=0.0,
                                                    value=0.0)
    num_categorias = st.number_input("Número de categorías", min_value=1, value=1)
    
    categorias = {}
    for i in range(num_categorias):
        nombre_categoria = st.text_input(f"Nombre de la categoría {i+1}")
        costo_categoria = st.number_input(f"Costo de la categoría {i+1}", min_value=0.0)
        categorias[nombre_categoria] = costo_categoria

    num_comediantes = st.number_input("Número de comediantes participantes", min_value=1, value=1)
    comediantes = []
    for i in range(num_comediantes):
        nombre_comediante = st.text_input(f"Nombre del comediante {i+1}")
        tarifa_comediante = st.number_input(f"Tarifa del comediante {i+1}", min_value=0.0)
        comediantes.append({"nombre": nombre_comediante, "tarifa": tarifa_comediante})

    if st.button("Guardar"):
        gui_controler.gestion_controler.crear_evento_bar(nombre_evento, fecha_evento, hora_apertura,
                                                         hora_show, ubicacion, ciudad, direccion,
                                                         categorias, comediantes, porcentaje_reduccion_preventa)
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
    porcentaje_reduccion_preventa = st.number_input("Porcentaje de reduccion durante la preventa", min_value=0.0,value=0.0)
    num_categorias = st.number_input("Número de categorías", min_value=1, value=1)

    categorias = {}
    for i in range(num_categorias):
        nombre_categoria = st.text_input(f"Nombre de la categoría {i+1}")
        costo_categoria = st.number_input(f"Costo de la categoría {i+1}", min_value=0.0)
        categorias[nombre_categoria] = costo_categoria

    num_artistas = st.number_input("Número de artistas participantes", min_value=1, value=1)
    artistas = []
    for i in range(num_artistas):
        nombre_artista = st.text_input(f"Nombre del artista {i+1}")
        artistas.append({"nombre": nombre_artista, "tarifa": 0})

    costo_alquiler = st.number_input("Costo de alquiler", min_value=0.0)  # Agregar campo para el costo de alquiler

    if st.button("Guardar"):
        gui_controler.gestion_controler.crear_evento_teatro(nombre_evento, fecha_evento, hora_apertura,
                                                            hora_show, ubicacion, ciudad, direccion,
                                                            categorias, artistas, costo_alquiler, porcentaje_reduccion_preventa)
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
    categoria = gui_controler.comprar_categoria(evento_seleccionado, tipo_evento, cantidad_boletas)

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

