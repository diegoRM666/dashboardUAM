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
visitas = bdc.consultar(
        f"SELECT DATE(v.visita_entrada) AS fecha, count(*) AS visitas "
        f"FROM visita v INNER JOIN salon s ON v.idsalon = s.idsalon "
        f"WHERE v.visita_entrada >= '{start_date}' "
        f"AND v.visita_entrada < '{end_date}' "
        f"AND s.salon = '{salon}' "
        f"AND s.edificio = '{edificio}' "
        f"GROUP BY fecha;"
        )

# Mostrar el DataFrame en Streamlit
if isinstance(visitas, pd.DataFrame) and not visitas.empty:
    # Graficación
    fig_pol1 = go.Figure()

    fig_pol1.add_trace(go.Scatter(
        x=visitas['fecha'], 
        y=visitas['visitas'],
        mode='lines+markers',  # Modo "líneas y puntos"
        name='Cantidad Queries',
    ))

    fig_pol1.update_layout(
                title="Visitas en Salón",
                xaxis_title="Fecha",
                yaxis_title="Cantidad de Visitas",
                paper_bgcolor='rgba(0, 0, 0, 0)',  # Fondo transparente
                plot_bgcolor='rgba(0, 0, 0, 0)',    # Fondo de la cuadrícula transparente
                xaxis = dict(gridcolor ='grey'),
                yaxis = dict(gridcolor ='grey')
            )
    

    graName1 = f"VS{salon}-{rango}-{datetime.today().strftime("%d-%m-%Y")}.png" 
    fig_pol1.write_image(f"../img/poli/{graName1}")

    



