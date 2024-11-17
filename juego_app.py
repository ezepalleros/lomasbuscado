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
        ventana.geometry("500x600")
        ventana.configure(bg="#6e8101")

        
        pygame.mixer.init()
        
        self.img_fondo = Image.open("img/gameboy.jpg")  # Reemplaza con la ruta de tu imagen
        self.img_fondo = self.img_fondo.resize((500, 700), Image.Resampling.LANCZOS)
        self.tk_img_fondo = ImageTk.PhotoImage(self.img_fondo)

        self.label_fondo = tk.Label(self.ventana, image=self.tk_img_fondo)
        self.label_fondo.place(x=0, y=0, relwidth=1, relheight=1)


        # Cargar sonido para respuestas correctas
        self.sonido_correcto = pygame.mixer.Sound("musica/goodresult-82807.mp3")
        self.sonido_incorrecto = pygame.mixer.Sound("musica/boo-36556.mp3")
        self.sonido_todoCorrecto = pygame.mixer.Sound("musica/claps.mp3")
        self.sonido_fondo = pygame.mixer.Sound("musica/gameboy.mp3")

        self.sonido_fondo.play(loops=-1)

      
        
        self.usuario = None
        self.vidas = 3
        self.puntaje = 0
        self.respuestas_correctas = []
        self.imagen_label = None


        # Crear instancia de login
        self.login = Login(ventana, self.iniciar_juego)

        # Crear el frame para puntaje y respuestas
        self.frame_puntaje = tk.Frame(self.ventana, bg="#6e8101")
        self.frame_puntaje.place(relx=0.5, rely=0.97, anchor="center")

        # La etiqueta de puntaje estará dentro del frame_puntaje
        self.etiqueta_puntaje = tk.Label(self.frame_puntaje, text=f"Puntaje: {self.puntaje}", font=("Helvetica", 14, "bold"), bg="#6e8101")
        self.etiqueta_puntaje.pack(side=tk.LEFT, padx=5)



    def iniciar_juego(self, usuario):
        self.usuario = usuario
        self.login.limpiar()
        self.mostrar_categorias()

    def mostrar_categorias(self):
        self.limpiar_ventana()
        self.etiqueta = tk.Label(self.ventana, text="Elija una categoría:", font=("Helvetica", 14, "bold"), bg="#6e8101")
        self.etiqueta.pack(pady=5)

        for categoria, color in colores_categoria.items():
            boton = tk.Button(self.ventana, text=categoria, font=("Helvetica", 12), bg=color,
                              command=lambda c=categoria: self.iniciar_categoria(c))
            boton.pack(pady=5)

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
            self.etiqueta = tk.Label(self.ventana, text=pregunta, font=("Helvetica", 10), bg="#6e8101")
            self.etiqueta.pack(pady=5)

            image_name = f"{self.categoria}_{self.pregunta_actual + 1}.png"
            image_path = f"img/{image_name}"

            try:
                img = Image.open(image_path)
                img = img.resize((200, 100), Image.Resampling.LANCZOS)
                img_tk = ImageTk.PhotoImage(img)

                if self.imagen_label is None:
                    self.imagen_label = tk.Label(self.ventana, image=img_tk, bg="#6e8101")
                    self.imagen_label.image = img_tk
                    self.imagen_label.pack(pady=10)
                else:
                    self.imagen_label.config(image=img_tk)
                    self.imagen_label.image = img_tk
            except FileNotFoundError:
                pass  

            self.entrada_respuesta = tk.Entry(self.ventana, font=("Helvetica", 10))
            self.entrada_respuesta.pack(pady=10)
            self.boton_enviar = tk.Button(self.ventana, text="Responder", font=("Helvetica", 10),
                                          command=self.verificar_respuesta)
            self.boton_enviar.pack(pady=10)
            self.respuestas_frame = tk.Frame(self.ventana, bg="#6e8101")
            self.respuestas_frame.pack()

            self.etiquetas_respuestas = []
            for i in range(len(opciones)):
                etiqueta = tk.Label(self.respuestas_frame, text="", font=("Helvetica", 10),
                                    bg="#6e8101", fg="black", width=25, height=2,
                                    relief="solid", borderwidth=2)
                etiqueta.config(highlightbackground=self.color_categoria, highlightthickness=2)
                etiqueta.grid(row=i // 2, column=i % 2, padx=5, pady=5)
                self.etiquetas_respuestas.append(etiqueta)

            self.etiqueta_puntaje.config(text=f"Puntaje: {self.puntaje}")  
            self.etiqueta_puntaje.pack(side=tk.LEFT, padx=5)
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
                pygame.mixer.Sound.play(self.sonido_todoCorrecto)
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

        self.etiqueta = tk.Label(self.ventana, text=f"Fin del juego, {self.usuario}. Puntaje final: {self.puntaje}",
                                 font=("Helvetica", 14, "bold"), bg="#6e8101")
        self.etiqueta.pack(pady=20)

        guardar_jugador(self.usuario, self.puntaje)
        jugadores_top = obtener_top_jugadores()

        if jugadores_top:
            encabezado = tk.Label(self.ventana, text="Top Jugadores:", font=("Helvetica", 12, "bold"), bg="#6e8101")
            encabezado.pack(pady=10)

            for idx, (nombre, puntaje) in enumerate(jugadores_top, start=1):
                texto = f"{idx}. {nombre} - {puntaje} puntos"
                etiqueta = tk.Label(self.ventana, text=texto, font=("Helvetica", 12), bg="#6e8101")
                etiqueta.pack(pady=5)
        else:
            etiqueta = tk.Label(self.ventana, text="No hay jugadores registrados aún.",
                                font=("Helvetica", 12), bg="#6e8101")
            etiqueta.pack(pady=5)

        
        self.boton_jugar_de_nuevo = tk.Button(self.ventana, text="Jugar de nuevo", font=("Helvetica", 12),
                                command=self.mostrar_categorias)
        self.boton_jugar_de_nuevo.pack(pady=5)

    def mostrar_tabla_clasificaciones(self):
        self.limpiar_ventana()
        encabezado = tk.Label(self.ventana, text="Tabla de Clasificaciones", font=("Helvetica", 14, "bold"), bg="#6e8101")
        encabezado.pack(pady=20)

        jugadores_top = obtener_top_jugadores()

        if jugadores_top:
            for idx, (nombre, puntaje) in enumerate(jugadores_top, start=1):
                texto = f"{idx}. {nombre} - {puntaje} puntos"
                etiqueta = tk.Label(self.ventana, text=texto, font=("Helvetica", 12), bg="#6e8101")
                etiqueta.pack(pady=5)
        else:
            etiqueta = tk.Label(self.ventana, text="No hay jugadores registrados aún.", font=("Helvetica", 12),
                                bg="#6e8101")
            etiqueta.pack(pady=5)

        
        boton_volver = tk.Button(self.ventana, text="Volver al juego", font=("Helvetica", 12),
                                 command=self.mostrar_categorias)
        boton_volver.pack(pady=20)

    def mostrar_categorias(self):
        self.limpiar_ventana()
        self.etiqueta = tk.Label(self.ventana, text="Elija una categoría:", font=("Helvetica", 14, "bold"), bg="#6e8101")
        self.etiqueta.pack(pady=8)

        for categoria, color in colores_categoria.items():
            boton = tk.Button(self.ventana, text=categoria, font=("Helvetica", 12), bg=color,
                              command=lambda c=categoria: self.iniciar_categoria(c))
            boton.pack(pady=8)

        
        boton_tabla = tk.Button(self.ventana, text="Tabla de Clasificaciones", font=("Helvetica", 12), bg="lightblue",
                                command=self.mostrar_tabla_clasificaciones)
        boton_tabla.pack(pady=8)

    def limpiar_ventana(self):
        for widget in self.ventana.winfo_children():
            if widget not in [self.label_fondo, self.frame_puntaje, self.imagen_label]:
                widget.destroy()
    
