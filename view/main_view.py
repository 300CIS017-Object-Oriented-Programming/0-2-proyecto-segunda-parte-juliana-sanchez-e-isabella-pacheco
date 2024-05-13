import streamlit as st
from streamlit_option_menu import option_menu


def draw_admin_page(gui_controler):
    st.markdown("<img src='https://lh7-us.googleusercontent.com/xjxAtADEig-ArDJO16fwHNTd3fpexqRHyxpt4mD5VYlR_MxigAFvTi6bGOmhO-U5V04126PmwyURqEQAIXyWtC-McrK7V2q9vVXUaJHL37mh6Lz20ptbMCTba5E9nTZKJsB1OPlxr8hrqonWRRLeM9s' width='200' style='display: block; margin: 0 auto;'>", unsafe_allow_html=True) 
    st.markdown("<h1 style='text-align: center;'>Bienvenido a Gonzalo Shows</h1>", unsafe_allow_html=True) 
    st.markdown("<h3 style='font-weight:500;text-align: center;'>Gracias por usar nuestro software, ¿Qué deseas hacer?</h2>", unsafe_allow_html=True) 

    with st.sidebar:
        opcion_seleccionada = option_menu("Navegación", ["Ver eventos creados", "Crear evento Bar", "Crear evento Filantrópico", "Crear evento Teatro", "Comprar boletas", "Generar reporte Ventas", "Generar reporte Artistas", "Generar reporte Compradores"], orientation="vertical")

    if opcion_seleccionada == "Ver eventos creados":
        mostrar_eventos_creados()
    elif opcion_seleccionada == "Crear evento Bar":
        crear_evento_bar()
    elif opcion_seleccionada == "Crear evento Filantrópico":
        crear_evento_filantropico()
    elif opcion_seleccionada == "Crear evento Teatro":
        crear_evento_teatro()
    elif opcion_seleccionada == "Comprar boletas":
        comprar_boletas()
    elif opcion_seleccionada == "Generar reporte Ventas":
        generar_reporte_ventas()
    elif opcion_seleccionada == "Generar reporte Artistas":
        generar_reporte_artistas()
    elif opcion_seleccionada == "Generar reporte Compradores":
        generar_reporte_compradores()
        
def mostrar_eventos_creados():
    st.subheader("Eventos Creados")

    # Obtener los eventos creados
    eventos = obtener_eventos_guardados()

    # Crear un menú interno para filtrar los eventos por tipo
    tipo_evento_seleccionado = st.radio("Selecciona el tipo de evento:", ["Filantrópico", "Bar", "Teatro"])

    # Filtrar los eventos según el tipo seleccionado
    eventos_filtrados = [evento for evento in eventos if evento["tipo"] == tipo_evento_seleccionado]

    # Mostrar la información de los eventos filtrados
    for evento in eventos_filtrados:
        st.write("Nombre:", evento["nombre"])
        st.write("Ubicación:", evento["ubicacion"])
        st.write("Fecha:", evento["fecha"])
        st.write("Estado:", evento["estado"])

        # Verificar si el estado del evento es "realizado"
        if evento["estado"].lower() != "realizado":
            # Mostrar botón de editar
            if st.button(f"Editar {evento['nombre']}"):
                editar_evento(evento)
        else:
            st.write("El evento ya está realizado y no se puede editar.")
        st.write("---")


def actualizar_evento(evento):
    eventos_guardados = obtener_eventos_guardados()
    # Encontrar y reemplazar el evento actualizado en la lista de eventos
    for i, evt in enumerate(eventos_guardados):
        if evt["nombre"] == evento["nombre"]:
            eventos_guardados[i] = evento
            break
    st.session_state.eventos = eventos_guardados
    st.experimental_rerun()  # Recargar la página para reflejar los cambios

def editar_evento(evento):
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
    if evento["tipo"] == "Teatro":
        costo_alquiler = st.empty()
        costo_alquiler_input = costo_alquiler.number_input("Costo alquiler", value=float(evento["costo_alquiler"]), min_value=0.0)

    # Guardar los cambios si se hace clic en el botón
    if st.button("Guardar cambios"):
        evento["nombre"] = nombre_evento_input
        evento["fecha"] = fecha_evento_input
        evento["hora_apertura"] = hora_apertura_input
        evento["hora_show"] = hora_show_input
        evento["ubicacion"] = ubicacion_input
        evento["ciudad"] = ciudad_input
        evento["direccion"] = direccion_input
        evento["estado"] = estado_input
        
        # Actualizar el costo del alquiler si es un evento de tipo "Teatro"
        if evento["tipo"] == "Teatro":
            evento["costo_alquiler"] = costo_alquiler_input

        # Actualizar el evento en la lista de eventos
        actualizar_evento(evento)
        st.success("¡Evento actualizado exitosamente!")

