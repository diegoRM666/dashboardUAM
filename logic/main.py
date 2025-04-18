import bd as bdc
import graficas as graphLocal
import pandas as pd
import streamlit as st
import reportes as rp
from datetime import datetime
import time
import profesores as pr
from streamlit_autorefresh import st_autorefresh
import threading

st.set_page_config(layout="wide")

############################## Titulo ##############################

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
        "Selecciona un rango",
        ("1 Semana", "1 Mes", "3 Meses", "Todo el tiempo", "Personalizado"),
        index=3
        )

        # Si tenemos un tiempo personalizado
        if time_range == "Personalizado": 
            fecha_1, fecha_2 = graphLocal.obtener_fechas_inicio_fin_personalizado()
            fecha_inicio_prev=st.text_input("Inicio (AAAA-MM-DD):", value=f"{fecha_1} ")
            fecha_fin_prev=st.text_input("Fin (AAAA-MM-DD):", value=f"{fecha_2}")

            # Comprobamos que ambas fechas sean validas
            if fecha_inicio_prev == "" or fecha_fin_prev == "":
                # Si una no cumple entonces se procede con mandar valores sin datos
                st.error("Especifique ambas fechas")
                fecha_inicio ="9999-12-31"
                fecha_fin="9999-12-31"

        # En caso de fechas validas, entonces damos las fechas que se ingresaron
            else:
                fecha_inicio=fecha_inicio_prev
                fecha_fin=fecha_fin_prev
        else:
            fecha_inicio = graphLocal.transformar_fechas(time_range)
            fecha_fin = datetime.today()

    # Generamos las graficas y las desplegamos
    uso_salon, uso_diario= graphLocal.uso_salon_dia(salon, edificio, fecha_inicio, fecha_fin)

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
    fig_visitas, visitas= graphLocal.obtener_visitas_tiempo(salon, edificio, fecha_inicio, fecha_fin)

    # Hacemos columnas para que se aprecie mejor
    col1, col2 = st.columns(2)

    if fig_visitas != None or not visitas.empty:
        with col1:
            st.plotly_chart(fig_visitas, use_container_width=True)
        with col2:
            st.table(visitas)
    
    ########### Promedio de Visitas ###########


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
    profesores = pr.obtener_profesores()
    # Selector de Edificio
    profesor_seleccionado = st.selectbox("Selecciona un profesor", profesores['nombre'].unique())
    #Seleccionemos un rango de fechas 

    col001, col002, col003 = st.columns([1,1,1])
    with col003:
        #Selector de rango de fechas
        time_range2 = st.selectbox(
        "Selecciona un rango",
        ("1 Semana", "1 Mes", "3 Meses", "Todo el tiempo"),
        index=3, 
        key="tab_prof"
        )

        start_date2 = graphLocal.transformar_fechas(time_range2)

    preferencias = pr.obtener_preferencias(profesor_seleccionado)
    profesor_it, numero_visitas = pr.profesor_itinerario(profesor_seleccionado, start_date2)


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
            nueva_humedad = st.number_input("Nueva Humedad (%)", min_value=0.0, max_value=100.0, value=preferencias.at[0, 'humedad'])
            nueva_luminosidad = st.number_input("Nueva Luminosidad (lx)", min_value=0.0, max_value=10000.0, value=preferencias.at[0, 'luminosidad'])

            # Botón para enviar cambios
            submit_button = st.form_submit_button(label="Actualizar Preferencias")
            if submit_button:
                pr.cambiar_preferencias(nueva_temperatura, nueva_humedad, nueva_luminosidad, profesor_seleccionado)
                st.success("Preferencias atmosféricas actualizadas exitosamente.")
                time.sleep(5)
                st.rerun()

        # Botón para regresar a los valores default
        default_button = st.button(label="Valores Default", use_container_width=True)
        if default_button:
            pr.cambiar_preferencias("22.00", "50.00", "300.00", profesor_seleccionado)
            st.success("Preferencias atmosféricas actualizadas a default")
            time.sleep(5)
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

    col1, col2 = st.columns([1,3])

    with col1:
        rango_reporte = st.selectbox(
        "Selecciona un rango",
        ("30 Dias", "90 Dias", "180 Dias")
        )

    if st.button("Generar Reporte"):
        with st.spinner(f"Generando el reporte para: {rango_reporte}..."):
            rp.limpiarcarpetas()
            nombreParcial = rango_reporte.replace(" ", "")
            start_date = rp.transformar_fechas(rango_reporte)

            texto1, texto2, texto3 = rp.graficos_reporte(start_date,datetime.today(),nombreParcial)

            tex_img = f"{texto1}\n{texto3}\n{texto2}"

            tex_path = rp.crear_tex(rango_reporte,nombreParcial, start_date.strftime("%d-%m-%Y"), datetime.today().strftime("%d-%m-%Y"),tex_img)
            rp.compilar_tex(tex_path)

            st.success(f"Reporte generado para los ultimos {rango_reporte}... ")