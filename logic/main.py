import bd as bdc
import graficas as graphLocal
import pandas as pd
import streamlit as st
import reportes as rp
from datetime import datetime, timedelta
import time
import profesores as pr
from streamlit_autorefresh import st_autorefresh

st.set_page_config(layout="wide")

# Control para evitar que autorefresh interrumpa generación de reportes
if "generando_reporte" not in st.session_state:
    st.session_state.generando_reporte = False

if not st.session_state.generando_reporte:
    st_autorefresh(interval=120000, limit=None, key="dashboard_refresh")

print("···· RUNNING ····")

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

tab1, tab2, tab3 = st.tabs(["Dashboard", "Profesores", "Reportes"])

############################## Dashboard ##############################
with tab1:
    st.markdown("## Ocupabilidad Salones")
    salones = graphLocal.obtener_salones()

    col01, col02 = st.columns([1, 1])
    with col01:
        edificio = st.selectbox("Selecciona un edificio", salones['edificio'].unique())
        salones_disponibles = salones[salones['edificio'] == edificio]['salon']
        salon = st.selectbox("Selecciona un salón", salones_disponibles)

    # Selector de fechas con slider
    fecha_min_str, fecha_max_str = graphLocal.obtener_fechas_inicio_fin_personalizado()
    fecha_min = datetime.strptime(fecha_min_str, "%Y-%m-%d")
    fecha_max = datetime.strptime(fecha_max_str, "%Y-%m-%d")
    fecha_default_inicio = fecha_max - timedelta(days=90)

    st.markdown("### Selecciona el rango de fechas")
    fecha_inicio, fecha_fin = st.slider(
        "Rango de fechas",
        min_value=fecha_min,
        max_value=fecha_max,
        value=(fecha_default_inicio, fecha_max),
        format="DD/MM/YYYY"
    )

    conteo_actual = graphLocal.conteo_registros()
    config_actual = {
        "salon": salon,
        "edificio": edificio,
        "fecha_inicio": fecha_inicio.strftime("%Y-%m-%d"),
        "fecha_fin": fecha_fin.strftime("%Y-%m-%d"),
        "conteo": conteo_actual
    }

    if "config_anterior" not in st.session_state or st.session_state.config_anterior != config_actual:
        st.session_state.config_anterior = config_actual

        uso_salon, uso_diario = graphLocal.uso_salon_dia(salon, edificio, fecha_inicio, fecha_fin)
        fig_visitas, visitas = graphLocal.obtener_visitas_tiempo(salon, edificio, fecha_inicio, fecha_fin)
        fig_temp, fig_hum, fig_lum, promedios = graphLocal.condicion_salon(salon, edificio, fecha_inicio, fecha_fin)

        st.session_state.uso_salon = uso_salon
        st.session_state.uso_diario = uso_diario
        st.session_state.fig_visitas = fig_visitas
        st.session_state.visitas = visitas
        st.session_state.fig_temp = fig_temp
        st.session_state.fig_hum = fig_hum
        st.session_state.fig_lum = fig_lum
        st.session_state.promedios = promedios
    else:
        uso_salon = st.session_state.uso_salon
        uso_diario = st.session_state.uso_diario
        fig_visitas = st.session_state.fig_visitas
        visitas = st.session_state.visitas
        fig_temp = st.session_state.fig_temp
        fig_hum = st.session_state.fig_hum
        fig_lum = st.session_state.fig_lum
        promedios = st.session_state.promedios

    col1, col2 = st.columns(2)
    if uso_diario is not None:
        with col1:
            st.plotly_chart(uso_salon, use_container_width=True)
        with col2:
            st.plotly_chart(uso_diario, use_container_width=True)

    st.markdown("## Número de Visitas")
    col1, col2 = st.columns(2)
    if fig_visitas is not None or not visitas.empty:
        with col1:
            st.plotly_chart(fig_visitas, use_container_width=True)
        with col2:
            st.table(visitas)
    else: 
        st.warning("No hay datos para los parámetros")

    st.markdown("----")
    st.markdown("## Condiciones Salón")
    col1, col2 = st.columns(2)
    col11, col12 = st.columns(2)
    if fig_temp is not None or fig_hum is not None or fig_lum is not None or not promedios.empty:
        with col1:
            st.plotly_chart(fig_temp, use_container_width=True)
        with col2:
            st.plotly_chart(fig_hum, use_container_width=True)
        with col11:
            st.plotly_chart(fig_lum, use_container_width=True)
        with col12:
            st.table(promedios)
    else: 
        st.warning("No hay datos para los parámetros")

############################## Itinerario de profesores ##############################
with tab2:
    st.markdown("## Información profesores")
    profesores = pr.obtener_profesores()
    profesor_seleccionado = st.selectbox("Selecciona un profesor", profesores['nombre'].unique())

    preferencias = pr.obtener_preferencias(profesor_seleccionado)
    profesor_it, numero_visitas = pr.profesor_itinerario(profesor_seleccionado, fecha_inicio, fecha_fin)

    col1, col2 = st.columns(2)
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
            nueva_temperatura = st.number_input("Nueva Temperatura (ºC)", min_value=0.0, max_value=50.0, value=preferencias.at[0, 'temperatura'])
            nueva_humedad = st.number_input("Nueva Humedad (%)", min_value=0.0, max_value=100.0, value=preferencias.at[0, 'humedad'])
            nueva_luminosidad = st.number_input("Nueva Luminosidad (lx)", min_value=0.0, max_value=10000.0, value=preferencias.at[0, 'luminosidad'])
            submit_button = st.form_submit_button(label="Actualizar Preferencias")
            if submit_button:
                pr.cambiar_preferencias(nueva_temperatura, nueva_humedad, nueva_luminosidad, profesor_seleccionado)
                st.success("Preferencias atmosféricas actualizadas exitosamente.")
                time.sleep(5)
                st.rerun()

        default_button = st.button(label="Valores Default", use_container_width=True)
        if default_button:
            pr.cambiar_preferencias("22.00", "50.00", "300.00", profesor_seleccionado)
            st.success("Preferencias atmosféricas actualizadas a default")
            time.sleep(5)
            st.rerun()

    st.markdown("### Itinerario")
    if not profesor_it.empty:
        st.table(profesor_it)
    else:
        st.warning("No hay datos del profesor para el tiempo referido")

############################## Creación Reportes ##############################
with tab3:
    st.markdown("## Generación de reportes")

    col1, col2 = st.columns([1, 3])
    with col1:
        rango_reporte = st.selectbox(
            "Selecciona un rango",
            ("30 Dias", "90 Dias", "180 Dias")
        )

    if st.button("Generar Reporte"):
        st.session_state.generando_reporte = True
        with st.spinner(f"Generando el reporte para: {rango_reporte}..."):
            rp.limpiarcarpetas()
            nombreParcial = rango_reporte.replace(" ", "")
            start_date = rp.transformar_fechas(rango_reporte)
            texto1, texto2, texto3 = rp.graficos_reporte(start_date, datetime.today(), nombreParcial)
            tex_img = f"{texto1}\n{texto3}\n{texto2}"
            tex_path = rp.crear_tex(
                rango_reporte,
                nombreParcial,
                start_date.strftime("%d-%m-%Y"),
                datetime.today().strftime("%d-%m-%Y"),
                tex_img
            )
            rp.compilar_tex(tex_path)
        st.success(f"Reporte generado para los últimos {rango_reporte}... ✅")
        st.session_state.generando_reporte = False