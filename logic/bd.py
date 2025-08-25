import pandas as pd
from sqlalchemy import create_engine
import platform
from sqlalchemy.sql import text

# Generar la conexión a la base de datos
def conectarBase():
    """Establece la conexión a la base de datos y la devuelve usando SQLAlchemy."""
    s_o = platform.system()
    try:
        if s_o == "Darwin":
            password = 'admin'
        else:
            password = 'gogo219715122121B$'
        
        # Crear la URL de conexión de SQLAlchemy
        db_url = f"mysql+pymysql://root:{password}@localhost/sensor"
        
        # Crear el motor de conexión con SQLAlchemy
        engine = create_engine(db_url)

        # Conectar al motor (esto también verifica si la conexión es válida)
        connection = engine.connect()
        
        #print("Conectado a la base de datos MySQL con SQLAlchemy.")
        return connection

    except Exception as e:
        print("Error al conectar a MySQL:", e)
        return None

# Ejecutar una actualización
def actualizar(query):
    """Actualiza una o varias tablas en la base de datos y devuelve un mensaje de éxito o error."""
    connection = conectarBase()
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return "No se pudo establecer la conexión a la base de datos."
    
    try:
        # Ejecuta la consulta de actualización
        with connection.begin():  # Asegura una transacción
            connection.execute(text(query))  # Envolver en 'text'
        msj = "Actualización exitosa."
        return msj

    except Exception as e:
        print("Error al ejecutar la actualización:", e)
        msj = f"Error al ejecutar la actualización: {e}"
        return msj

    finally:
        # Cierra la conexión si fue establecida
        cerrarConexion(connection)


# Hacer una consulta de datos
def consultar(query, msj="naranjas"):
    """Ejecuta una consulta en la base de datos y devuelve los resultados en un DataFrame."""
    connection = conectarBase()
    if connection is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return "No se pudo establecer la conexión a la base de datos."

    try:
        # Ejecutar la consulta y obtener los resultados en un DataFrame usando pandas y SQLAlchemy
        df = pd.read_sql(query, connection)
        print(msj)
        return df

    except Exception as e:
        print("Error al ejecutar la consulta:", e)
        msj = f"Error al ejecutar la consulta: {e}"
        return msj

    finally:
        # Cerrar la conexión
        cerrarConexion(connection)

# Cerrar la conexión de BD
def cerrarConexion(connection):
    """Cierra la conexión a la base de datos."""
    if connection is not None:
        connection.close()
        #print("Conexión cerrada")
