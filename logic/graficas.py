import bd as bdc
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO


def transformar_fechas(time_range):
    end_date = datetime.today()

    if time_range == "1 Semana":
        start_date = end_date - timedelta(days=7)
    elif time_range == "1 Mes":
        start_date = end_date - timedelta(days=30)
    elif time_range == "3 Meses":
        start_date = end_date - timedelta(days=90)
    elif time_range == "6 Meses": 
        start_date = end_date - timedelta(days=180)
    elif time_range == "Todo el tiempo":
        start_date = '2024-01-01 00:00:00'
    
    return start_date

def obtener_visitas_tiempo(salon, edificio, start_date, end_date):
    visitas = bdc.consultar(
        f"SELECT DATE(v.visita_entrada) AS fecha, count(*) AS visitas "
        f"FROM visita v INNER JOIN salon s ON v.idsalon = s.idsalon "
        f"WHERE v.visita_entrada >= '{start_date}' "
        f"AND v.visita_entrada < '{end_date}' "
        f"AND s.salon = '{salon}' "
        f"AND s.edificio = '{edificio}' "
        f"GROUP BY fecha;"
        )
    

    if isinstance(visitas, pd.DataFrame) and not visitas.empty:
        # Graficación
        fig_pol1 = go.Figure()

        fig_pol1.add_trace(go.Scatter(
            x=visitas['fecha'], 
            y=visitas['visitas'],
            mode='lines+markers',  # Modo "líneas y puntos"
            name='Cantidad Queries',
        ))

        fig_pol1.update_layout(
                    title="Visitas en Salón",
                    xaxis_title="Fecha",
                    yaxis_title="Cantidad de Visitas",
                    paper_bgcolor='rgba(0, 0, 0, 0)',  # Fondo transparente
                    plot_bgcolor='rgba(0, 0, 0, 0)'    # Fondo de la cuadrícula transparente
                )
        
        return fig_pol1

    elif visitas.empty:
        st.warning(f"No hay datos para el tiempo referido")
        return None


def obtener_salones():
    # Ejecutar la consulta y obtener los resultados en un DataFrame
    salones = bdc.consultar("SELECT edificio, salon FROM salon;")
    return salones

def uso_salon_dia(salon_seleccionado, edificio_seleccionado, start_date, end_date):
    # Consulta para obtener los datos en un DataFrame
    ocupacion_salon = bdc.consultar(
        f"SELECT s.edificio AS edificio, s.salon AS salon, v.visita_entrada AS entrada, "
        f"v.visita_salida AS salida, p.nombre AS profesor "
        f"FROM salon s "
        f"INNER JOIN visita v ON s.idsalon = v.idsalon "
        f"INNER JOIN profesor p ON v.idprofesor = p.idprofesor "
        f"WHERE s.salon = {salon_seleccionado} AND s.edificio = '{edificio_seleccionado}' "
        f"AND v.visita_entrada >= '{start_date}' "
        f"AND v.visita_entrada <= '{end_date}';"
    )

    #Generacion de columnas para que se vea como un dashboard
    col1, col2 = st.columns([1,1])
    # Mostrar el DataFrame en Streamlit
    if isinstance(ocupacion_salon, pd.DataFrame) and not ocupacion_salon.empty:
        # Convertir las columnas de tiempo
        ocupacion_salon['entrada'] = pd.to_datetime(ocupacion_salon['entrada'])
        ocupacion_salon['salida'] = pd.to_datetime(ocupacion_salon['salida'])
        
        # Calcular la duración en horas para cada visita
        ocupacion_salon['duracion_horas'] = (ocupacion_salon['salida'] - ocupacion_salon['entrada']).dt.total_seconds() / 3600

        # Agrupar por profesor y sumar la duración total de horas
        duracion_por_profesor = ocupacion_salon.groupby('profesor')['duracion_horas'].sum().reset_index()

        # Crear la gráfica de dona
        fig_dona = go.Figure(
            go.Pie(
                labels=duracion_por_profesor['profesor'],
                values=duracion_por_profesor['duracion_horas'],
                hole=0.4,  # Esto crea el efecto de dona
                textinfo='label',
                hoverinfo='label+value',
                showlegend=False
            )
        )

        # Configurar el título de la gráfica
        fig_dona.update_layout(title_text="Tiempo de uso del salón por profesor (horas)",
                            paper_bgcolor='rgba(0, 0, 0, 0)',  # Fondo del papel transparente
                            plot_bgcolor='rgba(0, 0, 0, 0)',  # Fondo del gráfico transparente
                            height = 500,
                            width = 500)

        # Separar en fecha y hora
        ocupacion_salon['fecha_entrada'] = ocupacion_salon['entrada'].dt.date
        ocupacion_salon['hora_entrada'] = ocupacion_salon['entrada'].dt.time

        duracion_por_dia = ocupacion_salon.groupby('fecha_entrada')['duracion_horas'].sum().reset_index()

        # Crear la gráfica de dona
        fig_dona2 = go.Figure(
            go.Pie(
                labels=duracion_por_dia['fecha_entrada'],
                values=duracion_por_dia['duracion_horas'],
                hole=0.4,  # Esto crea el efecto de dona
                textinfo='label',
                hoverinfo='label+value',
                showlegend=False
            )

        )

        # Configurar el título de la gráfica
        fig_dona2.update_layout(title_text="Tiempo de uso por día (horas)",
                            paper_bgcolor='rgba(0, 0, 0, 0)',  # Fondo del papel transparente
                            plot_bgcolor='rgba(0, 0, 0, 0)',  # Fondo del gráfico transparente
                            height = 500,
                            width = 500)
        

        #actualizacion_condicion(salon_seleccionado, edificio_seleccionado)
        return fig_dona, fig_dona2
    
    elif ocupacion_salon.empty:
        st.warning(f"No hay datos para el tiempo referido")
        return None, None
        
    else:
        st.error(f"Error: {ocupacion_salon}")
        return None, None
    