def crear_evento_filantropico():
    st.subheader("Crear Evento Filantrópico")

    nombre_evento = st.text_input("Nombre del evento")
    fecha_evento = st.date_input("Fecha del evento")
    hora_apertura = st.time_input("Hora de apertura")
    hora_show = st.time_input("Hora del show")
    ubicacion = st.text_input("Ubicación del evento")
    ciudad = st.text_input("Ciudad del evento")
    direccion = st.text_input("Dirección")
    estado = st.selectbox("Estado del evento", ["Realizado", "Por realizar", "Cancelado", "Aplazado", "Cerrado"])
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
        tarifa_artista = st.number_input(f"Tarifa del artista {i+1}", min_value=0.0)
        artistas.append({"nombre": nombre_artista, "tarifa": tarifa_artista})

    if st.button("Guardar"):
        guardar_evento(nombre_evento, fecha_evento, hora_apertura, hora_show, ubicacion, ciudad, direccion, estado, "", artistas, 0, "Filantrópico", patrocinadores)


def crear_evento_bar():
    st.subheader("Crear Evento Bar")

    nombre_evento = st.text_input("Nombre del evento")
    fecha_evento = st.date_input("Fecha del evento")
    hora_apertura = st.time_input("Hora de apertura")
    hora_show = st.time_input("Hora del show")
    ubicacion = st.text_input("Ubicación del evento")
    ciudad = st.text_input("Ciudad del evento")
    direccion = st.text_input("Dirección")
    estado = st.selectbox("Estado del evento", ["Realizado", "Por realizar", "Cancelado", "Aplazado", "Cerrado"])
    num_categorias = st.number_input("Número de categorías", min_value=1, value=1)
    
    categorias = []
    for i in range(num_categorias):
        nombre_categoria = st.text_input(f"Nombre de la categoría {i+1}")
        costo_categoria = st.number_input(f"Costo de la categoría {i+1}", min_value=0.0)
        categorias.append({"nombre": nombre_categoria, "costo": costo_categoria})

    num_comediantes = st.number_input("Número de comediantes participantes", min_value=1, value=1)
    comediantes = []
    for i in range(num_comediantes):
        nombre_comediante = st.text_input(f"Nombre del comediante {i+1}")
        tarifa_comediante = st.number_input(f"Tarifa del comediante {i+1}", min_value=0.0)
        comediantes.append({"nombre": nombre_comediante, "tarifa": tarifa_comediante})

    if st.button("Guardar"):
        guardar_evento(nombre_evento, fecha_evento, hora_apertura, hora_show, ubicacion, ciudad, direccion, estado, categorias, comediantes, 0, "Bar")

def crear_evento_teatro():
    st.subheader("Crear Evento Teatro")

    nombre_evento = st.text_input("Nombre del evento")
    fecha_evento = st.date_input("Fecha del evento")
    hora_apertura = st.time_input("Hora de apertura")
    hora_show = st.time_input("Hora del show")
    ubicacion = st.text_input("Ubicación del evento")
    ciudad = st.text_input("Ciudad del evento")
    direccion = st.text_input("Dirección")
    estado = st.selectbox("Estado del evento", ["Realizado", "Por realizar", "Cancelado", "Aplazado", "Cerrado"])
    num_categorias = st.number_input("Número de categorías", min_value=1, value=1)
    
    categorias = []
    for i in range(num_categorias):
        nombre_categoria = st.text_input(f"Nombre de la categoría {i+1}")
        costo_categoria = st.number_input(f"Costo de la categoría {i+1}", min_value=0.0)
        categorias.append({"nombre": nombre_categoria, "costo": costo_categoria})

    num_artistas = st.number_input("Número de artistas participantes", min_value=1, value=1)
    artistas = []
    for i in range(num_artistas):
        nombre_artista = st.text_input(f"Nombre del artista {i+1}")
        tarifa_artista = st.number_input(f"Tarifa del artista {i+1}", min_value=0.0)
        artistas.append({"nombre": nombre_artista, "tarifa": tarifa_artista})

    costo_alquiler = st.number_input("Costo de alquiler", min_value=0.0)  # Agregar campo para el costo de alquiler

    if st.button("Guardar"):
        guardar_evento(nombre_evento, fecha_evento, hora_apertura, hora_show, ubicacion, ciudad, direccion, estado, categorias, artistas, costo_alquiler, "Teatro")


