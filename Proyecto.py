import sympy as sp
from sympy import symbols
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math

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
    def L_algebraicos(x, c):
        x, c = symbols('x c')




app = App()
app.mainloop()