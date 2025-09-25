import bd as bdc
import graficas as graph
import subprocess
import pandas as pd
from datetime import datetime, timedelta
import os
import shutil

#Librerias para latex
from pylatex import Document, Section, Subsection, Command, Figure
from pylatex.utils import NoEscape


# Funcion para obtener las fechas bien
def transformar_fechas(time_range):
    end_date = datetime.today()

    if time_range == "30 Dias":
        start_date = end_date - timedelta(days=30)
    elif time_range == "90 Dias":
        start_date = end_date - timedelta(days=90)
    elif time_range == "180 Dias": 
        start_date = end_date - timedelta(days=180)
    else:
        start_date = end_date - timedelta(days=time_range)
    
    return start_date


# Función general para la extracción de salones y edificios y ejecutar un script
def generar_grafico(start_date, end_date, time_range, script_name, salon_edificio):
    # Iterar sobre los resultados y ejecutar el script con los parámetros correspondientes
    texto = ""

    if not salon_edificio.empty:
        for _, row in salon_edificio.iterrows():
            salon, edificio = row["salon"], row["edificio"]
            subprocess.run(["python3", script_name, f"{salon}", f"{edificio}", f"{start_date}", f"{end_date}", f"{time_range}"])
            # Aqui podriamos hacer la escritura de las imagenes. 
            if script_name == "graP.py":
                texto = texto + "\n"+ insercion_graP(salon, edificio, time_range)
            elif script_name == "graLv.py":
                texto = texto + "\n"+ insercion_graLv(salon, edificio, time_range)
            elif script_name == "graLc.py":
                texto = texto + "\n"+ insercion_graLc(salon, edificio, time_range)

    return texto

# Generación de todos los gráficos
def graficos_reporte(start_date,end_date, time_range):
    salon_edificio = bdc.consultar(
        f"SELECT DISTINCT s.salon as salon, s.edificio as edificio "
        f"FROM sensor.salon s "
        f"INNER JOIN sensor.visita v ON s.idsalon = v.idsalon "
        f"WHERE v.visita_entrada >= '{start_date}' AND v.visita_entrada < '{end_date}';"
    )

    salon_edificio2 = bdc.consultar(
        f"SELECT DISTINCT s.salon as salon, s.edificio as edificio "
        f"FROM salon s "
        f"INNER JOIN condicion c ON s.idsalon = c.idsalon "
        f"WHERE c.time_condicion >= '{start_date}' AND c.time_condicion < '{end_date}';"
    )

    texto1 = generar_grafico(start_date, end_date, time_range, "graP.py", salon_edificio)
    texto2 = generar_grafico(start_date, end_date, time_range, "graLv.py", salon_edificio)
    texto3 = generar_grafico(start_date, end_date, time_range, "graLc.py", salon_edificio2)

    return texto1, texto2, texto3


# Funcione de Limpieza
def limpiar_y_recrear(carpeta):
    if os.path.exists(carpeta):
        shutil.rmtree(carpeta)  # Elimina la carpeta y todo su contenido
    os.makedirs(carpeta)  # Recrea la carpeta vacía

def limpiarcarpetas():
    limpiar_y_recrear("../img/poli")
    limpiar_y_recrear("../img/pie")
    limpiar_y_recrear("../img/tables")
    limpiar_y_recrear("../report")


# Generar el PDF
def crear_tex(rango_reporte, rango, start_date, end_date, texImg):
    # Contenido del archivo LaTeX
    tex_content = r"""
    \documentclass{article}
    \usepackage[utf8]{inputenc}
    \usepackage{graphicx}
    \usepackage{geometry}
    \usepackage{caption}
    \geometry{letterpaper, margin=1in}

    \title{Reporte de sensores de los ultimos """ + rango_reporte + r"""}
    \author{Leonardo Daniel Sánchez Martinez}
    \date{\today}

    \begin{document}

    \maketitle
    Recuperado de """ + start_date + r""" a """ + end_date + texImg +r"""

    \end{document}
    """


    filename = f"reporte-{rango}-{datetime.today().strftime("%d-%m-%Y")}.tex"
    tex_path = os.path.join("../report/", filename)
    with open(tex_path, 'w') as tex_file:
        tex_file.write(tex_content)
    
    print(f"Archivo .tex creado en {tex_path}")
    return tex_path

