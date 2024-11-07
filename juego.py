import tkinter as tk
from tkinter import messagebox

# Datos de las preguntas y respuestas
preguntas = {
    "Cultura general": [
        ("¿Cuál sería la octava maravilla del mundo?", [
            ("Las Cataratas del Iguazú", 20000),
            ("La Gran Muralla China", 10000),
            ("La Torre Eiffel", 5000),
            ("El Tah Mahal", 3000),
            ("El Monumental", 1500),
            ("La Bombonera", 1000),
        ]),
        ("Decime un cuento o película infantil en el que haya un hada.", [
            ("La Cenicienta", 50000),
            ("Peter Pan", 25000),
            ("La Bella Durmiente", 15000),
            ("Shrek", 10000),
            ("Pinocho", 5000),
        ]),
        ("¿Qué podés hacer con pan?", [
            ("Sanguche", 100000),
            ("Tostada", 80000),
            ("Pan rallado", 60000),
            ("Budín de pan", 40000),
        ]),
    ],
    "Entretenimiento": [
        ("¿Qué actor argentino es el más conocido?", [
            ("Ricardo Darín", 20000),
            ("Guillermo Francella", 10000),
            ("Adrián Suar", 5000),
            ("Leonardo Sbaraglia", 3000),
            ("Pablo Echarri", 1500),
            ("Juan Minujín", 1000),
        ]),
        ("¿Cuál es la serie de televisión más popular en Argentina?", [
            ("Los Simuladores", 50000),
            ("Casados con hijos", 25000),
            ("El Marginal", 15000),
            ("Violetta", 10000),
            ("Graduados", 5000),
        ]),
        ("¿Qué cantante argentino es el más famoso?", [
            ("Charly García", 100000),
            ("Gustavo Cerati", 80000),
            ("Luis Alberto Spinetta", 60000),
            ("Fito Páez", 40000),
        ]),
    ],
    "Deportes": [
        ("¿Qué deporte NUNCA va a ser parte de los Juegos Olímpicos?", [
            ("Poker", 20000),
            ("Piedra, papel o tijera", 10000),
            ("Quemado", 5000),
            ("Bowling", 3000),
            ("Ruleta rusa", 1500),
            ("Chess-Boxing", 1000),
        ]),
        ("Messi podrá ser el mejor futbolista del mundo, pero nunca tendrá ___", [
            ("Altura/Estatura", 50000),
            ("Tranquilidad", 25000),
            ("Facha", 15000),
            ("Una copa Libertadores", 10000),
            ("La del Diego", 5000),
        ]),
        ("¿Hasta con cuánto tanto del envido cantás la falta?", [
            ("30", 100000),
            ("31", 80000),
            ("27", 60000),
            ("28", 40000),
        ]),
    ],
    "Historia Argentina": [
        ("¿Quién es el presidente más recordado?", [
            ("Juan Domingo Perón", 20000),
            ("Domingo Faustino Sarmiento", 10000),
            ("Hipólito Yrigoyen", 5000),
            ("Raúl Alfonsín", 3000),
            ("Cristina Fernández de Kirchner", 1500),
            ("Nestor Kirchner", 1000),
        ]),
        ("La batalla de ____ fue, es y será la más importante de nuestra historia.", [
            ("Batalla de San Lorenzo", 50000),
            ("Batalla de Maipú", 25000),
            ("Batalla de Tucumán", 15000),
            ("Batalla de Caseros", 10000),
            ("Batalla de Pavón", 5000),
        ]),
        ("¿Qué prócer argentino es más recordado por su lucha por la independencia?", [
            ("José de San Martín", 100000),
            ("Manuel Belgrano", 80000),
            ("Martín Miguel de Güemes", 60000),
            ("Juan Manuel de Rosas", 40000),
        ]),
    ],
}

# Colores para cada categoría
category_colors = {
    "Cultura general": "lightblue",
    "Entretenimiento": "lightgreen",
    "Deportes": "lightcoral",
    "Historia Argentina": "lightgoldenrod",
}

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

        self.etiqueta = tk.Label(ventana, text="Ingrese su nombre y apellido:", font=("Helvetica", 12, "bold"), bg="white")
        self.etiqueta.pack(pady=20)

        self.entrada = tk.Entry(ventana, font=("Helvetica", 12))
        self.entrada.pack(pady=10)

        self.boton_iniciar = tk.Button(ventana, text="Comenzar", font=("Helvetica", 12), command=self.iniciar_sesion)
        self.boton_iniciar.pack(pady=20)

    def iniciar_sesion(self):
        self.usuario = self.entrada.get()
        if self.usuario:
            self.mostrar_categorias()
        else:
            messagebox.showwarning("Advertencia", "Por favor ingrese un nombre.")

    def mostrar_categorias(self):
        self.limpiar_ventana()
        self.etiqueta = tk.Label(self.ventana, text="Elija una categoría:", font=("Helvetica", 14, "bold"), bg="white")
        self.etiqueta.pack(pady=20)

        for categoria, color in category_colors.items():
            boton = tk.Button(self.ventana, text=categoria, font=("Helvetica", 12), bg=color,
                              command=lambda c=categoria: self.iniciar_juego(c))
            boton.pack(pady=10)

    def iniciar_juego(self, categoria):
        self.limpiar_ventana()
        self.pregunta_actual = 0
        self.categoria = categoria
        self.color_categoria = category_colors[categoria]
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
