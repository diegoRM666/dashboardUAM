import bd as bdc
import graficas as graphLocal
import pandas as pd
import streamlit as st
import reportes as rp
from datetime import datetime



############################## Titulo ##############################
st.set_page_config(layout="wide")
col1, col2, col3, col4 = st.columns(4)


with col1: 
    st.image("../img/CBI_Blanco/CBI_icono.png", width=300)
with col2: 
    st.markdown("# Sensores Salones")
    st.markdown("Aplicación para monitoreo de salones")
    st.markdown("Área de Sistemas")
    st.markdown("Leonardo Daniel Sánchez Martinez")
    st.markdown("Creado por Diego Ruiz Mora ©")


############################## Creación Pestañas ##############################
# Crear pestañas
tab1, tab2, tab3 = st.tabs(["Dashboard", "Profesores", "Reportes"])



############################## Dashboard  ##############################
########### Ocupación y condicion de salones ###########
with tab1: 
    st.markdown("## Ocupabilidad Salones")
    # Ejecutar la consulta y obtener los resultados en un DataFrame 
    salones = graphLocal.obtener_salones()

    # Desplegar los selectbox
    col01, col02= st.columns([1,1])

    with col01: 
        # Selector de Edificio
        edificio = st.selectbox("Selecciona un edificio", salones['edificio'].unique())

        # Filtrar el DataFrame para mostrar solo los salones del edificio seleccionado
        salones_disponibles = salones[salones['edificio'] == edificio]['salon']

        # Selector de Salón
        salon = st.selectbox("Selecciona un salón", salones_disponibles)

    #Otras columnas para darle mejor formato
    col001, col002, col003 = st.columns([1,1,1])
    with col003:
        #Selector de rango de fechas
        time_range = st.selectbox(
        "",
        ("1 Semana", "1 Mes", "3 Meses", "Todo el tiempo"),
        index=3
        )

        fecha_inicio = graphLocal.transformar_fechas(time_range)

    # Generamos las graficas y las desplegamos
    uso_salon, uso_diario= graphLocal.uso_salon_dia(salon, edificio, fecha_inicio, datetime.today())

    # Hacemos columnas para que se vea mejor
    col1, col2 = st.columns(2)

    if uso_diario!=None or uso_diario!=None:
        with col1: 
            # Mostrar la gráfica en Streamlit
            st.plotly_chart(uso_salon, use_container_width=True)
        with col2: 
            st.plotly_chart(uso_diario, use_container_width=True)

    ########### Número de Visitas ###########
    st.markdown("## Número de Visitas")
    fig_visitas = graphLocal.obtener_visitas_tiempo(salon, edificio, fecha_inicio, datetime.today())
    st.plotly_chart(fig_visitas, use_container_width=True)

    ########### Condiciones de los salones ###########
    st.markdown("----")
    st.markdown("## Condiciones Salón")
    # Generación de graficas
    fig_temp, fig_hum, fig_lum, promedios =graphLocal.condicion_salon(salon, edificio, fecha_inicio)

    # Hacemos columnas para que se vea mejor
    col1, col2 = st.columns(2)
    col11, col12 = st.columns(2)

    if fig_temp!=None or fig_hum!=None or fig_lum!=None or not promedios.empty:
        
        with col1: 
            st.plotly_chart(fig_temp, use_container_width=True)
        with col2: 
            st.plotly_chart(fig_hum, use_container_width=True)
        with col11:
            st.plotly_chart(fig_lum, use_container_width=True)
        with col12:
            st.table(promedios) 



############################## Itinerario de profesores ##############################
with tab2:
    st.markdown("## Información profesores")
    ################ Despliegue de Selectbox ################
    profesores = graphLocal.obtener_profesores()
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

        start_date2 = graphLocal.transformar_fechas(time_range2)

    preferencias = graphLocal.obtener_preferencias(profesor_seleccionado)
    profesor_it, numero_visitas = graphLocal.profesor_itinerario(profesor_seleccionado, start_date2)


    col1,col2 = st.columns(2)
    
    with col1: 
        if not preferencias.empty: 
            st.markdown("### Preferencias Atmosfericas")
            st.markdown(f"👤 **Nombre**: {preferencias.iloc[0,0]}")
            st.markdown(f"🪪 **RFID**: {preferencias.iloc[0,1]}")
            st.markdown(f"🌡️ **:red[Temperatura]**: *{preferencias.iloc[0,2]}* °C")
            st.markdown(f"💧 **:blue[Humedad]**: *{preferencias.iloc[0,3]}* g/m³")
            st.markdown(f"💡 **:orange[Luminosidad]**: *{preferencias.iloc[0,4]}* lx")
            st.info(f"Conteo Visitas: {numero_visitas}")

    with col2: 
        with st.form(key='form_actualizar_pa'):
            st.write("### Actualizar preferencias atmosféricas")
            
            # Campos de entrada para nuevas preferencias
            nueva_temperatura = st.number_input("Nueva Temperatura (ºC)", min_value=0.0, max_value=50.0, value=preferencias.at[0, 'temperatura'])
            nueva_humedad = st.number_input("Nueva Humedad (g/m³)", min_value=0.0, max_value=100.0, value=preferencias.at[0, 'humedad'])
            nueva_luminosidad = st.number_input("Nueva Luminosidad (lx)", min_value=0.0, max_value=10000.0, value=preferencias.at[0, 'luminosidad'])

            # Botón para enviar cambios
            submit_button = st.form_submit_button(label="Actualizar Preferencias")
            if submit_button:
                graphLocal.cambiar_preferencias(nueva_temperatura, nueva_humedad, nueva_luminosidad, profesor_seleccionado)
                st.success("Preferencias atmosféricas actualizadas exitosamente.")
                st.rerun()

    ########### Itinerario Profesores ###########
    st.markdown("### Itinerario")
    if  not profesor_it.empty:
        st.table(profesor_it)
    else:
        st.warning("No hay datos del profesor para el tiempo referido")



############################## Creación Reportes ##############################
with tab3:

    st.markdown("## Generación de reportes")
    year_dispo = rp.years_dispo()
    year_select = st.selectbox("Seleccione un año", year_dispo)

    meses_dispo_prev = rp.meses_dispo(year_select)
    meses_dispo = rp.conv_mes_nombre(meses_dispo_prev)
    seleccionados = []

    col1, col2 = st.columns([1,3])

    with col1:
        for mes in meses_dispo:
            if st.checkbox(mes, key=mes):
                seleccionados.append(mes)

    seleccionados_num = rp.conv_nombre_mes(seleccionados)
    
    if st.button("Generar Reporte"):
        if seleccionados:
            with st.spinner(f"Generando el reporte para: {', '.join(seleccionados)}..."):
                rp.salon_edificio(seleccionados_num,year_select)
                st.success(f"Reporte Generado")
                
        else:
            st.warning("Por favor, selecciona al menos un mes para generar el reporte.")
        
    
