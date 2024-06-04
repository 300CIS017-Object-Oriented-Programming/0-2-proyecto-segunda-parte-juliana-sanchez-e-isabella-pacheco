import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generar_reporte_artistas(info_evento):
    st.subheader("Reporte de Artistas")

    if info_evento:
        datos_artistas = {}

        # Recorrer todos los artistas del evento seleccionado
        for artista, tarifa in info_evento["artistas"].items():
            if info_evento["tipo"] == "Bar":
                tarifi = info_evento["ingreso"] / len(info_evento["artistas"]) + tarifa
            else:
                tarifi = tarifa
            # Si el artista ya existe en los datos_artistas, agregar la información del evento actual
            datos_artistas[artista] = [{
                "nombre_evento":
                    info_evento["nombre_evento"],
                "fecha":
                    info_evento["fecha"],
                "lugar":
                    info_evento["ubicacion"],
                "boletas_vendidas":
                    info_evento["boletas_vendidas"],
                "tarifa_artista":
                    tarifi
            }]

        # Mostrar el reporte de artistas
        if datos_artistas:
            for artista, eventos_info in datos_artistas.items():
                st.markdown(
                    f"<h3 style='font-size: 20px;'>Artista: {artista}</h3>",
                    unsafe_allow_html=True
                )  # Aumentar tamaño del nombre del artista
                for evento_info in eventos_info:
                    st.write(
                        f"Nombre del evento: {evento_info['nombre_evento']}")
                    st.write(f"Fecha: {evento_info['fecha']}")
                    st.write(f"Lugar: {evento_info['lugar']}")
                    st.write(
                        f"Boletas Vendidas: {evento_info['boletas_vendidas']}")
                    st.write(
                        f"Tarifa del artista: ${evento_info['tarifa_artista']}"
                    )
                    st.write("---")
        else:
            st.write("No hay datos de artistas para mostrar.")
    else:
        st.write("Evento no encontrado.")

def generar_reporte_ventas(evento_info_bar, evento_info_filantropic, evento_info_teatro, clientes):
        st.subheader("Reporte de Ventas")

        # Diccionario para almacenar las ventas por evento y categoría
        ventas = {}

        # Calcular las ventas por evento y categoría
        for evento in evento_info_bar:
            if evento:
                cantidad_boletas_regular = 0
                # Calcular los ingresos a partir del costo de las boletas vendidas
                ingresos = 0
                cantidad_cortesias = evento["cantidad_cortesias"]
                cantidad_preventa = 0
                ingreso_preventa = 0
                categorias = {}
                for boleta in evento["boletas"]:
                    if boleta["preventa"]:
                        cantidad_preventa += 1
                        ingreso_preventa += boleta["precio"]
                    else:
                        cantidad_boletas_regular += 1
                    ingresos += boleta["precio"]
                    if boleta["categoria"] not in categorias:
                        categorias[boleta["categoria"]] = 0
                    categorias[boleta["categoria"]] += boleta["precio"]
                # Calcular el costo de los comediantes
                costo_artista = evento["costo_artistas"]
                total = ingresos - (costo_artista)
                st.write(f"Evento: {evento['nombre']}")
                st.write(f"Total Ingresos Bar (20% retribución): ${total*0.2}")
                st.write(f"{cantidad_cortesias} Cantidad de boletas")
                st.write(f"Se vendieron {cantidad_preventa} boletas en Preventa con ingreso total de ${ingreso_preventa}")
                st.write(f"Se vendieton un total de {cantidad_boletas_regular} "
                         f"boletas en fase regular con un ingreso de ${ingresos - ingreso_preventa}")
                for categoria, totalito in categorias.items():
                    if categoria != "cortesia":
                        st.write(f"Se obtuvo un ingreso de  ${totalito} en la categoria {categoria}")
                st.write(f"Se vendieron {cantidad_cortesias} cortesias")

        for evento in evento_info_filantropic:
            if evento:
                # Calcular los ingresos a partir de los aportes de los patrocinadores
                ingresos = 0
                for patrocinador in evento["patrocinadores"].values():
                    ingresos += patrocinador
                st.write(f"Evento: {evento['nombre']}")
                st.write(f"Ingresos totales por los aportes de los patrocinadores: {ingresos}")
                st.write(f"Se vendieron {evento['cantidad_boletas']} boletas")


        for evento in evento_info_teatro:
            if evento:
                cantidad_boletas_regular = 0
                ingresos = 0
                cantidad_cortesias = evento["cantidad_cortesias"]
                cantidad_preventa = 0
                ingreso_preventa = 0
                categorias = {}
                for boleta in evento["boletas"]:
                    precio = boleta["precio"]
                    if boleta["preventa"]:
                        cantidad_preventa += 1
                        ingreso_preventa += precio - precio*0.07
                    else:
                        cantidad_boletas_regular += 1
                    ingresos += precio - precio*0.07
                    if boleta["categoria"] not in categorias:
                        categorias[boleta["categoria"]] = 0
                    categorias[boleta["categoria"]] += precio - precio

                costo_alquiler = evento["costo_alquiler"]
                total = ingresos - costo_alquiler
                st.write(f"Evento: {evento['nombre']}")
                st.write(f"Total Ingresos: ${total}")
                st.write(
                    f"Se vendieron {cantidad_preventa} boletas en Preventa con ingreso total de ${ingreso_preventa}")
                st.write(f"Se vendieton un total de {cantidad_boletas_regular} "
                         f"boletas en fase regular con un ingreso de ${ingresos - ingreso_preventa}")
                for categoria, totalito in categorias.items():
                    if categoria != "cortesia":
                        st.write(f"Se obtuvo un ingreso de  ${totalito} en la categoria {categoria}")
                st.write(f"Se vendieron {cantidad_cortesias} cortesias")

        if clientes:
            st.table(clientes)

