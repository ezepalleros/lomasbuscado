import tkinter as tk
from tkinter import messagebox
from conexion import obtener_top_jugadores

class Login:
    def __init__(self, ventana, callback_iniciar_juego):
        self.ventana = ventana
        self.callback_iniciar_juego = callback_iniciar_juego

        # Configuración visual del login
        self.etiqueta = tk.Label(ventana, text="Ingrese su nombre y apellido:", font=("Helvetica", 12, "bold"))
        self.etiqueta.pack(pady=20)

        self.entrada = tk.Entry(ventana, font=("Helvetica", 12))
        self.entrada.pack(pady=10)

        self.boton_iniciar = tk.Button(ventana, text="Comenzar", font=("Helvetica", 12), command=self.iniciar_sesion, width=0, height=0)
        self.boton_iniciar.pack(pady=5)

        # Mostrar el Top 3 de jugadores al inicio
        self.mostrar_top_3()

    def iniciar_sesion(self):
        usuario = self.entrada.get()
        if usuario:
            self.callback_iniciar_juego(usuario)
        else:
            messagebox.showwarning("Advertencia", "Por favor ingrese un nombre.")

    def mostrar_top_3(self):
        # Mostrar un encabezado para el Top 3
        tk.Label(self.ventana, text="Top 3 jugadores:", font=("Helvetica", 12, "bold")).pack(pady=10)

        # Obtener el Top 3 desde la base de datos
        top_jugadores = obtener_top_jugadores()
        if top_jugadores:
            for idx, (nombre, puntaje) in enumerate(top_jugadores, start=1):
                tk.Label(self.ventana, text=f"{idx}. {nombre} - {puntaje} puntos",
                         font=("Helvetica", 12)).pack(pady=5)
        else:
            tk.Label(self.ventana, text="No hay jugadores registrados aún.",
                     font=("Helvetica", 12)).pack(pady=5)

    def limpiar(self):
        self.etiqueta.pack_forget()
        self.entrada.pack_forget()
        self.boton_iniciar.pack_forget()
        
