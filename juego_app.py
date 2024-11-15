import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk 
import os
from data import preguntas, colores_categoria
from login import Login
from conexion import guardar_jugador, obtener_top_jugadores
import pygame


class JuegoApp:
    def __init__(self, ventana):
        self.ventana = ventana
        ventana.title("Lo + Buscado")
        ventana.geometry("600x600")
        ventana.configure(bg="white")

     
        pygame.mixer.init()

       
        # Cargar sonido para respuestas correctas
        self.sonido_correcto = pygame.mixer.Sound("musica/goodresult-82807.mp3")
        self.sonido_incorrecto = pygame.mixer.Sound("musica/boo-36556.mp3")
        self.sonido_fondo = pygame.mixer.Sound("musica/suspense-cinematic-248035.mp3")
        
       
        pygame.mixer.Sound.play(self.sonido_fondo)
       
        self.usuario = None
        self.vidas = 3
        self.puntaje = 0
        self.respuestas_correctas = []
        self.imagen_label = None
        
        
        # Crear instancia de login
        self.login = Login(ventana, self.iniciar_juego)

        # Crear el frame para puntaje y respuestas
        self.frame_puntaje = tk.Frame(self.ventana, bg="white")
        self.frame_puntaje.place(relx=0.5, rely=0.95, anchor="center")

        # La etiqueta de puntaje estará dentro del frame_puntaje
        self.etiqueta_puntaje = tk.Label(self.frame_puntaje, text=f"Puntaje: {self.puntaje}", font=("Helvetica", 14, "bold"), bg="white")
        self.etiqueta_puntaje.pack(side=tk.LEFT, padx=10)
       
        
    
    def iniciar_juego(self, usuario):
        self.usuario = usuario
        self.login.limpiar()
        self.mostrar_categorias()

    def mostrar_categorias(self):
        self.limpiar_ventana()
        self.etiqueta = tk.Label(self.ventana, text="Elija una categoría:", font=("Helvetica", 14, "bold"), bg="white")
        self.etiqueta.pack(pady=20)

        for categoria, color in colores_categoria.items():
            boton = tk.Button(self.ventana, text=categoria, font=("Helvetica", 12), bg=color,
                              command=lambda c=categoria: self.iniciar_categoria(c))
            boton.pack(pady=10)

    def iniciar_categoria(self, categoria):
        self.puntaje = 0
        self.respuestas_correctas = []
        self.vidas = 3
        self.pregunta_actual = 0
        self.categoria = categoria
        self.color_categoria = colores_categoria[categoria]

        self.etiqueta_puntaje.config(text=f"Puntaje: {self.puntaje}")

        self.limpiar_ventana()
        self.hacer_pregunta()

    def hacer_pregunta(self):
        if self.pregunta_actual < len(preguntas[self.categoria]):
            pregunta, opciones = preguntas[self.categoria][self.pregunta_actual]
            self.limpiar_ventana()
            self.respuestas_correctas = []
            self.vidas = 3
            self.etiqueta = tk.Label(self.ventana, text=pregunta, font=("Helvetica", 12), bg="white")
            self.etiqueta.pack(pady=20)

            image_name = f"{self.categoria}_{self.pregunta_actual + 1}.png"
            image_path = f"img/{image_name}"

            try:
                img = Image.open(image_path)
                img = img.resize((300, 200), Image.Resampling.LANCZOS)
                img_tk = ImageTk.PhotoImage(img)

                if self.imagen_label is None:
                    self.imagen_label = tk.Label(self.ventana, image=img_tk, bg="white")
                    self.imagen_label.image = img_tk
                    self.imagen_label.pack(pady=10)
                else:
                    self.imagen_label.config(image=img_tk)
                    self.imagen_label.image = img_tk
            except FileNotFoundError:
                pass  # Si no encuentra la imagen, continúa sin mostrarla.

            self.entrada_respuesta = tk.Entry(self.ventana, font=("Helvetica", 12))
            self.entrada_respuesta.pack(pady=10)
            self.boton_enviar = tk.Button(self.ventana, text="Responder", font=("Helvetica", 12),
                                          command=self.verificar_respuesta)
            self.boton_enviar.pack(pady=10)
            self.respuestas_frame = tk.Frame(self.ventana, bg="white")
            self.respuestas_frame.pack()

            self.etiquetas_respuestas = []
            for i in range(len(opciones)):
                etiqueta = tk.Label(self.respuestas_frame, text="", font=("Helvetica", 12),
                                    bg="white", fg="black", width=30, height=2,
                                    relief="solid", borderwidth=2)
                etiqueta.config(highlightbackground=self.color_categoria, highlightthickness=2)
                etiqueta.grid(row=i // 2, column=i % 2, padx=5, pady=5)
                self.etiquetas_respuestas.append(etiqueta)

            self.etiqueta_puntaje.config(text=f"Puntaje: {self.puntaje}")  # Actualizar el puntaje
            self.etiqueta_puntaje.pack(side=tk.LEFT, padx=10)
        else:
            self.finalizar_juego()

    def verificar_respuesta(self):
        respuesta = self.entrada_respuesta.get().strip().lower()
        pregunta, opciones = preguntas[self.categoria][self.pregunta_actual]

        correcta = False
        for idx, (respuestas_correctas, puntos) in enumerate(opciones):
            if isinstance(respuestas_correctas, list):
                if any(respuesta == r.lower() for r in respuestas_correctas) and respuestas_correctas[0] not in self.respuestas_correctas:
                    self.etiquetas_respuestas[idx].config(
                        text=f"{idx + 1}- {respuestas_correctas[0]} ({puntos} puntos)")
                    self.puntaje += puntos
                    self.respuestas_correctas.append(respuestas_correctas[0])
                    correcta = True
                    break
            else:
                if respuesta == respuestas_correctas.lower() and respuestas_correctas not in self.respuestas_correctas:
                    self.etiquetas_respuestas[idx].config(text=f"{idx + 1}- {respuestas_correctas} ({puntos} puntos)")
                    self.puntaje += puntos
                    self.respuestas_correctas.append(respuestas_correctas)
                    correcta = True
                    break

        if correcta:
            self.entrada_respuesta.delete(0, tk.END)
            pygame.mixer.Sound.play(self.sonido_correcto)  
            messagebox.showinfo("Respuesta Correcta", "¡Respuesta correcta!")
            self.actualizar_puntaje()
            if len(self.respuestas_correctas) == len(opciones):
                messagebox.showinfo("Pregunta Completada", "¡Has respondido todas las respuestas correctamente!")
                self.pregunta_actual += 1
                self.hacer_pregunta()
        else:
            self.vidas -= 1
            pygame.mixer.Sound.play(self.sonido_incorrecto)
            messagebox.showerror("Respuesta Incorrecta", f"Incorrecto. Te quedan {self.vidas} vidas.")
            if self.vidas == 0:
                self.pregunta_actual += 1
                self.hacer_pregunta()

    def actualizar_puntaje(self):
        self.etiqueta_puntaje.config(text=f"Puntaje: {self.puntaje}")

    def finalizar_juego(self):
        self.limpiar_ventana()
        self.etiqueta = tk.Label(self.ventana, text=f"Fin del juego. Puntaje final: {self.puntaje}",
                                 font=("Helvetica", 14, "bold"), bg="white")
        self.etiqueta.pack(pady=20)

        self.boton_jugar_de_nuevo = tk.Button(self.ventana, text="Jugar de nuevo", font=("Helvetica", 12),
                                              command=self.mostrar_categorias)
        self.boton_jugar_de_nuevo.pack(pady=20)
    
    def limpiar_ventana(self):
        for widget in self.ventana.winfo_children():
            if widget != self.imagen_label and widget != self.frame_puntaje:  
                widget.destroy()