def condicion_salon (salon_seleccionado, edificio_seleccionado, start_date):
    # Condiciones del salon: 

    condiciones_salon = bdc.consultar(
        f"SELECT s.edificio AS edificio, s.salon AS salon, c.temperatura AS temperatura, " 
        f"c.humedad AS humedad, c.luminosidad AS luminosidad, time_condicion AS fecha "
        f"FROM salon s "
        f"INNER JOIN condicion c ON c.idsalon = s.idsalon "
        f"WHERE s.salon = {salon_seleccionado} AND s.edificio = '{edificio_seleccionado}'"
        f"AND time_condicion >= '{start_date}';")

    if isinstance(condiciones_salon, pd.DataFrame) and not condiciones_salon.empty:

        # Convertir la columna de fechas a tipo datetime
        condiciones_salon['fecha'] = pd.to_datetime(condiciones_salon['fecha'])

        # Crear la figura de la gráfica de línea
        fig_temperatura = go.Figure()

        # Añadir la línea de temperatura al gráfico
        fig_temperatura.add_trace(go.Scatter(
            x=condiciones_salon['fecha'], 
            y=condiciones_salon['temperatura'],
            mode='lines+markers',  # Modo "líneas y puntos"
            name='Temperatura',
            line=dict(color='red'),  # Color de la línea
            marker=dict(size=6)  # Tamaño de los puntos
        ))

        # Configuración de la gráfica
        fig_temperatura.update_layout(
            title="Variación de la Temperatura en el Tiempo",
            xaxis_title="Fecha",
            yaxis_title="Temperatura (°C)",
            paper_bgcolor='rgba(0, 0, 0, 0)',  # Fondo transparente
            plot_bgcolor='rgba(0, 0, 0, 0)'    # Fondo de la cuadrícula transparente
        )

        ####################################################################################### 

        # Convertir la columna de fechas a tipo datetime
        condiciones_salon['fecha'] = pd.to_datetime(condiciones_salon['fecha'])

        # Crear la figura de la gráfica de línea
        fig_humedad = go.Figure()

        # Añadir la línea de temperatura al gráfico
        fig_humedad.add_trace(go.Scatter(
            x=condiciones_salon['fecha'], 
            y=condiciones_salon['humedad'],
            mode='lines+markers',  # Modo "líneas y puntos"
            name='Humedad',
            line=dict(color='blue'),  # Color de la línea
            marker=dict(size=6)  # Tamaño de los puntos
        ))

        # Configuración de la gráfica
        fig_humedad.update_layout(
            title="Variación de la Humedad en el Tiempo",
            xaxis_title="Fecha",
            yaxis_title="Humedad (g/m^3)",
            paper_bgcolor='rgba(0, 0, 0, 0)',  # Fondo transparente
            plot_bgcolor='rgba(0, 0, 0, 0)'    # Fondo de la cuadrícula transparente
        )

        #######################################################################################

        # Convertir la columna de fechas a tipo datetime
        condiciones_salon['fecha'] = pd.to_datetime(condiciones_salon['fecha'])

        # Crear la figura de la gráfica de línea
        fig_luminosidad = go.Figure()

        # Añadir la línea de luminosidad al gráfico
        fig_luminosidad.add_trace(go.Scatter(
            x=condiciones_salon['fecha'], 
            y=condiciones_salon['luminosidad'],
            mode='lines+markers',  # Modo "líneas y puntos"
            name='Luminosidad',
            line=dict(color='yellow'),  # Color de la línea
            marker=dict(size=6)  # Tamaño de los puntos
        ))

        # Configuración de la gráfica
        fig_luminosidad.update_layout(
            title="Variación de la Luminosidad en el Tiempo",
            xaxis_title="Fecha",
            yaxis_title="Luminosidad (lx)",
            paper_bgcolor='rgba(0, 0, 0, 0)',  # Fondo transparente
            plot_bgcolor='rgba(0, 0, 0, 0)'    # Fondo de la cuadrícula transparente
        )


        #######################################################################################
        # Convertir la columna de fechas a tipo datetime
        condiciones_salon['fecha'] = pd.to_datetime(condiciones_salon['fecha']).dt.date

        # Agrupar por fecha y calcular el promedio
        promedios = condiciones_salon.groupby('fecha')[['temperatura', 'humedad', 'luminosidad']].mean().reset_index()
        promedios = promedios.rename(columns={'temperatura': 'temperaturaAVG', 'humedad': 'humedadAVG', 'luminosidad': 'luminosidadAVG'})

        return fig_temperatura, fig_humedad, fig_luminosidad, promedios

    else:
        st.warning("No hay datos para el tiempo referido")
        return None, None, None, pd.DataFrame()


