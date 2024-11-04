import bd as bdc
import pandas as pd
import streamlit as st
import plotly.graph_objects as go


def ocupacion_salonesDB():
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


        print (ocupacion_salon)

        # Agrupar por profesor y sumar la duración total de horas
        duracion_por_profesor = ocupacion_salon.groupby('profesor')['duracion_horas'].sum().reset_index()

        with col1:
            # Crear la gráfica de dona
            fig_dona = go.Figure(
                go.Pie(
                    labels=duracion_por_profesor['profesor'],
                    values=duracion_por_profesor['duracion_horas'],
                    hole=0.4,  # Esto crea el efecto de dona
                    textinfo='label+percent',
                    hoverinfo='label+value'
                )
            )

            # Configurar el título de la gráfica
            fig_dona.update_layout(title_text="Tiempo de uso del salón por profesor (horas)",
                                paper_bgcolor='rgba(0, 0, 0, 0)',  # Fondo del papel transparente
                                plot_bgcolor='rgba(0, 0, 0, 0)',  # Fondo del gráfico transparente
                                height = 400,
                                width = 400)
            
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
                    textinfo='label+percent',
                    hoverinfo='label+value'
                )

            )

            # Configurar el título de la gráfica
            fig_dona2.update_layout(title_text="Tiempo de uso por día (horas)",
                                paper_bgcolor='rgba(0, 0, 0, 0)',  # Fondo del papel transparente
                                plot_bgcolor='rgba(0, 0, 0, 0)',  # Fondo del gráfico transparente
                                height = 400,
                                width = 400)
            
            # Mostrar la gráfica en Streamlit
            st.plotly_chart(fig_dona2, use_container_width=True)
        
        
    else:
        st.write("No hay datos disponibles para el salón seleccionado.")


    
    
        