import bd as bdc
import pandas as pd
import streamlit as st
import plotly.graph_objects as go


def ocupacion_salonesDB():
    #Titulo
    st.markdown("------")
    st.markdown("## Ocupabilidad Salones")
    # Ejecutar la consulta y obtener los resultados en un DataFrame
    salones = bdc.consultar("SELECT edificio, salon FROM sensor.salon;")

    # Selector de Edificio
    edificio_seleccionado = st.selectbox("Selecciona un edificio", salones['edificio'].unique())

    # Filtrar el DataFrame para mostrar solo los salones del edificio seleccionado
    salones_disponibles = salones[salones['edificio'] == edificio_seleccionado]['salon']

    # Selector de Salón
    salon_seleccionado = st.selectbox("Selecciona un salón", salones_disponibles)
    # Consulta para obtener los datos en un DataFrame
    ocupacion_salon = bdc.consultar(
        f"SELECT s.edificio AS edificio, s.salon AS salon, v.visita_entrada AS entrada, "
        f"v.visita_salida AS salida, p.nombre AS profesor "
        f"FROM salon s "
        f"INNER JOIN visita v ON s.idsalon = v.idsalon "
        f"INNER JOIN profesor p ON v.idprofesor = p.idprofesor "
        f"WHERE s.salon = {salon_seleccionado} AND s.edificio = '{edificio_seleccionado}';"
    )

    #Generacion de columnas para que se vea como un dashboard
    col1, col2 = st.columns([1,1])
    # Mostrar el DataFrame en Streamlit
    if ocupacion_salon is not None and not ocupacion_salon.empty:
        # Convertir las columnas de tiempo
        ocupacion_salon['entrada'] = pd.to_datetime(ocupacion_salon['entrada'])
        ocupacion_salon['salida'] = pd.to_datetime(ocupacion_salon['salida'])
        
        # Calcular la duración en horas para cada visita
        ocupacion_salon['duracion_horas'] = (ocupacion_salon['salida'] - ocupacion_salon['entrada']).dt.total_seconds() / 3600

        # Agrupar por profesor y sumar la duración total de horas
        duracion_por_profesor = ocupacion_salon.groupby('profesor')['duracion_horas'].sum().reset_index()

        with col1:
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
            
            # Mostrar la gráfica en Streamlit
            st.plotly_chart(fig_dona, use_container_width=True)

        # Separar en fecha y hora
        ocupacion_salon['fecha_entrada'] = ocupacion_salon['entrada'].dt.date
        ocupacion_salon['hora_entrada'] = ocupacion_salon['entrada'].dt.time

        duracion_por_dia = ocupacion_salon.groupby('fecha_entrada')['duracion_horas'].sum().reset_index()

        with col2:
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
            
            # Mostrar la gráfica en Streamlit
            st.plotly_chart(fig_dona2, use_container_width=True)
    else:
        st.write("No hay datos disponibles para el salón seleccionado.")

    # Condiciones del salon: 
    condiciones_salon = bdc.consultar(
        f"SELECT s.edificio AS edificio, s.salon AS salon, c.temperatura AS temperatura, " 
        f"c.humedad AS humedad, c.luminosidad AS luminosidad, time_condicion AS fecha "
        f"FROM salon s "
        f"INNER JOIN condicion c ON c.idsalon = s.idsalon "
        f"WHERE s.salon = {salon_seleccionado} AND s.edificio = '{edificio_seleccionado}';")
    
    print(condiciones_salon)

    col21, col22 = st.columns([1,1])

    with col21:
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

        st.plotly_chart(fig_temperatura, use_container_width=True)

    with col22:
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

        # Mostrar la gráfica en Streamlit
        st.plotly_chart(fig_humedad, use_container_width=True)

    col31, col32 = st.columns([1,1])

    with col31:
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
        # Mostrar la gráfica en Streamlit
        st.plotly_chart(fig_luminosidad, use_container_width=True)
    
    # Agrupacion por fecha: 


    with col32: 
        # Convertir la columna de fechas a tipo datetime
        condiciones_salon['fecha'] = pd.to_datetime(condiciones_salon['fecha']).dt.date

        # Agrupar por fecha y calcular el promedio
        promedios = condiciones_salon.groupby('fecha')[['temperatura', 'humedad', 'luminosidad']].mean().reset_index()

        # Mostrar los resultados en Streamlit
        st.dataframe(promedios)


def profesor_pa (): 
    st.markdown("## Información profesores")
    # Ejecutar la consulta y obtener los resultados en un DataFrame
    profesores = bdc.consultar("SELECT nombre FROM sensor.profesor;")

    # Selector de Edificio
    profesor_seleccionado = st.selectbox("Selecciona un profesor", profesores['nombre'].unique())

    # Condiciones del salon
    pa_seleccionada = bdc.consultar(
        f"select p.nombre as nombre, rfid as RFID, pa.temperatura as temperatura, pa.humedad as humedad, pa.luminosidad as luminosidad "
        f"from profesor p inner join preferencias_atmosfericas pa on p.idprofesor = pa.idprofesor "
        f"where p.nombre = '{profesor_seleccionado}' ;")
    
    reset_pa = pa_seleccionada.reset_index(drop=True)
    st.table(reset_pa)