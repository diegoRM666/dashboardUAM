import bd as bdc
import graficas as graphLocal
import pandas as pd
import streamlit as st


############################## Titulo ##############################
st.title("Sensores Salones")

############################## Dashboard Ocupación ##############################

graphLocal.ocupacion_salonesDB()