def generar_reporte_financiero_bar(evento):
    cantidad_boletas_regular = 0
    ingresos = 0
    cantidad_cortesias = evento["cantidad_cortesias"]
    metodos = {"Tarjeta": 0,
               "Trasnferencia": 0,
               "Efectivo": 0
               }
    cantidad_preventa = 0
    ingreso_preventa = 0
    ganancias_taquill = 0
    categorias = {}
    for boleta in evento["boletas"]:
        precio = boleta["precio"]
        if boleta["preventa"]:
            cantidad_preventa += 1
            ingreso_preventa += precio - precio * 0.07
        else:
            cantidad_boletas_regular += 1
        ingresos += precio - precio * 0.07
        ganancias_taquill += precio * 0.07
        if boleta["categoria"] not in categorias:
            categorias[boleta["categoria"]] = 0
        categorias[boleta["categoria"]] += precio - precio
        if boleta["metodo"] == "Transferencia bancaria":
            metodos["Trasnferencia"] += precio
        elif boleta["metodo"] == "Efectivo":
            metodos["Efectivo"] += precio
        else:
            metodos["Tarjeta"] += precio

    costo = evento["costo_artistas"]
    st.subheader("Reporte Financiero")
    st.write(f"Evento: {evento['nombre']}")
    st.write(f"Total ganancia: {ingresos - costo}")
    st.write(f"Se ha pagado ${costo} a los artistas")
    st.write(
        f"Se vendieron {cantidad_preventa} boletas en Preventa con ingreso total de ${ingreso_preventa}")
    st.write(f"Se vendieton un total de {cantidad_boletas_regular} "
             f"boletas en fase regular con un ingreso de ${ingresos - ingreso_preventa}")
    for categoria, totalito in categorias.items():
        if categoria != "cortesia":
            st.write(f"Se obtuvo un ingreso de  ${totalito} en la categoria {categoria}")
    st.write(f"Se vendieron {cantidad_cortesias} cortesias")
    st.write(f"La taquilla ha retenido un total de ${ganancias_taquill}")
    st.table(metodos)

def generar_reporte_financiero_filantropico(evento_info):
    st.subheader("Reporte Financiero")

    ingresos = 0
    for patrocinador in evento_info["patrocinadores"].values():
        ingresos += patrocinador

    st.write(f"Evento: {evento_info['nombre']}")
    st.write(f"\nSe le ha pagado a los artista un total de ${evento_info['costo_artistas']} ")
    st.write("Los patrocinasdores:")
    st.table(evento_info["patrocinadores"])
    st.write(f"Se ha obtenido un total de ${ingresos-evento_info['costo_artistas']}")

