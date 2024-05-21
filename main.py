import streamlit as st
from streamlit_option_menu import option_menu
from io import BytesIO
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle


class Evento:
    def __init__(self, nombre, fecha, hora_apertura, hora_show, ubicacion, ciudad, direccion, estado, categoria,
                 artistas, costo_alquiler, tipo):
        self.nombre = nombre
        self.fecha = fecha
        self.hora_apertura = hora_apertura
        self.hora_show = hora_show
        self.ubicacion = ubicacion
        self.ciudad = ciudad
        self.direccion = direccion
        self.estado = estado
        self.categoria = categoria
        self.artistas = artistas
        self.costo_alquiler = costo_alquiler
        self.tipo = tipo

    def actualizar(self, nombre=None, fecha=None, hora_apertura=None, hora_show=None, ubicacion=None, ciudad=None,
                   direccion=None, estado=None, categoria=None, artistas=None, costo_alquiler=None, tipo=None):
        if nombre is not None:
            self.nombre = nombre
        if fecha is not None:
            self.fecha = fecha
        if hora_apertura is not None:
            self.hora_apertura = hora_apertura
        if hora_show is not None:
            self.hora_show = hora_show
        if ubicacion is not None:
            self.ubicacion = ubicacion
        if ciudad is not None:
            self.ciudad = ciudad
        if direccion is not None:
            self.direccion = direccion
        if estado is not None:
            self.estado = estado
        if categoria is not None:
            self.categoria = categoria
        if artistas is not None:
            self.artistas = artistas
        if costo_alquiler is not None:
            self.costo_alquiler = costo_alquiler
        if tipo is not None:
            self.tipo = tipo

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "fecha": self.fecha,
            "hora_apertura": self.hora_apertura,
            "hora_show": self.hora_show,
            "ubicacion": self.ubicacion,
            "ciudad": self.ciudad,
            "direccion": self.direccion,
            "estado": self.estado,
            "categoria": self.categoria,
            "artistas": self.artistas,
            "costo_alquiler": self.costo_alquiler,
            "tipo": self.tipo
        }


eventicos = []


