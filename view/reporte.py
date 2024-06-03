import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from io import BytesIO
from reportlab.lib.pagesizes import letter

def generar_reporte_artistas(nombre_artista, info_evento):
    pass

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
                    if categorias[boleta["categoria"]] not in categorias:
                        categorias[boleta["categoria"]] = 0
                    categorias[boleta["categoria"]] += precio - precio

                costo_alquiler = evento["costo_alquiler"]
                total = ingresos - costo_alquiler
                st.write(f"Evento: {evento['nombre']}")
                st.write(f"Total Ingresos: ${total}")
                st.write(
                    f"Se vendieron {cantidad_preventa} boletas en Preventa con ingreso total de ${ingreso_preventa}")
                st.write(f"Se vendieton un total de {cantidad_boletas - cantidad_preventa} "
                         f"boletas en fase regular con un ingreso de ${ingresos - ingreso_preventa}")
                for categoria, totalito in categorias.items():
                    if categoria != "cortesia":
                        st.write(f"Se obtuvo un ingreso de  ${totalito} en la categoria {categoria}")
                st.write(f"Se vendieron {cantidad_cortesias} cortesias")

        if clientes:
            st.table(clientes)

def generar_reporte_financiero_bar(ingresos_metodo_pago, ingresos_categorias, pago_artistas, nombre_evento):
    pass

def generar_reporte_financiero_filantropico(patrocinadores,nombre_evento):
    pass

def generar_reporte_financiero_teatro(ingresos_metodo_pago, ingresos_categorias,alquiler,nombre_evento):
    pass

def generar_reporte_compradores(info_clientes):
    st.subheader("Reporte de Compradores")

    if info_clientes:
        # Convertir los datos de los clientes a un DataFrame de Pandas
        df_clientes = pd.DataFrame(info_clientes)

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

        # Agregar la tabla al documento
        doc.build([table])

        # Descargar el PDF
        st.download_button(label="Descargar Reporte PDF",
                           data=pdf_reporte.getvalue(),
                           file_name="reporte_compradores.pdf",
                           mime="application/pdf")

        # Mostrar la tabla de clientes
        st.table(df_clientes)

        # Crear un diccionario para almacenar el número de boletas vendidas por evento
        boletas_por_evento = {}

        # Contar el número de boletas vendidas por evento
        for cliente in info_clientes:
            evento_actual = cliente["eventos"][0]
            boletas_actuales = cliente["cantidad_boletas"]
            boletas_por_evento[evento_actual] = boletas_por_evento.get(
                evento_actual, 0) + boletas_actuales

        # Convertir el diccionario en un DataFrame de Pandas para la gráfica
        df_boletas_por_evento = pd.DataFrame(
            list(boletas_por_evento.items()),
            columns=["Evento", "Boletas Vendidas"])

        # Generar la gráfica de barras con el número de boletas vendidas por evento
        st.subheader("Gráfica de boletas vendidas por evento")
        st.bar_chart(df_boletas_por_evento.set_index("Evento"))
    else:
        st.write("No hay datos de clientes aún.")