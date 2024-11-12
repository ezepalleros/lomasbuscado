import tkinter as tk
from tkinter import messagebox

class Login:
    def __init__(self, ventana, callback_iniciar_juego):
        self.ventana = ventana
        self.callback_iniciar_juego = callback_iniciar_juego

        # Configuración visual del login
        self.etiqueta = tk.Label(ventana, text="Ingrese su nombre y apellido:", font=("Helvetica", 12, "bold"), bg="white")
        self.etiqueta.pack(pady=20)

        self.entrada = tk.Entry(ventana, font=("Helvetica", 12))
        self.entrada.pack(pady=10)

        self.boton_iniciar = tk.Button(ventana, text="Comenzar", font=("Helvetica", 12), command=self.iniciar_sesion)
        self.boton_iniciar.pack(pady=20)

    def iniciar_sesion(self):
        usuario = self.entrada.get()
        if usuario:
            self.callback_iniciar_juego(usuario)
        else:
            messagebox.showwarning("Advertencia", "Por favor ingrese un nombre.")

    def limpiar(self):
        self.etiqueta.pack_forget()
        self.entrada.pack_forget()
        self.boton_iniciar.pack_forget()
