import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageFilter
from matplotlib.animation import FuncAnimation

# Variables globales
current_figure = None
ani = None  # Para mantener activa la animación

def ejecutar():
    global current_figure, ani

    try:
        # Cerrar la figura anterior si existe
        if current_figure:
            plt.close(current_figure)
            current_figure = None
            ani = None

        # Obtener valores de las entradas
        funcion_input = function.get()
        start = int(I1.get())
        end = int(I2.get())
        num_partitions = int(partition.get())

        # Validar valores
        if num_partitions <= 0 or start >= end:
            raise ValueError("El número de particiones debe ser positivo y el intervalo válido.")

        # Crear una función dinámica a partir de la entrada
        def dynamic_function(x):
            return eval(funcion_input)

        # Gráfica inicial
        x_dense = np.linspace(start, end, 1000)
        y_dense = dynamic_function(x_dense)

        # Crear una nueva figura y almacenarla en la variable global
        current_figure, ax = plt.subplots(figsize=(10, 6))
        plt.subplots_adjust(bottom=0.3)  # Ajustar espacio inferior para el slider y botones

        ax.plot(x_dense, y_dense, label="Función $f(x)$: " + funcion_input, color="blue")  # Mostrar función en leyenda
        ax.axhline(0, color="black", linewidth=0.8)
        ax.set_title("Demostración Visual del Teorema de Integrabilidad de Riemann")
        ax.set_xlabel("$x$")
        ax.set_ylabel("$f(x)$")
        ax.grid(alpha=0.5)
        
        # Crear slider
        slider_ax = plt.axes([0.25, 0.1, 0.5, 0.03])  # Posición [x, y, ancho, alto]
        partition_slider = Slider(slider_ax, 'Particiones', 1, num_partitions, valinit=1, valstep=1)

        # Función para actualizar la gráfica
        def update(partitions):
            # Limpiar colecciones previas (rectángulos)
            while len(ax.collections) > 0:
                ax.collections[0].remove()

            # Limpiar textos previos
            while len(ax.texts) > 0:
                ax.texts[0].remove()

            x_partitions = np.linspace(start, end, int(partitions) + 1)
            dx = (end - start) / int(partitions)

            # Cálculo de las sumas inferior y superior
            y_values_start = dynamic_function(x_partitions[:-1])
            y_values_end = dynamic_function(x_partitions[1:])
            lower_sum = np.sum(np.minimum(y_values_start, y_values_end) * dx)
            upper_sum = np.sum(np.maximum(y_values_start, y_values_end) * dx)
            integral_approximation = (lower_sum + upper_sum) / 2  # Promedio de las sumas

            # Dibujar rectángulos
            for i in range(int(partitions)):
                ax.fill_between(
                    [x_partitions[i], x_partitions[i + 1]],
                    0, dynamic_function(x_partitions[i]),
                    color="green", alpha=0.4, label="Suma inferior" if i == 0 else ""
                )
                ax.fill_between(
                    [x_partitions[i], x_partitions[i + 1]],
                    dynamic_function(x_partitions[i]),
                    dynamic_function(x_partitions[i + 1]),
                    color="orange", alpha=0.4, label="Suma superior" if i == 0 else ""
                )

            # Actualizar texto dinámico
            ax.text(0.05, 0.85, f"Suma inferior: {lower_sum:.4f}\nSuma superior: {upper_sum:.4f}\nIntegral aproximada: {integral_approximation:.4f}",
                    transform=ax.transAxes, fontsize=10, bbox=dict(facecolor="white", alpha=0.7))
            ax.text(0.97, 0.03, f"Particiones: {int(partitions)}", transform=ax.transAxes,
                    fontsize=10, color="black", ha="right", bbox=dict(facecolor="white", alpha=0.8))

            handles, labels = ax.get_legend_handles_labels()
            unique = [(h, l) for i, (h, l) in enumerate(zip(handles, labels)) if l not in labels[:i]]
            ax.legend(*zip(*unique), loc="upper right") 


            # Redibujar la gráfica
            current_figure.canvas.draw_idle()

        # Vincular el slider con la función de actualización
        partition_slider.on_changed(update)

        # Botón de animación automática en la figura
        def start_animation(event):
            global ani

            def auto_update(i):
                partition_slider.set_val(i + 1)

            # Crear la animación automática
            ani = FuncAnimation(current_figure, auto_update, frames=range(0, num_partitions), interval=500, repeat=True)
            plt.draw()

        def stop_animation(event):
            global ani
            if ani:
                ani.event_source.stop()  # Detener la animación

        # Botón para iniciar animación automática
        auto_button_ax = plt.axes([0.15, 0.01, 0.2, 0.05])  # Posición para el botón
        auto_button = Button(auto_button_ax, 'Automático')
        auto_button.on_clicked(start_animation)

        # Botón para detener animación automática
        stop_button_ax = plt.axes([0.65, 0.01, 0.2, 0.05])  # Posición para el botón
        stop_button = Button(stop_button_ax, 'Detener')
        stop_button.on_clicked(stop_animation)

        # Mostrar la función analizada debajo de la gráfica
        ax.text(0.5, -0.15, f"Función analizada: {funcion_input}", transform=ax.transAxes,
                fontsize=12, color="blue", ha="center")

        # Asegurar que la leyenda muestra ambos colores una vez
        handles, labels = ax.get_legend_handles_labels()
        unique = [(h, l) for i, (h, l) in enumerate(zip(handles, labels)) if l not in labels[:i]]
        ax.legend(*zip(*unique))

        plt.show()

    except Exception as e:
        messagebox.showerror("Error", f"Datos inválidos: {str(e)}")

