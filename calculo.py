import customtkinter as ctk
import sympy as sp
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math

# ==========================================
# 1. FUNCIÓN PRINCIPAL DE CÁLCULO
# ==========================================
def calcular_limite():
    x = sp.Symbol('x')
    # Obtenemos los textos que el usuario escribió en las cajas
    func_str = entry_funcion.get()
    c_str = entry_c.get()

    try:
        # Convertimos el texto a matemáticas de SymPy
        f = sp.sympify(func_str)
        c = sp.sympify(c_str)

        # Cáculo de Límites
        limite_exacto = ""
        # Evaluamos directamente el punto
        evaluacion_directa = f.subs(x, c)
        
        # Si da error (0/0, división por cero)
        if evaluacion_directa.has(sp.nan) or evaluacion_directa.has(sp.zoo):
            # Factorizamos y simplificamos
            f_simplificada = sp.cancel(f)
            limite_exacto = f_simplificada.subs(x,c)

            # Si después de simplificar sigue dando error:
            if limite_exacto.has(sp.nan) or limite_exacto.has(sp.zoo):
                limite_exacto = "No existe (Diverge)"
        else:
            # Si no hubo error al principio, ese es el límite
            limite_exacto = evaluacion_directa 
        
        # Cálculo numérico por aproximación
        limite_aprox = ""
        if c == sp.oo:
            valor = f.subs(x, 1000000).evalf()
            limite_aprox = str(round(valor, 4))
        elif c == -sp.oo:
            valor = f.subs(x, -1000000).evalf()
            limite_aprox = str(round(valor, 4))
        else:
            epsilon = 1e-6
            limite_izq = f.subs(x, c - epsilon).evalf()
            limite_der = f.subs(x, c + epsilon).evalf()

            if abs(limite_izq - limite_der) < 1e-3:
                limite_promedio = (limite_izq + limite_der) / 2
                limite_aprox = str(round(limite_promedio, 4))
            else: 
                limite_aprox = f"Diverge\nIzq: {round(limite_izq, 4)}\nDer: {round(limite_der, 4)}"

    
        # Textos en la interfaz
        resultado_txt.configure(state="normal")
        resultado_txt.delete("1.0", "end")
        resultado_txt.insert("1.0", f"Función: {f}\nLímite cuando x -> {c}\n\nLímite exacto:\n{limite_exacto}\n\nAproximación:\n{limite_aprox}")
        resultado_txt.configure(state="disabled")
# --- C) GRÁFICA (Sin numpy) ---
        ax.clear()
        
        # Definir los rangos de la gráfica
        if c == sp.oo: 
            inicio, fin = 1, 50
        elif c == -sp.oo: 
            inicio, fin = -50, -1
        else:
            c_val = float(c.evalf())
            inicio, fin = c_val - 5, c_val + 5

        # Crear lista de X manualmente usando un ciclo for
        num_puntos = 200
        paso = (fin - inicio) / (num_puntos - 1)
        x_vals = [inicio + i * paso for i in range(num_puntos)]

        # Evaluar la función en cada punto
        f_numerica = sp.lambdify(x, f, modules=['math'])
        y_vals = []
        
        for val in x_vals:
            try:
                # Evitar graficar el punto exacto si es una discontinuidad para no romper la línea
                if c != sp.oo and c != -sp.oo and abs(val - c_val) < 0.001:
                    y_vals.append(float('nan'))
                    continue
                y = f_numerica(val)
                y_vals.append(y)
            except:
                y_vals.append(float('nan'))

        # Dibujar la línea principal
        ax.plot(x_vals, y_vals, label=f"f(x)", color="cyan")
        
        # Dibujar el punto o la asíntota si es un número finito
        if c != sp.oo and c != -sp.oo:
            ax.axvline(x=c_val, color="gray", linestyle="--", alpha=0.4, label=f"x = {c}")
            
            try:
                lim_num = float(limite_exacto)
                eval_original = f.subs(x, c).evalf()
                # Comprobar si el punto existe o es un "agujero"
                if eval_original.is_number and not eval_original.has(sp.nan):
                    ax.plot(c_val, lim_num, marker='o', markersize=8, color='red', label="Punto Definido")
                else:
                    ax.plot(c_val, lim_num, marker='o', markersize=8, markerfacecolor='black', markeredgecolor='red', markeredgewidth=2, label="Agujero (Límite)")
            except:
                pass # Si el límite es texto ("No existe"), no grafica punto

        ax.legend()
        ax.grid(True, linestyle=":", alpha=0.4)
        canvas.draw()

    except Exception as e:
        # Atrapar errores por si el usuario escribe mal la función
        resultado_txt.configure(state="normal")
        resultado_txt.delete("1.0", "end")
        resultado_txt.insert("1.0", f"Error en la expresión matemática:\n{e}\n\nRecuerda usar * para multiplicar y ** para potencias.")
        resultado_txt.configure(state="disabled")
