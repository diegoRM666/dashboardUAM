from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
import bd as bdc
import graficas as graph
import subprocess

# Estos son unos diccionarios que me sirven para convertir
meses_nombres = {
        1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
        5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
        9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
    }

nombres_a_numeros = {nombre: numero for numero, nombre in meses_nombres.items()}

# Conversion de mes a nombre de mes
def conv_mes_nombre(meses):
    meses_converted = [meses_nombres[numero] for numero in meses] 
    return meses_converted

# Conversion de nombre de mes a mes
def conv_nombre_mes(meses):
    meses_converted = [nombres_a_numeros[nombre] for nombre in meses]
    return meses_converted

# Extraccion de salones y edificos para ciertos meses: 
def salon_edificio(meses, year):
    for mes in meses:
        salon_edificio = bdc.consultar(
            f"SELECT DISTINCT s.salon as salon,  s.edificio as edificio "
            f"from sensor.salon s inner join sensor.visita v on s.idsalon = v.idsalon "
            f"where month(v.visita_entrada) >= {mes} and month(v.visita_entrada) < {mes+1} "
            f"and year(visita_entrada) = {year}; "
        )
        for _, row in salon_edificio.iterrows():
            start_date = f"{year}-{mes}-01"
            end_date = f"{year}-{mes+1}-01"
            salon, edificio = row["salon"], row["edificio"]

            subprocess.run(["python3", "graP.py", f"{salon}", f"{edificio}", f"{start_date}", f"{end_date}",f"{mes}", f"{year}" ])


# Extraccion de meses disponibles para reporte: 
def meses_dispo(year_select):
    meses = bdc.consultar(
        f"SELECT DISTINCT MONTH(visita_entrada) AS mes FROM sensor.visita "
        f"WHERE YEAR(visita.visita_entrada) = '{year_select}';"
    )
    meses_dispo = meses['mes'].tolist()
    return meses_dispo

# Extraccion de años disponibles para reporte: 
def years_dispo():
    years = bdc.consultar(
        f"SELECT DISTINCT YEAR(visita_entrada) AS years FROM sensor.visita;"
    )
    years_dispo = years['years'].tolist()
    return years_dispo

# Generar el PDF
def generar_pdf(nombre_imagen, mes):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, 750, f"Reporte de .")

    # Incluir gráfico
    pdf.drawImage(nombre_imagen, 100, 400, width=400, height=300)

    # Información adicional
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 380, "Este es un gráfico de ejemplo con datos ficticios.")

    pdf.save()
    buffer.seek(0)
    return buffer

