import tkinter as tk
from tkinter import messagebox
from data import preguntas, colores_categoria
from login import Login

class JuegoApp:
    def __init__(self, ventana):
        self.ventana = ventana
        ventana.title("Lo + Buscado")
        ventana.geometry("600x600")
        ventana.configure(bg="white")

        self.usuario = None
        self.vidas = 3
        self.puntaje = 0
        self.respuestas_correctas = []

        # Crear instancia de login
        self.login = Login(ventana, self.iniciar_juego)

    def iniciar_juego(self, usuario):
        self.usuario = usuario
        self.login.limpiar()  # Ocultar el login una vez que el usuario ha ingresado
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
        self.limpiar_ventana()
        self.pregunta_actual = 0
        self.categoria = categoria
        self.color_categoria = colores_categoria[categoria]
        self.hacer_pregunta()

    def hacer_pregunta(self):
        if self.pregunta_actual < len(preguntas[self.categoria]):
            pregunta, opciones = preguntas[self.categoria][self.pregunta_actual]
            self.limpiar_ventana()
            self.respuestas_correctas = []
            self.vidas = 3
            self.etiqueta = tk.Label(self.ventana, text=pregunta, font=("Helvetica", 12), bg="white")
            self.etiqueta.pack(pady=20)

            # Cuadro de entrada en la parte superior
            self.entrada_respuesta = tk.Entry(self.ventana, font=("Helvetica", 12))
            self.entrada_respuesta.pack(pady=10)

            self.boton_enviar = tk.Button(self.ventana, text="Responder", font=("Helvetica", 12),
                                          command=self.verificar_respuesta)
            self.boton_enviar.pack(pady=10)

            # Diseño en cuadrícula para las respuestas con color de borde según la categoría
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
        else:
            self.finalizar_juego()

    def verificar_respuesta(self):
        respuesta = self.entrada_respuesta.get().strip()
        pregunta, opciones = preguntas[self.categoria][self.pregunta_actual]

        correcta = False
        for idx, (texto_respuesta, puntos) in enumerate(opciones):
            if respuesta.lower() == texto_respuesta.lower() and texto_respuesta not in self.respuestas_correctas:
                self.etiquetas_respuestas[idx].config(text=f"{idx + 1}- {texto_respuesta} ({puntos} puntos)")
                self.puntaje += puntos
                self.respuestas_correctas.append(texto_respuesta)
                correcta = True
                break

        if correcta:
            self.entrada_respuesta.delete(0, tk.END)
            messagebox.showinfo("Respuesta Correcta", "¡Respuesta correcta!")
            if len(self.respuestas_correctas) == len(opciones):
                messagebox.showinfo("Pregunta Completada", "¡Has respondido todas las respuestas correctamente!")
                self.pregunta_actual += 1
                self.hacer_pregunta()
        else:
            self.vidas -= 1
            messagebox.showerror("Respuesta Incorrecta", f"Incorrecto. Te quedan {self.vidas} vidas.")
            if self.vidas == 0:
                self.pregunta_actual += 1
                self.hacer_pregunta()

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
            widget.destroy()

