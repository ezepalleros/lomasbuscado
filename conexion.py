import mysql.connector

def obtener_conexion():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Cambia si usas otro usuario
        password="",  # Cambia si tienes contraseña
        database="juego_tkinter"
    )

def guardar_jugador(nombre, puntaje):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO jugadores (nombre, puntaje) VALUES (%s, %s)", (nombre, puntaje))
    conexion.commit()
    conexion.close()

def obtener_top_jugadores():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT nombre, puntaje FROM jugadores ORDER BY puntaje DESC LIMIT 3")
    resultados = cursor.fetchall()
    conexion.close()
    return resultados
