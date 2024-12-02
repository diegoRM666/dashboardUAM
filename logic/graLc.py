import plotly.graph_objects as go
import sys
import bd as bdc
import pandas as pd
from datetime import datetime, timedelta

salon = sys.argv[1]
edificio = sys.argv[2]
start_date = sys.argv[3]
end_date = sys.argv[4]
rango = sys.argv[5]


# Consulta para obtener los datos en un DataFrame
condiciones_salon = bdc.consultar(
        f"SELECT s.edificio AS edificio, s.salon AS salon, c.temperatura AS temperatura, " 
        f"c.humedad AS humedad, c.luminosidad AS luminosidad, time_condicion AS fecha "
        f"FROM salon s "
        f"INNER JOIN condicion c ON c.idsalon = s.idsalon "
        f"WHERE s.salon = {salon} AND s.edificio = '{edificio}'"
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
        plot_bgcolor='rgba(0, 0, 0, 0)',    # Fondo de la cuadrícula transparente
        xaxis = dict(gridcolor ="grey"),
        yaxis = dict(gridcolor ="grey")
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
        plot_bgcolor='rgba(0, 0, 0, 0)',    # Fondo de la cuadrícula transparente
        xaxis = dict(gridcolor ='grey'),
        yaxis = dict(gridcolor ='grey')
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
        plot_bgcolor='rgba(0, 0, 0, 0)',    # Fondo de la cuadrícula transparente
        xaxis = dict(gridcolor ='grey'),
        yaxis = dict(gridcolor ='grey')
    )


    #######################################################################################
    # Convertir la columna de fechas a tipo datetime
    condiciones_salon['fecha'] = pd.to_datetime(condiciones_salon['fecha']).dt.date

    # Agrupar por fecha y calcular el promedio
    promedios = condiciones_salon.groupby('fecha')[['temperatura', 'humedad', 'luminosidad']].mean().reset_index()
    promedios = promedios.rename(columns={'temperatura': 'temperaturaAVG', 'humedad': 'humedadAVG', 'luminosidad': 'luminosidadAVG'})

    tabla_avg = go.Figure(go.Table(
        header=dict(values=promedios.columns),
        cells=dict(values=[promedios[col] for col in promedios.columns])
    ))

    #######################################################################################
    # Guardar Imagenes
    graName1 = f"TS{salon}-{rango}-{datetime.today().strftime("%d-%m-%Y")}.png" 
    graName2 = f"HS{salon}-{rango}-{datetime.today().strftime("%d-%m-%Y")}.png" 
    graName3 = f"LS{salon}-{rango}-{datetime.today().strftime("%d-%m-%Y")}.png" 
    tableName = f"CAVG{salon}-{rango}-{datetime.today().strftime("%d-%m-%Y")}.png" 
    fig_temperatura.write_image(f"../img/poli/{graName1}")
    fig_humedad.write_image(f"../img/poli/{graName2}")
    fig_luminosidad.write_image(f"../img/poli/{graName3}")
    tabla_avg.write_image(f"../img/tables/{tableName}")