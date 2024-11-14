import bd as bdc
import graficas as graphLocal
import pandas as pd
import streamlit as st
import os



############################## Titulo ##############################
st.set_page_config(layout="centered")
col1, col2 = st.columns([1,1])


with col1: 
    st.image("../img/CBI_Blanco/CBI_icono.png", use_column_width=True)
with col2: 
    st.markdown("# Sensores Salones")
    st.markdown("Aplicación para monitoreo de salones")
    st.markdown("Área de Sistemas")
    st.markdown("Leonardo Daniel Sánchez Martinez")
    st.markdown("Creado por Diego Ruiz Mora ©")


############################## Dashboard Ocupación ##############################

graphLocal.ocupacion_salonesDB()
graphLocal.profesor_pa()


############################## Creación Reportes ##############################

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
        
    