# ==========================================
# 2. CONFIGURACIÓN DE LA INTERFAZ GRÁFICA
# ==========================================

# Configuración principal de la ventana
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk() # Instancia directa (Sin clases)
app.geometry("900x600")
app.title("Analizador de Límites")

# Adaptación de redimensionamiento
app.grid_columnconfigure(0, weight=1)
app.grid_rowconfigure(0, weight=1)

# Creación de pestañas
tabs = ctk.CTkTabview(app)
tabs.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

tab_inicio = tabs.add("Inicio")
tab_calculadora = tabs.add("Calculadora de Límites")


# CONTENIDO: Pestaña de Inicio

titulo = ctk.CTkLabel(tab_inicio, text="Bienvenido al Analizador", font=("Arial", 30, "bold"))
titulo.pack(pady=25)

texto_intro = """Programa para calcular y representar límites matemáticos.

Características de este software:
- Interfaz gráfica con CustomTkinter usando pestañas.
- Gráficos integrados con Matplotlib.
- Cálculo de límites analítico por sustitución y factorización (sin sp.limit).
- Evaluación lateral numérica.
- Generación de coordenadas con Python puro (sin numpy)."""

caja = ctk.CTkTextbox(tab_inicio, width=600, height=200, font=("Arial", 14))
caja.pack(pady=20)
caja.insert("1.0", texto_intro)
caja.configure(state="disabled")


# CONTENIDO: Pestaña Calculadora

contenedor = ctk.CTkFrame(tab_calculadora) 
contenedor.pack(fill="both", expand=True, padx=10, pady=10)

# Panel izquierdo para los controles
panel = ctk.CTkFrame(contenedor, width=320)
panel.pack(side="left", fill="y", padx=10, pady=10)

# Panel derecho para el gráfico
grafico_frame = ctk.CTkFrame(contenedor)
grafico_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

ctk.CTkLabel(panel, text="Cálculo de Límite", font=("Arial", 20, "bold")).pack(pady=15)

ctk.CTkLabel(panel, text="Función f(x):").pack()
entry_funcion = ctk.CTkEntry(panel, placeholder_text="Ej: (x**2-1)/(x-1)", width=250)
entry_funcion.pack(pady=5)

ctk.CTkLabel(panel, text="Valor al que tiende x (c):").pack()
entry_c = ctk.CTkEntry(panel, placeholder_text="Ej: 0, pi, oo", width=250)
entry_c.pack(pady=5)

# Botón que llama a la función principal que creamos arriba
ctk.CTkButton(panel, text="Calcular y Graficar", command=calcular_limite).pack(pady=20)

resultado_txt = ctk.CTkTextbox(panel, width=280, height=200)
resultado_txt.pack(pady=10)
resultado_txt.insert("1.0", "Ingresa los datos y presiona calcular.")
resultado_txt.configure(state="disabled")

# Preparar el lienzo de Matplotlib vacío al iniciar
figura = Figure(figsize=(5, 4), dpi=100)
# Poner fondo oscuro a la gráfica para que combine con CustomTkinter
figura.patch.set_facecolor('#2b2b2b')
ax = figura.add_subplot(111)
ax.set_facecolor('#2b2b2b')
ax.tick_params(colors='white')

canvas = FigureCanvasTkAgg(figura, master=grafico_frame)
canvas.get_tk_widget().pack(fill="both", expand=True)


# 3. PUNTO DE ARRANQUE DEL PROGRAMA

if __name__ == "__main__":
    app.mainloop()
