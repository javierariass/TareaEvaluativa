import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageFilter  # Biblioteca para manejar imágenes y aplicar filtros

# Función principal para ejecutar los cálculos y generar la gráfica
def ejecutar():
    try:
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

        # Puntos de partición
        x_partitions = np.linspace(start, end, num_partitions + 1)
        dx = (end - start) / num_partitions

        # Cálculo de las sumas inferior y superior
        lower_sum = np.sum(np.minimum(dynamic_function(x_partitions[:-1]), dynamic_function(x_partitions[1:])) * dx)
        upper_sum = np.sum(np.maximum(dynamic_function(x_partitions[:-1]), dynamic_function(x_partitions[1:])) * dx)
        integral_approximation = (lower_sum + upper_sum) / 2  # Promedio de las sumas

        # Gráfica de la función
        x_dense = np.linspace(start, end, 1000)
        y_dense = dynamic_function(x_dense)

        plt.figure(num="Tarea Extraclase", figsize=(10, 6))
        plt.plot(x_dense, y_dense, label="Función $f(x)$", color="blue")
        plt.scatter(x_partitions, dynamic_function(x_partitions), color="red", label="Puntos de partición")

        # Dibujar líneas rojas en discontinuidades
        for i in range(1, len(x_dense)):
            if np.abs(y_dense[i] - y_dense[i - 1]) > 1e6:  # Umbral para detectar discontinuidades
                plt.axvline(x=x_dense[i], color="red", linestyle="--", linewidth=2, label="Discontinuidad" if i == 1 else "")

        # Rectángulos para las sumas inferior y superior
        for i in range(num_partitions):
            plt.fill_between(
                [x_partitions[i], x_partitions[i + 1]],
                0, np.minimum(dynamic_function(x_partitions[i]), dynamic_function(x_partitions[i + 1])),
                color="green", alpha=0.4, label="Suma inferior" if i == 0 else ""
            )
            plt.fill_between(
                [x_partitions[i], x_partitions[i + 1]],
                np.minimum(dynamic_function(x_partitions[i]), dynamic_function(x_partitions[i + 1])),
                np.maximum(dynamic_function(x_partitions[i]), dynamic_function(x_partitions[i + 1])),
                color="orange", alpha=0.4, label="Suma superior" if i == 0 else ""
            )

        # Ajustes de la gráfica
        plt.title("Demostración Visual del Teorema de Integrabilidad de Riemann")
        plt.xlabel("$x$")
        plt.ylabel("$f(x)$")
        plt.axhline(0, color="black", linewidth=0.8)
        plt.legend()
        plt.grid(alpha=0.5)

        # Mostrar valores de las sumas y la integral aproximada en la gráfica
        plt.text(0.05, 0.85, f"Suma inferior: {lower_sum:.4f}\nSuma superior: {upper_sum:.4f}\nIntegral aproximada: {integral_approximation:.4f}",
                 transform=plt.gca().transAxes, fontsize=10, bbox=dict(facecolor="white", alpha=0.7))
        plt.text(0.97, 0.03, f"Función: {funcion_input}", transform=plt.gca().transAxes,
                 fontsize=10, color="black", ha="right", bbox=dict(facecolor="white", alpha=0.8))

        plt.show()

    except Exception as e:
        messagebox.showerror("Error", f"Datos inválidos: {str(e)}")

# Crear la ventana principal
window = tk.Tk()
window.title("Tarea Extraclase")
window.geometry("600x600")

# Cambiar el fondo de la ventana usando Pillow con desenfoque
try:
    background_image_pil = Image.open("img.png")  # Cargar la imagen
    blurred_image = background_image_pil.filter(ImageFilter.GaussianBlur(2))  # Aplicar desenfoque (ajusta el valor de 5)
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

tk.Label(window, text="Intervalo").place(x = 267,y = 280)

tk.Label(window, text="Minimo").place(x=220, y=310)
I1 = tk.Entry(window, font=("Arial", 12), width=5)
I1.place(x=220, y=340)

tk.Label(window, text="Maximo:").place(x=320, y=310)
I2 = tk.Entry(window, font=("Arial", 12), width=5)
I2.place(x=320, y=340)

tk.Label(window, text="Cantidad de particiones:").place(x=233, y=400)
partition = tk.Entry(window, font=("Arial", 12), width=30)
partition.place(x=155, y=430)

# Botón para ejecutar
execute_button = tk.Button(window, text="Ejecutar", command=ejecutar)
execute_button.place(x=265, y=470)

# Iniciar el bucle principal
window.mainloop()