def main():
    st.markdown(
        "<img src='https://lh7-us.googleusercontent.com/xjxAtADEig-ArDJO16fwHNTd3fpexqRHyxpt4mD5VYlR_MxigAFvTi6bGOmhO-U5V04126PmwyURqEQAIXyWtC-McrK7V2q9vVXUaJHL37mh6Lz20ptbMCTba5E9nTZKJsB1OPlxr8hrqonWRRLeM9s' width='200' style='display: block; margin: 0 auto;'>",
        unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;'>Bienvenido a Gonzalo Shows</h1>", unsafe_allow_html=True)
    st.markdown(
        "<h3 style='font-weight:500;text-align: center;'>Gracias por usar nuestro software, ¿Qué deseas hacer?</h2>",
        unsafe_allow_html=True)

    with st.sidebar:
        opcion_seleccionada = option_menu("Navegación",
                                          ["Ver eventos creados", "Crear evento Bar", "Crear evento Filantrópico",
                                           "Crear evento Teatro", "Comprar boletas", "Generar reporte Ventas",
                                           "Generar reporte Artistas", "Generar reporte Compradores"],
                                          orientation="vertical")

    if opcion_seleccionada == "Ver eventos creados":
        st.write(f"{eventicos}") # debug
        st.write(f"prueba {len(eventicos)}")
        if st.button(f"aumentar 1"):
            eventicos.append(1)
            eventicos.append(1)
            st.info(f"prueba {len(eventicos)} y {eventicos}")
        mostrar_eventos_creados()
        st.write(f"{eventicos}")
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

    eventos = obtener_eventos_guardados()

    tipo_evento_seleccionado = st.radio("Selecciona el tipo de evento:", ["Filantrópico", "Bar", "Teatro"])

    eventos_filtrados = [evento for evento in eventos if evento.tipo == tipo_evento_seleccionado]

    for evento in eventos_filtrados:
        st.write("Nombre:", evento.nombre)
        st.write("Ubicación:", evento.ubicacion)
        st.write("Fecha:", evento.fecha)
        st.write("Estado:", evento.estado)

        if evento.estado.lower() != "realizado":
            # Mostrar botón de editar
            if st.button(f"Editar {evento.nombre}"):
                editar_evento(evento)
        else:
            st.write("El evento ya está realizado y no se puede editar.")
        st.write("---")


def actualizar_evento(evento_actualizado):
    if 'eventos' not in st.session_state:
        st.session_state.eventos = []

    eventos_guardados = st.session_state.eventos

    for i, evento in enumerate(eventos_guardados):
        if evento.nombre == evento_actualizado.nombre:
            eventos_guardados[i] = evento_actualizado
            break

    st.session_state.eventos = eventos_guardados


def editar_evento(evento):
    st.subheader(f"Editar Evento {evento.nombre}")

    nombre_evento = st.text_input("Nombre del evento", value=evento.nombre, key="nombre_evento")
    ubicacion = st.text_input("Ubicación del evento", value=evento.ubicacion, key="ubicacion_evento")
    fecha_evento = st.date_input("Fecha del evento", value=evento.fecha, key="fecha_evento")
    hora_apertura = st.time_input("Hora de apertura", value=evento.hora_apertura, key="hora_apertura_evento")
    hora_show = st.time_input("Hora del show", value=evento.hora_show, key="hora_show_evento")
    estado = st.selectbox("Estado del evento", ["Realizado", "Por realizar", "Cancelado", "Aplazado", "Cerrado"],
                          index=["Realizado", "Por realizar", "Cancelado", "Aplazado", "Cerrado"].index(
                              evento.estado.capitalize()),
                          key="estado_evento")
    ciudad = st.text_input("Ciudad", value=evento.ciudad, key="ciudad_evento")
    direccion = st.text_input("Dirección", value=evento.direccion, key="direccion_evento")
    categoria = st.text_input("Categoría", value=evento.categoria, key="categoria_evento")
    artistas = st.text_area("Artistas", value=evento.artistas, key="artistas_evento")
    costo_alquiler = st.number_input("Costo de alquiler", value=evento.costo_alquiler, key="costo_alquiler_evento")

    if st.button("Guardar cambios", key="guardar_cambios"):
        evento_actualizado = Evento(
            nombre=nombre_evento,
            fecha=fecha_evento,
            hora_apertura=hora_apertura,
            hora_show=hora_show,
            ubicacion=ubicacion,
            ciudad=ciudad,
            direccion=direccion,
            estado=estado.lower(),
            categoria=categoria,
            artistas=artistas,
            costo_alquiler=costo_alquiler,
            tipo=evento.tipo
        )

        # Actualizar el evento en la lista de eventos
        actualizar_evento(evento_actualizado)
        st.success("¡Evento actualizado exitosamente!")
        st.experimental_rerun()  # Recargar la página para reflejar los cambios


def crear_evento_filantropico():
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
        nombre_patrocinador = st.text_input(f"Nombre del patrocinador {i + 1}")
        aporte_patrocinador = st.number_input(f"Aporte del patrocinador {i + 1}", min_value=0.0)
        patrocinadores.append({"nombre": nombre_patrocinador, "aporte": aporte_patrocinador})

    num_artistas = st.number_input("Número de artistas participantes", min_value=1, value=1)
    artistas = []
    for i in range(num_artistas):
        nombre_artista = st.text_input(f"Nombre del artista {i + 1}")
        tarifa_artista = st.number_input(f"Tarifa del artista {i + 1}", min_value=0.0)
        artistas.append({"nombre": nombre_artista, "tarifa": tarifa_artista})

    if st.button("Guardar"):
        guardar_evento(nombre_evento, fecha_evento, hora_apertura, hora_show, ubicacion, ciudad, direccion,
                       "Por realizar", "", artistas, 0, "Filantrópico", patrocinadores)


def crear_evento_bar():
    st.subheader("Crear Evento Bar")

    nombre_evento = st.text_input("Nombre del evento")
    fecha_evento = st.date_input("Fecha del evento")
    hora_apertura = st.time_input("Hora de apertura")
    hora_show = st.time_input("Hora del show")
    ubicacion = st.text_input("Ubicación del evento")
    ciudad = st.text_input("Ciudad del evento")
    direccion = st.text_input("Dirección")
    # estado = st.selectbox("Estado del evento", ["Realizado", "Por realizar", "Cancelado", "Aplazado", "Cerrado"])
    num_categorias = st.number_input("Número de categorías", min_value=1, value=1)

    categorias = []
    for i in range(num_categorias):
        nombre_categoria = st.text_input(f"Nombre de la categoría {i + 1}")
        costo_categoria = st.number_input(f"Costo de la categoría {i + 1}", min_value=0.0)
        categorias.append({"nombre": nombre_categoria, "costo": costo_categoria})

    num_comediantes = st.number_input("Número de comediantes participantes", min_value=1, value=1)
    comediantes = []
    for i in range(num_comediantes):
        nombre_comediante = st.text_input(f"Nombre del comediante {i + 1}")
        tarifa_comediante = st.number_input(f"Tarifa del comediante {i + 1}", min_value=0.0)
        comediantes.append({"nombre": nombre_comediante, "tarifa": tarifa_comediante})

    if st.button("Guardar"):
        guardar_evento(nombre_evento, fecha_evento, hora_apertura, hora_show, ubicacion, ciudad, direccion,
                       "Por realizar", categorias, comediantes, 0, "Bar")


def crear_evento_teatro():
    st.subheader("Crear Evento Teatro")

    nombre_evento = st.text_input("Nombre del evento")
    fecha_evento = st.date_input("Fecha del evento")
    hora_apertura = st.time_input("Hora de apertura")
    hora_show = st.time_input("Hora del show")
    ubicacion = st.text_input("Ubicación del evento")
    ciudad = st.text_input("Ciudad del evento")
    direccion = st.text_input("Dirección")
    num_categorias = st.number_input("Número de categorías", min_value=1, value=1)

    categorias = []
    for i in range(num_categorias):
        nombre_categoria = st.text_input(f"Nombre de la categoría {i + 1}")
        costo_categoria = st.number_input(f"Costo de la categoría {i + 1}", min_value=0.0)
        categorias.append({"nombre": nombre_categoria, "costo": costo_categoria})

    num_artistas = st.number_input("Número de artistas participantes", min_value=1, value=1)
    artistas = []
    for i in range(num_artistas):
        nombre_artista = st.text_input(f"Nombre del artista {i + 1}")
        tarifa_artista = st.number_input(f"Tarifa del artista {i + 1}", min_value=0.0)
        artistas.append({"nombre": nombre_artista, "tarifa": tarifa_artista})

    costo_alquiler = st.number_input("Costo de alquiler", min_value=0.0)

    if st.button("Guardar"):
        guardar_evento(nombre_evento, fecha_evento, hora_apertura, hora_show, ubicacion, ciudad, direccion,
                       "Por realizar", categorias, artistas, costo_alquiler, "Teatro")


def guardar_evento(nombre_evento, fecha_evento, hora_apertura, hora_show, ubicacion, ciudad, direccion, estado,
                   categoria, artistas, costo_alquiler, tipo_evento, patrocinadores=[]):
    # evento = {
    # "nombre": nombre_evento,
    # "fecha": fecha_evento,
    # "hora_apertura": hora_apertura,
    # "hora_show": hora_show,
    #  "ubicacion": ubicacion,
    #  "ciudad": ciudad,
    #   "direccion": direccion,
    #   "estado": estado,
    #   "categoria": categoria,
    #   "artistas": artistas,
    #   "costo_alquiler": costo_alquiler,
    #   "tipo": tipo_evento
    #  }
    # if tipo_evento == "Filantrópico":
    #     evento["patrocinadores"] = patrocinadores
    evento = Evento(nombre_evento, fecha_evento, hora_apertura, hora_show, ubicacion, ciudad, direccion, estado,
                    categoria, artistas, costo_alquiler, tipo_evento)
    # eventos_guardados = obtener_eventos_guardados()
    # eventos_guardados.append(evento)
    eventicos.append(evento)
    st.write(f"{evento}")
    eventicos.append(1)
    # st.session_state.eventos = eventos_guardados
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


def generar_reporte_compradores():
    st.subheader("Reporte de Compradores")

    clientes = obtener_clientes_guardados()

    if clientes:
        # Convertir los datos de los clientes a un DataFrame de Pandas
        df_clientes = pd.DataFrame(clientes)

        # Generar el PDF del reporte
        pdf_reporte = BytesIO()
        doc = SimpleDocTemplate(pdf_reporte, pagesize=letter)

        # Convertir el DataFrame a una tabla de ReportLab
        data = [df_clientes.columns.tolist()] + df_clientes.values.tolist()
        table = Table(data)

        # Estilo de la tabla
        style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), '#77DCE7'),
                            ('TEXTCOLOR', (0, 0), (-1, 0), (0, 0, 0)),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), '#E6F0ED'),
                            ('GRID', (0, 0), (-1, -1), 1, '#ffffff')])

        table.setStyle(style)

        doc.build([table])

        st.download_button(
            label="Descargar Reporte PDF",
            data=pdf_reporte.getvalue(),
            file_name="reporte_compradores.pdf",
            mime="application/pdf"
        )

        st.table(df_clientes)
        eventos = obtener_eventos_guardados()

        # Crear un diccionario para almacenar el número de boletas vendidas por evento
        boletas_por_evento = {}

        # Contar el número de boletas vendidas por evento (pendiente debug)
        for cliente in clientes:
            evento_actual = cliente["evento"]
            boletas_actuales = cliente["cantidad_boletas"]
            boletas_por_evento[evento_actual] = boletas_por_evento.get(evento_actual, 0) + boletas_actuales

        # Convertir el diccionario en un DataFrame de Pandas para la gráfica
        df_boletas_por_evento = pd.DataFrame(list(boletas_por_evento.items()), columns=["Evento", "Boletas Vendidas"])

        # Generar la gráfica de barras con el número de boletas vendidas por evento
        st.subheader("Gráfica de boletas vendidas por evento")
        st.bar_chart(df_boletas_por_evento.set_index("Evento"))
    else:
        st.write("No hay datos de clientes aún.")


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
                ingresos = sum(p["aporte"] for p in evento["patrocinadores"]) - sum(
                    a["tarifa"] for a in evento["artistas"])
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
                ventas[evento["nombre"]] = {"ingresos": 0, "boletas_vendidas": 0, "costo_artista": 0,
                                            "costo_alquiler": 0}

            ventas[evento["nombre"]]["ingresos"] += ingresos
            ventas[evento["nombre"]]["boletas_vendidas"] += cantidad_boletas
            ventas[evento["nombre"]]["costo_artista"] += costo_artista
            ventas[evento["nombre"]]["costo_alquiler"] += costo_alquiler
            ventas[evento["nombre"]]["total"] = total

    # Mostrar el reporte de ventas por evento
    for evento, info in ventas.items():
        st.write(f"Evento: {evento}")
        st.write(f"Total Ingresos: ${info['ingresos'] + info['costo_artista'] + info['costo_alquiler']}")
        st.write(f"Boletas Vendidas: {info['boletas_vendidas']}")
        if info['costo_artista']:
            st.write(f"Costo de los Artistas: ${info['costo_artista']}")
        if info['costo_alquiler']:
            st.write(f"Costo de Alquiler: ${info['costo_alquiler']}")
        st.write(f"Total: ${info['total']}")
        st.write("---")

    if clientes:
        st.table(clientes)