def guardar_evento(nombre_evento, fecha_evento, hora_apertura, hora_show, ubicacion, ciudad, direccion, estado, categoria, artistas, costo_alquiler, tipo_evento, patrocinadores=[]):
    evento = {
        "nombre": nombre_evento,
        "fecha": fecha_evento,
        "hora_apertura": hora_apertura,
        "hora_show": hora_show,
        "ubicacion": ubicacion,
        "ciudad": ciudad,
        "direccion": direccion,
        "estado": estado,
        "categoria": categoria,
        "artistas": artistas,
        "costo_alquiler": costo_alquiler,
        "tipo": tipo_evento
    }
    if tipo_evento == "Filantrópico":
        evento["patrocinadores"] = patrocinadores

    eventos_guardados = obtener_eventos_guardados()
    eventos_guardados.append(evento)
    st.session_state.eventos = eventos_guardados
    st.success("¡Evento guardado exitosamente!")

def obtener_eventos_guardados():
    if "eventos" not in st.session_state:
        st.session_state.eventos = []
    return st.session_state.eventos

def comprar_boletas():
    st.subheader("Comprar Boletas")

    # Información del cliente
    nombre_comprador = st.text_input("Nombre del comprador")
    telefono = st.text_input("Teléfono")
    correo = st.text_input("Correo electrónico")
    direccion = st.text_input("Dirección")
    donde_conocio = st.text_input("¿Dónde nos conoció?")
    cantidad_boletas = st.number_input("¿Cuántas boletas comprará?", min_value=1, value=1)

    # Selección del evento
    eventos = obtener_eventos_guardados()
    nombres_eventos = [evento["nombre"] for evento in eventos]
    evento_seleccionado = st.selectbox("Selecciona el evento:", nombres_eventos)

    evento = next((e for e in eventos if e["nombre"] == evento_seleccionado), None)

    if evento:
        if evento["tipo"] == "Filantrópico":
            st.write("Entrada gratuita")
        else:
            st.subheader("Selecciona la categoría:")
            categorias = evento["categoria"]
            nombre_categorias = [categoria["nombre"] for categoria in categorias]
            categoria_elegida = st.selectbox("Categoría:", nombre_categorias)

            # Obtener el costo de la categoría seleccionada
            costo_categoria = next((c["costo"] for c in categorias if c["nombre"] == categoria_elegida), 0)
            total = cantidad_boletas * costo_categoria
            st.write(f"Total a pagar: ${total}")

    metodo_pago = st.selectbox("Método de pago", ["Tarjeta de crédito", "Transferencia bancaria", "Efectivo"])

    if st.button("Comprar"):
        info_cliente = {
            "nombre": nombre_comprador,
            "telefono": telefono,
            "correo": correo,
            "direccion": direccion,
            "donde_conocio": donde_conocio,
            "cantidad_boletas": cantidad_boletas,
            "evento": evento_seleccionado,
            "metodo_pago": metodo_pago
        }
        guardar_info_cliente(info_cliente)
        st.success("¡Compra realizada exitosamente!")

def guardar_info_cliente(info_cliente):
    clientes = obtener_clientes_guardados()
    clientes.append(info_cliente)
    st.session_state.clientes = clientes

def obtener_clientes_guardados():
    if "clientes" not in st.session_state:
        st.session_state.clientes = []
    return st.session_state.clientes

