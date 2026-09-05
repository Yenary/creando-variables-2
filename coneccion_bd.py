import mysql.connector
from mysql.connector import Error

def obtener_coneccion():
    try:
        conexion= mysql.connector.connect(
            host="localhost",
            database="contador",
            user="root",
            password="root"
        )
        if conexion.is_connected():
            print("conexion exitosa a la base de datos")
            return conexion
        else:
            print("No se pudo establecer una conexion")
            return None
        
    except Error as e:
        print(f"Error al conectar a la base de datos {e}")
        return None     