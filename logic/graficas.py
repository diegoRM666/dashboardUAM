import bd as bdc
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta


def transformar_fechas(time_range):
    end_date = datetime.today()

    if time_range == "1 Semana":
        start_date = end_date - timedelta(days=7)
    elif time_range == "1 Mes":
        start_date = end_date - timedelta(days=30)
    elif time_range == "3 Meses":
        start_date = end_date - timedelta(days=90)
    elif time_range == "Todo el tiempo":
        start_date = '2024-01-01 00:00:00'
    
    return start_date


def obtener_salon():
    # Ejecutar la consulta y obtener los resultados en un DataFrame
    salones = bdc.consultar("SELECT edificio, salon FROM salon;")

    # Unas columnas para organizar los containers. 
    col01, col02= st.columns([1,1])

    with col01: 
        # Selector de Edificio
        edificio_seleccionado = st.selectbox("Selecciona un edificio", salones['edificio'].unique())

        # Filtrar el DataFrame para mostrar solo los salones del edificio seleccionado
        salones_disponibles = salones[salones['edificio'] == edificio_seleccionado]['salon']

        # Selector de Salón
        salon_seleccionado = st.selectbox("Selecciona un salón", salones_disponibles)

    #Otras columnas para darle mejor formato
    col001, col002, col003 = st.columns([1,1,1])
    with col003:
        #Selector de rango de fechas
        time_range = st.selectbox(
        "",
        ("1 Semana", "1 Mes", "3 Meses", "Todo el tiempo"),
        index=3
        )

        start_date = transformar_fechas(time_range)

    return salon_seleccionado, edificio_seleccionado, start_date

def uso_salon_dia(salon_seleccionado, edificio_seleccionado, start_date):

    # Consulta para obtener los datos en un DataFrame
    ocupacion_salon = bdc.consultar(
        f"SELECT s.edificio AS edificio, s.salon AS salon, v.visita_entrada AS entrada, "
        f"v.visita_salida AS salida, p.nombre AS profesor "
        f"FROM salon s "
        f"INNER JOIN visita v ON s.idsalon = v.idsalon "
        f"INNER JOIN profesor p ON v.idprofesor = p.idprofesor "
        f"WHERE s.salon = {salon_seleccionado} AND s.edificio = '{edificio_seleccionado}' "
        f"AND v.visita_entrada >= '{start_date}';"
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

def obtener_profesor():
    # Ejecutar la consulta y obtener los resultados en un DataFrame
    profesores = bdc.consultar("SELECT nombre FROM sensor.profesor;")
    # Selector de Edificio
    profesor_seleccionado = st.selectbox("Selecciona un profesor", profesores['nombre'].unique())
    #Seleccionemos un rango de fechas 

    col001, col002, col003 = st.columns([1,1,1])
    with col003:
        #Selector de rango de fechas
        time_range2 = st.selectbox(
        "",
        ("1 Semana", "1 Mes", "3 Meses", "Todo el tiempo"),
        index=3, 
        key="tab_prof"
        )

        start_date2 = transformar_fechas(time_range2)

    
    return profesor_seleccionado, start_date2

def profesor_itinerario (profesor_seleccionado, start_date2): 
    profesor_it = bdc.consultar(
        f"select s.salon as salon, s.edificio as edificio, v.visita_entrada as entrada, v.visita_salida as salida "
        f"from visita v "
        f"inner join salon s on s.idsalon = v.idsalon "
        f"inner join profesor p on p.idprofesor = v.idprofesor "
        f"where p.nombre = '{profesor_seleccionado}' "
        f"and v.visita_entrada >= '{start_date2}';"
        )
    
    if isinstance(profesor_it, pd.DataFrame) and not profesor_it.empty:
        return profesor_it
    else:
        st.warning("No hay datos para el tiempo referido")
        return pd.DataFrame()

def obtener_preferencias(profesor_seleccionado):
    # Condiciones preferidas
    pa_seleccionada = bdc.consultar(
        f"select p.nombre as nombre, rfid as RFID, pa.temperatura as temperatura, pa.humedad as humedad, pa.luminosidad as luminosidad "
        f"from profesor p inner join preferencias_atmosfericas pa on p.idprofesor = pa.idprofesor "
        f"where p.nombre = '{profesor_seleccionado}' ;")
    
    if isinstance (pa_seleccionada, pd.DataFrame) and not pa_seleccionada.empty:
        reset_pa = pa_seleccionada.reset_index(drop=True)
        return reset_pa

    else: 
        st.error(f"Error: {pa_seleccionada}")

def cambiar_preferencias(nueva_temperatura, nueva_humedad, nueva_luminosidad, profesor_seleccionado):
    # Crear formulario para actualizar preferencias
    # Cóigo para actualizar las preferencias en la base de datos
    bdc.actualizar(
        f"UPDATE preferencias_atmosfericas "
        f"SET temperatura = {nueva_temperatura}, humedad = {nueva_humedad}, luminosidad = {nueva_luminosidad} "
        f"WHERE idprofesor = (SELECT idprofesor FROM profesor WHERE nombre = '{profesor_seleccionado}');"
    )