def insercion_graP(salon, edificio, rango):
    image1_path = f"../img/pie/UP{salon}-{rango}-{datetime.today().strftime("%d-%m-%Y")}.png" 
    image2_path = f"../img/pie/UD{salon}-{rango}-{datetime.today().strftime("%d-%m-%Y")}.png" 

    texto_imagen = r"""
    \section{""" + edificio +r""", Salon: """+ salon +r"""}
    \noindent
    \begin{minipage}{0.48\textwidth}
        \centering
        \includegraphics[width=\textwidth]{""" + image1_path + r"""}
        \captionof{figure}{Tiempo de Uso por Profesor}
    \end{minipage}
    \hfill
    \begin{minipage}{0.48\textwidth}
        \centering
        \includegraphics[width=\textwidth]{""" + image2_path + r"""}
        \captionof{figure}{Tiempo de Uso por Dia}
    \end{minipage}
    """
    return texto_imagen

def insercion_graLv(salon, edificio, rango):
    image1_path = f"../img/poli/VS{salon}-{rango}-{datetime.today().strftime("%d-%m-%Y")}.png" 

    texto_imagen = r"""
    \section{""" + edificio + r""", Salon: """ + salon + r"""}
    \noindent
    \begin{minipage}{0.48\textwidth}
        \centering
        \includegraphics[width=\textwidth]{""" + image1_path + r"""}
        \captionof{figure}{Visitas por Salon}
    \end{minipage}
    """
    return texto_imagen

def insercion_graLc(salon, edificio, rango):
    image1_path = f"../img/poli/TS{salon}-{rango}-{datetime.today().strftime("%d-%m-%Y")}.png"  
    image2_path = f"../img/poli/HS{salon}-{rango}-{datetime.today().strftime("%d-%m-%Y")}.png"
    image3_path = f"../img/poli/LS{salon}-{rango}-{datetime.today().strftime("%d-%m-%Y")}.png"
    image4_path = f"../img/tables/CAVG{salon}-{rango}-{datetime.today().strftime("%d-%m-%Y")}.png" 

    texto_imagen = r"""
    \section{""" + edificio +r""", Salon: """+ salon +r"""}
    \noindent
    \begin{minipage}{0.48\textwidth}
        \centering
        \includegraphics[width=\textwidth]{""" + image1_path + r"""}
        \captionof{figure}{Temperatura}
    \end{minipage}
    \hfill
    \begin{minipage}{0.48\textwidth}
        \centering
        \includegraphics[width=\textwidth]{""" + image2_path + r"""}
        \captionof{figure}{Humedad}
    \end{minipage}

    \noindent
    \begin{minipage}{0.48\textwidth}
        \centering
        \includegraphics[width=\textwidth]{""" + image3_path + r"""}
        \captionof{figure}{Luminosidad}
    \end{minipage}
    \hfill
    \begin{minipage}{0.48\textwidth}
        \centering
        \includegraphics[width=\textwidth]{""" + image4_path + r"""}
        \captionof{figure}{Promedio de Condiciones}
    \end{minipage}
    """
    return texto_imagen

def compilar_tex(tex_path):
    # Ejecutar pdflatex para compilar el archivo
    output_dir = os.path.dirname(tex_path)
    try:
        subprocess.run(
            ['pdflatex', '-output-directory', output_dir, tex_path],
            check=True
        )
        print(f"Archivo compilado correctamente en {output_dir}")
        return output_dir;
    except subprocess.CalledProcessError as e:
        print(f"Error al compilar el documento: {e}")
        return None