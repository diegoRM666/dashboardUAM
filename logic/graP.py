import plotly.graph_objects as go
import sys
import bd as bdc
import pandas as pd
from datetime import datetime, timedelta

salon = sys.argv[1]
edificio = sys.argv[2]
start_date = sys.argv[3]
end_date = sys.argv[4]
rango = sys.argv[5]


# Consulta para obtener los datos en un DataFrame
ocupacion_salon = bdc.consultar(
    f"SELECT s.edificio AS edificio, s.salon AS salon, v.visita_entrada AS entrada, "
    f"v.visita_salida AS salida, p.nombre AS profesor "
    f"FROM salon s "
    f"INNER JOIN visita v ON s.idsalon = v.idsalon "
    f"INNER JOIN profesor p ON v.idprofesor = p.idprofesor "
    f"WHERE s.salon = {salon} AND s.edificio = '{edificio}' "
    f"AND v.visita_entrada >= '{start_date}' "
    f"AND v.visita_entrada <= '{end_date}';"
)


# Mostrar el DataFrame en Streamlit
if isinstance(ocupacion_salon, pd.DataFrame) and not ocupacion_salon.empty:
    # Convertir las columnas de tiempo
    ocupacion_salon['entrada'] = pd.to_datetime(ocupacion_salon['entrada'])
    ocupacion_salon['salida'] = pd.to_datetime(ocupacion_salon['salida'])
    
    # Calcular la duración en horas para cada visita
    ocupacion_salon['duracion_horas'] = (ocupacion_salon['salida'] - ocupacion_salon['entrada']).dt.total_seconds() / 3600

    # Agrupar por profesor y sumar la duración total de horas
    duracion_por_profesor = ocupacion_salon.groupby('profesor')['duracion_horas'].sum().reset_index()

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

    # Separar en fecha y hora
    ocupacion_salon['fecha_entrada'] = ocupacion_salon['entrada'].dt.date
    ocupacion_salon['hora_entrada'] = ocupacion_salon['entrada'].dt.time

    duracion_por_dia = ocupacion_salon.groupby('fecha_entrada')['duracion_horas'].sum().reset_index()

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
    

    graName1 = f"UP{salon}-{rango}-{datetime.today().strftime("%d-%m-%Y")}.png" 
    fig_dona.write_image(f"../img/pie/{graName1}")
    graName2 = f"UD{salon}-{rango}-{datetime.today().strftime("%d-%m-%Y")}.png" 
    fig_dona2.write_image(f"../img/pie/{graName2}")
    



