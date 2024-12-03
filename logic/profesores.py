import bd as bdc
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta


def obtener_profesores():
    # Ejecutar la consulta y obtener los resultados en un DataFrame
    profesores = bdc.consultar("SELECT nombre FROM sensor.profesor;")
    return profesores

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
        return profesor_it, len(profesor_it)
    else:
        return pd.DataFrame(), 0

def obtener_preferencias(profesor_seleccionado):
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
    bdc.actualizar(
        f"UPDATE preferencias_atmosfericas "
        f"SET temperatura = {nueva_temperatura}, humedad = {nueva_humedad}, luminosidad = {nueva_luminosidad} "
        f"WHERE idprofesor = (SELECT idprofesor FROM profesor WHERE nombre = '{profesor_seleccionado}');"
    )