# Crear la ventana principal
window = tk.Tk()
window.title("Tarea Extraclase")
window.geometry("600x700")

# Cambiar el fondo de la ventana usando Pillow con desenfoque
try:
    background_image_pil = Image.open("img.png")  # Cargar la imagen
    blurred_image = background_image_pil.filter(ImageFilter.GaussianBlur(2))  # Aplicar desenfoque
    background_image_tk = ImageTk.PhotoImage(blurred_image)  # Convertir a formato compatible con tkinter
    background_label = tk.Label(window, image=background_image_tk)
    background_label.place(relwidth=1, relheight=1)
except Exception as e:
    messagebox.showerror("Error", f"No se pudo cargar o procesar la imagen de fondo: {str(e)}")

# Etiqueta de ayuda al inicio
tk.Label(window, text="""=== Guía de funciones disponibles ===
Operadores básicos: +, -, *, /, ** (potencia)
Funciones matemáticas comunes (requieren 'np.'):
    np.sin(x)   -> Seno
    np.cos(x)   -> Coseno
    np.tan(x)   -> Tangente
    np.exp(x)   -> Exponencial (e^x)
    np.log(x)   -> Logaritmo natural (base e)
    np.log10(x) -> Logaritmo base 10
    np.sqrt(x)  -> Raíz cuadrada
    np.abs(x)   -> Valor absoluto
""", justify="left", font=("Arial", 10), bg="lightyellow").pack(pady=10)

# Etiquetas y entradas
tk.Label(window, text="Función:").pack(pady=5)
function = tk.Entry(window, font=("Arial", 12), width=30)
function.pack()

tk.Label(window, text="Intervalo").place(x=267, y=280)

tk.Label(window, text="Mínimo").place(x=220, y=310)
I1 = tk.Entry(window, font=("Arial", 12), width=5)
I1.place(x=220, y=340)

tk.Label(window, text="Máximo:").place(x=320, y=310)
I2 = tk.Entry(window, font=("Arial", 12), width=5)
I2.place(x=320, y=340)

tk.Label(window, text="Cantidad de particiones:").place(x=233, y=400)
partition = tk.Entry(window, font=("Arial", 12), width=30)
partition.place(x=155, y=430)

# Botón para ejecutar
execute_button = tk.Button(window, text="Ejecutar", command=ejecutar)
execute_button.place(x=265, y=500)

# Iniciar el bucle principal
window.mainloop()
