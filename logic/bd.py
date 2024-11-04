import mysql.connector
from mysql.connector import Error
import pandas as pd

# Generar la conexión a la base de datos
def conectarBase():
    """Establece la conexión a la base de datos y la devuelve."""
    try:
        # Crear la conexión
        connection = mysql.connector.connect(
            host='localhost',       # Cambia por la IP o nombre de tu servidor MySQL
            database='sensor',   # Nombre de la base de datos
            user='root',      # Usuario de MySQL
            password='15122121B' # Contraseña de MySQL
        )
        
        if connection.is_connected():
            db_info = connection.get_server_info()
            print("Conectado a MySQL Server versión", db_info)
            return connection

    except Error as e:
        print("Error al conectar a MySQL:", e)
        return None

# Hacer una consulta de datos
# Cada consulta 
def consultar(query):
    """Ejecuta una consulta en la base de datos y devuelve los resultados en un DataFrame."""
    connection = conectarBase()
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return None

    try:
        # Ejecutar la consulta y obtener los resultados en un DataFrame
        df = pd.read_sql(query, connection)
        return df

    except Error as e:
        print("Error al ejecutar la consulta:", e)
        return None

    finally:
        # Cerrar la conexión
        cerrarConexion(connection)


# Cerrar la conexión de BD
def cerrarConexion(connection):
    """Cierra la conexión a la base de datos."""
    if connection is not None and connection.is_connected():
        connection.close()
        print("Conexión cerrada")
