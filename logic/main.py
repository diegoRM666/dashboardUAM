import bd as bdc
import graficas as graphLocal
import pandas as pd
import streamlit as st
import os



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
    salon, edificio, fecha_inicio = graphLocal.obtener_salon()

    # Generamos las graficas y las desplegamos
    uso_salon, uso_diario= graphLocal.uso_salon_dia(salon, edificio, fecha_inicio)

    # Hacemos columnas para que se vea mejor
    col1, col2 = st.columns(2)

    if uso_diario!=None or uso_diario!=None:
        with col1: 
            # Mostrar la gráfica en Streamlit
            st.plotly_chart(uso_salon, use_container_width=True)
        with col2: 
            st.plotly_chart(uso_diario, use_container_width=True)


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

    profesor_seleccionado, start_date2 = graphLocal.obtener_profesor()
    preferencias = graphLocal.obtener_preferencias(profesor_seleccionado)
    profesor_it = graphLocal.profesor_itinerario(profesor_seleccionado, start_date2)


    col1,col2 = st.columns(2)
    
    with col1: 
        if not preferencias.empty: 
            st.markdown("### Preferencias Atmosfericas")
            st.markdown(f"👤 **Nombre**: {preferencias.iloc[0,0]}")
            st.markdown(f"🪪 **RFID**: {preferencias.iloc[0,1]}")
            st.markdown(f"🌡️ **:red[Temperatura]**: *{preferencias.iloc[0,2]}* °C")
            st.markdown(f"💧 **:blue[Humedad]**: *{preferencias.iloc[0,3]}* g/m³")
            st.markdown(f"💡 **:orange[Luminosidad]**: *{preferencias.iloc[0,4]}* lx")

    with col2: 
        with st.form(key='form_actualizar_pa'):
            st.write("### Actualizar preferencias atmosféricas")
            
            # Campos de entrada para nuevas preferencias
            nueva_temperatura = st.number_input("Nueva Temperatura (ºC))", min_value=0.0, max_value=50.0, value=preferencias.at[0, 'temperatura'])
            nueva_humedad = st.number_input("Nueva Humedad (g/m³)", min_value=0.0, max_value=100.0, value=preferencias.at[0, 'humedad'])
            nueva_luminosidad = st.number_input("Nueva Luminosidad (lx)", min_value=0.0, max_value=10000.0, value=preferencias.at[0, 'luminosidad'])

            # Botón para enviar cambios
            submit_button = st.form_submit_button(label="Actualizar Preferencias")
            if submit_button:
                graphLocal.cambiar_preferencias(nueva_temperatura, nueva_humedad, nueva_luminosidad, profesor_seleccionado)
                st.success("Preferencias atmosféricas actualizadas exitosamente.")
                st.rerun()

    if  not profesor_it.empty:
        st.markdown("### Itinerario")
        st.table(profesor_it)



############################## Creación Reportes ##############################
with tab3:
    st.markdown("-----------")
    st.markdown("## Generación de reportes")

    col1, col2 = st.columns([2,3])

    with col1:
        fecha_selected = st.selectbox("Selecciona un rango de fechas para generar el reporte: ",
                ("1 mes", "3 meses", "6 meses", "1 año"),
                index=3)
        
        if fecha_selected == '1 mes':
            st.warning("Usted escogio un mes")
        elif fecha_selected == '3 meses':
            st.warning("Usted escogio 3 meses")
        elif fecha_selected == '6 meses':
            st.warning("Usted escogio 6 meses")
        elif fecha_selected == '1 año':
            st.warning("Usted escogio 1 año")
        
    
