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



    def calcular_limite_trig(self):
        import math # Módulo estándar de Python, no requiere instalación
        
        x = sp.Symbol('x')
        func_str = self.entry_trig_funcion.get()
        c_str = self.entry_trig_c.get()

        try:
            f = sp.sympify(func_str)
            c = sp.sympify(c_str)

            # ==========================================
            # 1. CÁLCULO NUMÉRICO DEL LÍMITE
            # ==========================================
            limite_texto = ""
            
            if c == sp.oo:
                valor = f.subs(x, 1000000).evalf()
                limite_texto = str(round(valor, 4))
            elif c == -sp.oo:
                valor = f.subs(x, -1000000).evalf()
                limite_texto = str(round(valor, 4))
            else:
                epsilon = 1e-6
                limite_izq = f.subs(x, c - epsilon).evalf()
                limite_der = f.subs(x, c + epsilon).evalf()
                
                if abs(limite_izq - limite_der) < 1e-3:
                    limite_promedio = (limite_izq + limite_der) / 2
                    limite_texto = str(round(limite_promedio, 4))
                else:
                    limite_texto = f"Diverge (Izq: {round(limite_izq, 4)}, Der: {round(limite_der, 4)})"

            self.resultado_trig.delete("1.0", "end")
            self.resultado_trig.insert("1.0", f"Función: {f}\nLímite aproximado (x -> {c}):\nResultado = {limite_texto}")

            # ==========================================
            # 2. LÓGICA DE GRAFICACIÓN (PYTHON PURO)
            # ==========================================
            self.ax_trig.clear()
            
            # Definir el inicio y fin del gráfico
            if c == sp.oo: 
                inicio, fin = 1, 50
            elif c == -sp.oo: 
                inicio, fin = -50, -1
            else:
                c_val = float(c.evalf())
                inicio, fin = c_val - 5, c_val + 5

            # Reemplazo de np.linspace: Creamos 200 puntos equiespaciados manualmente
            num_puntos = 200
            paso = (fin - inicio) / (num_puntos - 1)
            x_vals = [inicio + i * paso for i in range(num_puntos)]

            # Convertimos la función para que use el módulo 'math' de Python
            f_numerica = sp.lambdify(x, f, modules=['math'])
            y_vals = []
            
            # Evaluamos la función punto por punto
            for val in x_vals:
                try:
                    # Intentamos calcular el valor de y
                    y = f_numerica(val)
                    y_vals.append(y)
                except:
                    # Si hay error (ej. división por cero en x=0 para sin(x)/x)
                    # Agregamos 'nan' (Not a Number) para que matplotlib corte la línea ahí
                    y_vals.append(float('nan'))

            # Matplotlib acepta listas normales de Python sin problemas
            self.ax_trig.plot(x_vals, y_vals, label="f(x)", color="cyan")
            
            # Línea vertical en el punto a evaluar
            if c != sp.oo and c != -sp.oo:
                self.ax_trig.axvline(x=c_val, color="red", linestyle="--", alpha=0.6, label=f"x = {c}")

            self.ax_trig.legend()
            self.ax_trig.grid(True, linestyle=":", alpha=0.7)
            self.canvas_trig.draw()

        except Exception as e:
            self.resultado_trig.delete("1.0", "end")
            self.resultado_trig.insert("1.0", f"Error en la expresión:\n{e}")






app = App()
app.mainloop()