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