def generar_reporte_artistas():
    st.subheader("Reporte de Artistas")

    eventos = obtener_eventos_guardados()
    clientes = obtener_clientes_guardados()

    # Filtro para seleccionar un evento
    nombres_eventos = [evento["nombre"] for evento in eventos]
    evento_seleccionado = st.selectbox("Selecciona un evento:", nombres_eventos)

    # Filtrar los eventos para mostrar solo la información del evento seleccionado
    evento_filtrado = next((evento for evento in eventos if evento["nombre"] == evento_seleccionado), None)

    if evento_filtrado:
        datos_artistas = {}

        for artista in evento_filtrado["artistas"]:
            nombre_artista = artista["nombre"]

            # Si el artista ya existe en los datos_artistas, agregar la información del evento actual
            if nombre_artista in datos_artistas:
                datos_artistas[nombre_artista].append({
                    "nombre_evento": evento_filtrado["nombre"],
                    "fecha": evento_filtrado["fecha"],
                    "lugar": evento_filtrado["ubicacion"],
                    "boletas_vendidas": 0,  # Inicializar la cantidad de boletas vendidas en 0
                    "tarifa_artista": artista["tarifa"]
                })
            else:
                # Si el artista es nuevo, crear una nueva entrada en datos_artistas
                datos_artistas[nombre_artista] = [{
                    "nombre_evento": evento_filtrado["nombre"],
                    "fecha": evento_filtrado["fecha"],
                    "lugar": evento_filtrado["ubicacion"],
                    "boletas_vendidas": 0,  # Inicializar la cantidad de boletas vendidas en 0
                    "tarifa_artista": artista["tarifa"]
                }]

        # Actualizar la cantidad de boletas vendidas según las compras realizadas
        for cliente in clientes:
            for evento_info in datos_artistas.get(cliente["nombre"], []):
                if evento_info["nombre_evento"] == cliente["evento"]:
                    evento_info["boletas_vendidas"] += cliente["cantidad_boletas"]

        if datos_artistas:
            for artista, eventos_info in datos_artistas.items():
                st.markdown(f"<h3 style='font-size: 20px;'>Artista: {artista}</h3>",
                            unsafe_allow_html=True)  # Aumentar tamaño del nombre del artista
                for evento_info in eventos_info:
                    st.write(f"Nombre del evento: {evento_info['nombre_evento']}")
                    st.write(f"Fecha: {evento_info['fecha']}")
                    st.write(f"Lugar: {evento_info['lugar']}")
                    st.write(f"Boletas Vendidas: {evento_info['boletas_vendidas']}")
                    st.write(f"Tarifa del artista: ${evento_info['tarifa_artista']}")
                    st.write("---")
        else:
            st.write("No hay datos de artistas para mostrar.")
    else:
        st.write("Evento no encontrado.")


if __name__ == "__main__":
    main()
