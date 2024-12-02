import bd as bdc
import graficas as graph
import subprocess
from datetime import datetime, timedelta
import os
import shutil


# Funcion para obtener las fechas bien
def transformar_fechas(time_range):
    end_date = datetime.today()

    if time_range == "1 Mes":
        start_date = end_date - timedelta(days=30)
    elif time_range == "3 Meses":
        start_date = end_date - timedelta(days=90)
    elif time_range == "6 Meses": 
        start_date = end_date - timedelta(days=180)
    
    return start_date

# Función general para la extracción de salones y edificios y ejecutar un script
def generar_grafico(start_date, end_date, time_range, script_name):
    # Consulta SQL para obtener los salones y edificios
    salon_edificio = bdc.consultar(
        f"SELECT DISTINCT s.salon as salon, s.edificio as edificio "
        f"FROM sensor.salon s "
        f"INNER JOIN sensor.visita v ON s.idsalon = v.idsalon "
        f"WHERE v.visita_entrada >= '{start_date}' AND v.visita_entrada < '{end_date}';"
    )
    
    # Iterar sobre los resultados y ejecutar el script con los parámetros correspondientes
    for _, row in salon_edificio.iterrows():
        salon, edificio = row["salon"], row["edificio"]
        subprocess.run(["python3", script_name, f"{salon}", f"{edificio}", f"{start_date}", f"{end_date}", f"{time_range}"])

# Generación de todos los gráficos
def graficos_reporte(start_date,end_date, time_range):
    generar_grafico(start_date, end_date, time_range, "graP.py")
    generar_grafico(start_date, end_date, time_range, "graLv.py")
    generar_grafico(start_date, end_date, time_range, "graLc.py")

def limpiar_y_recrear(carpeta):
    if os.path.exists(carpeta):
        shutil.rmtree(carpeta)  # Elimina la carpeta y todo su contenido
    os.makedirs(carpeta)  # Recrea la carpeta vacía

def limpiarcarpetas():
    limpiar_y_recrear("../img/poli")
    limpiar_y_recrear("../img/pie")
    limpiar_y_recrear("../img/tables")

# Generar el PDF
def generar_pdf(rango):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, 750, f"Reporte de {rango}.")
    pdf.drawString()

    # Incluir gráfico
    #pdf.drawImage(nombre_imagen, 100, 400, width=400, height=300)

    # Información adicional
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 380, "Este es un gráfico de ejemplo con datos ficticios.")

    pdf.save()
    buffer.seek(0)
    return buffer

