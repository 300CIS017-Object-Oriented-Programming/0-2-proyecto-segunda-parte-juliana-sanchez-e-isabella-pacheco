import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from io import BytesIO
from reportlab.lib.pagesizes import letter

def generar_reporte_artistas(nombre_artista, info_evento):
    pass

def generar_reporte_ventas(vendidas, ingresos_preventa, ingresos_regular, nombre_evento):
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
                    ingresos = sum(
                        cantidad_boletas * c["costo"] for c in evento["categoria"] if c["nombre"] == "Boleta")
                    # Calcular el costo de los artistas y el costo de alquiler
                    costo_artista = sum(a["tarifa"] for a in evento["artistas"])
                    costo_alquiler = evento["costo_alquiler"]
                elif tipo_evento == "Bar":
                    # Calcular los ingresos a partir del costo de las boletas vendidas
                    ingresos = sum(
                        c["costo"] * cantidad_boletas for c in evento["categoria"] if c["nombre"] == "Boleta")
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