def generar_reporte_financiero_teatro(evento):
    cantidad_boletas_regular = 0
    ingresos = 0
    cantidad_cortesias = evento["cantidad_cortesias"]
    metodos = {"Tarjeta": 0,
               "Trasnferencia": 0,
               "Efectivo": 0
    }
    cantidad_preventa = 0
    ingreso_preventa = 0
    ganancias_taquill = 0
    categorias = {}
    for boleta in evento["boletas"]:
        precio = boleta["precio"]
        if boleta["preventa"]:
            cantidad_preventa += 1
            ingreso_preventa += precio - precio * 0.07
        else:
            cantidad_boletas_regular += 1
        ingresos += precio - precio * 0.07
        ganancias_taquill += precio * 0.07
        if boleta["categoria"] not in categorias:
            categorias[boleta["categoria"]] = 0
        categorias[boleta["categoria"]] += precio - precio
        if boleta["metodo"] == "Transferencia bancaria":
            metodos["Trasnferencia"] += precio
        elif boleta["metodo"] == "Efectivo":
            metodos["Efectivo"] += precio
        else:
            metodos["Tarjeta"] += precio

    costo_alquiler = evento["costo_alquiler"]
    total = ingresos - costo_alquiler
    st.subheader("Reporte Financiero")
    st.write(f"Evento: {evento['nombre']}")
    st.write(f"Total ganancia: {ingresos-evento['costo_alquiler']}")
    st.write(f"Se ha pagado ${evento['costo_alquiler']} por alquiler")
    st.write(
        f"Se vendieron {cantidad_preventa} boletas en Preventa con ingreso total de ${ingreso_preventa}")
    st.write(f"Se vendieton un total de {cantidad_boletas_regular} "
             f"boletas en fase regular con un ingreso de ${ingresos - ingreso_preventa}")
    for categoria, totalito in categorias.items():
        if categoria != "cortesia":
            st.write(f"Se obtuvo un ingreso de  ${totalito} en la categoria {categoria}")
    st.write(f"Se vendieron {cantidad_cortesias} cortesias")
    st.write(f"La taquilla ha retenido un total de ${ganancias_taquill}")
    st.table(metodos)

def generar_reporte_compradores(info_clientes):
    st.subheader("Reporte de Compradores")

    if info_clientes:
        # Convertir los datos de los clientes a un DataFrame de Pandas
        df_clientes = pd.DataFrame(info_clientes)

        # Generar el PDF del reporte
        pdf_reporte = BytesIO()
        doc = SimpleDocTemplate(pdf_reporte, pagesize=letter)

        # Crear estilo de párrafo
        styles = getSampleStyleSheet()
        styleN = styles['Normal']
        styleH = styles['Heading1']

        # Convertir el DataFrame a una tabla de ReportLab
        data = [df_clientes.columns.tolist()] + df_clientes.values.tolist()
        table = Table(data)

        # Estilo de la tabla
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), '#77DCE7'),
            ('TEXTCOLOR', (0, 0), (-1, 0), (0, 0, 0)),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), '#E6F0ED'),
            ('GRID', (0, 0), (-1, -1), 1, '#ffffff')
        ])
        table.setStyle(style)

        # Agregar la tabla al documento
        elements = []
        # elements.append(Paragraph('Reporte de Compradores', styleH)) # Comentado temporalmente
        elements.append(table)
        doc.build(elements)

        # Descargar el PDF
        st.download_button(
            label="Descargar Reporte PDF",
            data=pdf_reporte.getvalue(),
            file_name="reporte_compradores.pdf",
            mime="application/pdf"
        )

        # Mostrar la tabla de clientes
        st.table(df_clientes)

        # Crear un diccionario para almacenar el número de boletas vendidas por evento
        boletas_por_evento = {}

        # Contar el número de boletas vendidas por evento
        for cliente in info_clientes:
            evento_actual = cliente["evento"]
            boletas_actuales = cliente["cantidad_boletas"]
            boletas_por_evento[evento_actual] = boletas_por_evento.get(evento_actual, 0) + boletas_actuales

        # Convertir el diccionario en un DataFrame de Pandas para la gráfica
        df_boletas_por_evento = pd.DataFrame(
            list(boletas_por_evento.items()),
            columns=["Evento", "Boletas Vendidas"]
        )

        # Generar la gráfica de barras con el número de boletas vendidas por evento
        st.subheader("Gráfica de boletas vendidas por evento")
        st.bar_chart(df_boletas_por_evento.set_index("Evento"))
    else:
        st.write("No hay datos de clientes aún.")