def generar_reporte_ventas():
    st.subheader("Reporte de Ventas")

    # Obtener la información de los eventos y clientes
    eventos = obtener_eventos_guardados()
    clientes = obtener_clientes_guardados()

    # Diccionario para almacenar las ventas por evento y categoría
    ventas = {}

    # Calcular las ventas por evento y categoría
    for cliente in clientes:
        evento = next((e for e in eventos if e["nombre"] == cliente["evento"]), None)
        if evento:
            tipo_evento = evento["tipo"]
            cantidad_boletas = cliente["cantidad_boletas"]

            if tipo_evento == "Filantrópico":
                # Calcular los ingresos a partir de los aportes de los patrocinadores
                ingresos = sum(p["aporte"] for p in evento["patrocinadores"]) - sum(a["tarifa"] for a in evento["artistas"])
                costo_artista = sum(a["tarifa"] for a in evento["artistas"])
                costo_alquiler = 0
            elif tipo_evento == "Teatro":
                # Calcular los ingresos a partir del costo de las boletas vendidas por categoría
                ingresos = sum(cantidad_boletas * c["costo"] for c in evento["categoria"] if c["nombre"] == "Boleta")
                # Calcular el costo de los artistas y el costo de alquiler
                costo_artista = sum(a["tarifa"] for a in evento["artistas"])
                costo_alquiler = evento["costo_alquiler"]
            elif tipo_evento == "Bar":
                # Calcular los ingresos a partir del costo de las boletas vendidas
                ingresos = sum(c["costo"] * cantidad_boletas for c in evento["categoria"] if c["nombre"] == "Boleta")
                # Calcular el costo de los comediantes
                costo_artista = sum(a["tarifa"] for a in evento["artistas"])
                costo_alquiler = 0
            
            total = ingresos - (costo_artista + costo_alquiler)

            if evento["nombre"] not in ventas:
                ventas[evento["nombre"]] = {"ingresos": 0, "boletas_vendidas": 0, "costo_artista": 0, "costo_alquiler": 0}

            ventas[evento["nombre"]]["ingresos"] += ingresos
            ventas[evento["nombre"]]["boletas_vendidas"] += cantidad_boletas
            ventas[evento["nombre"]]["costo_artista"] += costo_artista
            ventas[evento["nombre"]]["costo_alquiler"] += costo_alquiler
            ventas[evento["nombre"]]["total"] = total

    # Mostrar el reporte de ventas por evento
    for evento, info in ventas.items():
        st.write(f"Evento: {evento}")
        st.write(f"Total Ventas: ${info['ingresos'] + info['costo_artista'] + info['costo_alquiler']}")
        st.write(f"Boletas Vendidas: {info['boletas_vendidas']}")
        if info['costo_artista']:
            st.write(f"Costo de los Artistas: ${info['costo_artista']}")
        if info['costo_alquiler']:
            st.write(f"Costo de Alquiler: ${info['costo_alquiler']}")
        st.write(f"Total: ${info['total']}")
        st.write("---")


def generar_reporte_compradores():
    st.subheader("Reporte de Compradores")


    clientes = obtener_clientes_guardados()


    if clientes:
        st.table(clientes)
    else:
        st.write("No hay datos de clientes aún.")



def generar_reporte_artistas():
    st.subheader("Reporte de Artistas")

    eventos = obtener_eventos_guardados()
    clientes = obtener_clientes_guardados()


    datos_artistas = {}

    for evento in eventos:
        tipo_evento = evento["tipo"]
        if tipo_evento in ["Bar", "Teatro", "Filantrópico"]:
            artistas_evento = evento["artistas"]
            for artista in artistas_evento:
                nombre_artista = artista["nombre"]
                if nombre_artista not in datos_artistas:
                    datos_artistas[nombre_artista] = []

                # Buscar las compras relacionadas con este evento y artista
                compras_artista_evento = [cliente for cliente in clientes if cliente["evento"] == evento["nombre"] and artista["nombre"] in [a["nombre"] for a in evento["artistas"]]]
                for compra in compras_artista_evento:
                    datos_artista_evento = {
                        "nombre_evento": evento["nombre"],
                        "fecha": evento["fecha"],
                        "lugar": evento["ubicacion"],
                        "boletas_vendidas": compra["cantidad_boletas"],
                        "tarifa_artista": artista["tarifa"]
                    }
                    datos_artistas[nombre_artista].append(datos_artista_evento)


    if datos_artistas:
        for artista, eventos_info in datos_artistas.items():
            st.write(f"Artista: {artista}")
            for evento_info in eventos_info:
                st.write(f"Nombre del evento: {evento_info['nombre_evento']}")
                st.write(f"Fecha: {evento_info['fecha']}")
                st.write(f"Lugar: {evento_info['lugar']}")
                st.write(f"Boletas Vendidas: {evento_info['boletas_vendidas']}")
                st.write(f"Tarifa del artista: ${evento_info['tarifa_artista']}")
                st.write("---")
    else:
        st.write("No hay datos de artistas para mostrar.")
