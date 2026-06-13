import sympy as sp
from sympy import symbols
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math

def calcular_limite_numerico(funcion_str, c_str):
    #Interpretar el valor de 'c' (por si el usuario escribe "pi" o "pi/2")
    try:
        # Usamos sympify para que entienda "pi" y evalf para volverlo decimal
        c_val = float(sp.sympify(c_str).evalf())
    except Exception:
        return "Error: Verifica el valor de x."

    # 2. Definir una distancia 'h' muy pequeña para acercarnos
    h = 0.00001 
    
    #Evaluar por la izquierda (c - h) y por la derecha (c + h)
    lim_izq = evaluar_funcion(funcion_str, c_val - h)
    lim_der = evaluar_funcion(funcion_str, c_val + h)
    
    # 4. Comprobar si hubo errores matemáticos (ej. asíntotas verticales)
    if lim_izq is None or lim_der is None:
        return "El límite diverge o es indefinido"
        
    #Comparar ambos lados. Si la diferencia es muy chiquita, convergen al mismo punto.
    if abs(lim_izq - lim_der) < 0.01:
        # Promediamos ambos lados para mayor precisión y redondeamos a 4 decimales
        limite_final = (lim_izq + lim_der) / 2
        return round(limite_final, 4)
    else:
        # Si por la izquierda da un número y por la derecha otro muy distinto
        return "No existe (límites laterales distintos)"

#Configuración de la ventana
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Título y tamaño de la ventana
        self.geometry("800x600")
        self.title("Analizador de limites")
        
        # Colores de la aplicación
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Adaptación al tamaño de la ventana
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Para la creación de las pestañas
        self.tabs = ctk.CTkTabview(self)
        self.tabs.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Creación de las pestañas
        self.tab_inicio = self.tabs.add("Inicio")
        self.tab_limites_algebraicos = self.tabs.add("Límites algebraicos")
        self.tab_limites_trigonometricos = self.tabs.add("Límites trigonométricos")
        self.tab_limites_infinitos = self.tabs.add("Límites infinitos")

        # Llamar a cada pestaña
        self.crear_inicio()
        #self.crear_limites_algebraicos()
        #self.crear_limites_trigonométricos()
        #self.crear_limites_infinitos()
        
        #-------------------
        # Pestaña de inicio
        #-------------------

    def crear_inicio(self):
        titulo = ctk.CTkLabel(
            self.tab_inicio,
            text = "Pestaña de inicio",
            font = ("Arial", 30, "bold")
            )
        titulo.pack(pady=25)

        texto = """Programa para representar límites y blablabla"""


        caja = ctk.CTkTextbox(self.tab_inicio, width=900, height=350, font=("Arial", 16))
        caja.pack(pady=20)
        caja.insert("1.0", texto)
        caja.configure(state="disabled")

    def crear_canvas(self, frame):
        figura = Figure(figsize=(6, 5), dpi=100)
        eje = figura.add_subplot(111)
        canvas = FigureCanvasTkAgg(figura, master=frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        return figura, eje, canvas
        
        #=====================
        # Limites algebraicos
        #=====================

    def L_algebraicos(self):
        contenedor = ctk.CTkFrame(self.L_algebraicos) 
        contenedor.pack(fill="both", expand=True, padx=10, pady=10)

        panel = ctk.CTkFrame(contenedor, width=340)
        panel.pack(side="left", fill="y", padx=10, pady=10)

        grafico = ctk.CTkFrame(contenedor)
        grafico.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(panel, text="Límite algebraico", font=("Arial", 24, "bold")).pack(pady=15)

        ctk.CTkLabel(panel, text="Función: ").pack()
        entry_funcion = ctk.CTkEntry(app, placeholder_text="Ingrese f(x) ej: (x**2 - 1)/(x - 1)")
        entry_funcion.pack(pady=10)

        ctk.CTkLabel(panel, text="Valor al que tiende x: ").pack()
        entry_h = ctk.CTkEntry(app, placeholder_text="Valor de c (ej: 1 o oo)")
        entry_h.pack(pady=10)

        """#ctk.CTkButton(
            panel, 
            text="Calcular y graficar"
            command=self.graicar_limite
        ).pack(pady=20)"""
        
        self.resulttado_limite = ctk.CTkTextbox(panel, width=310, height=350)
        self.resultado_limite.pack(pady=10)

    #def graficar_limite(self):




app = App()
app.mainloop()