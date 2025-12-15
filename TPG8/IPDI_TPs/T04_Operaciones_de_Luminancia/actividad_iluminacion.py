import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt
import imageio

# ---------------- Funciones de procesamiento ----------------

def normalizar_imagen(img):
    return np.clip(img / 255., 0., 1.)

def rgb_a_yiq(img):
    yiq = np.zeros(img.shape)
    yiq[:, :, 0] = 0.229 * img[:, :, 0] + 0.587 * img[:, :, 1] + 0.114 * img[:, :, 2]
    yiq[:, :, 1] = 0.595716 * img[:, :, 0] - 0.274453 * img[:, :, 1] - 0.321263 * img[:, :, 2]
    yiq[:, :, 2] = 0.211456 * img[:, :, 0] - 0.522591 * img[:, :, 1] + 0.311135 * img[:, :, 2]
    return yiq

def ajustar_metodo_raiz(yiq):
    yiq = yiq.copy()
    yiq[:, :, 0] = np.clip(yiq[:, :, 0], 0, 1)
    yiq[:, :, 0] = np.sqrt(yiq[:, :, 0])
    return yiq

def ajustar_metodo_cuadrado(yiq):
    yiq = yiq.copy()
    yiq[:, :, 0] = np.clip(yiq[:, :, 0], 0, 1)
    yiq[:, :, 0] = yiq[:, :, 0] ** 2
    return yiq

def ajustar_lineal_trozos(Y, Ymin=0.2, Ymax=0.8):
    Y_copy = np.zeros_like(Y)
    Y_copy[Y > Ymax] = 1
    mask = (Y >= Ymin) & (Y <= Ymax)
    Y_copy[mask] = (Y[mask] - Ymin) / (Ymax - Ymin)
    return Y_copy

def yiq_a_rgb(yiq):
    yiq = np.clip(yiq, -1, 1)
    rgb = np.zeros(yiq.shape)
    rgb[:, :, 0] = yiq[:, :, 0] + 0.9663 * yiq[:, :, 1] + 0.6210 * yiq[:, :, 2]
    rgb[:, :, 1] = yiq[:, :, 0] - 0.2721 * yiq[:, :, 1] - 0.6474 * yiq[:, :, 2]
    rgb[:, :, 2] = yiq[:, :, 0] - 1.1070 * yiq[:, :, 1] + 1.7046 * yiq[:, :, 2]
    return np.clip(rgb, 0, 1)

def graficar_imagenes(img_original, img_alterada, metodo):
    import time  # necesario para dar tiempo al render

    titulos = {
        'raiz': "Método de la Raíz",
        'lineal': "Método Lineal por Trozos",
        'cuadrado': "Método del Cuadrado"
    }
    fig = plt.figure(figsize=(8, 4))
    plt.suptitle(titulos.get(metodo, "Transformación"), fontsize=16)
    plt.subplot(1, 2, 1)
    plt.imshow(img_original)
    plt.title("Imagen Original")
    plt.axis('off')
    plt.subplot(1, 2, 2)
    plt.imshow(img_alterada)
    plt.title("Imagen Alterada")
    plt.axis('off')

    manager = plt.get_current_fig_manager()
    plt.pause(0.001)  # fuerza render inicial
    manager.window.update_idletasks()
    time.sleep(0.05)  # da tiempo a que se calcule el tamaño

    w = manager.window.winfo_width()
    h = manager.window.winfo_height()
    sw = manager.window.winfo_screenwidth()
    sh = manager.window.winfo_screenheight()
    x = (sw // 2) - (w // 2)
    y = (sh // 2) - (h // 2)
    manager.window.geometry(f"+{x}+{y}")

    plt.show()


# ---------------- Interfaz Tkinter ----------------

def abrir_imagen():
    global img_original, img_normalizada, yiq
    ruta = filedialog.askopenfilename(filetypes=[("Archivos de imagen", "*.bmp;*.png;*.jpg")])
    if ruta:
        img_original = imageio.imread(ruta)
        img_pil = Image.fromarray(img_original).resize((300, 300))
        img_tk = ImageTk.PhotoImage(img_pil)
        canvas_imagen.create_image(0, 0, anchor="nw", image=img_tk)
        canvas_imagen.image = img_tk
        label_estado.config(text=f"Imagen cargada: {ruta.split('/')[-1]}")
        img_normalizada = normalizar_imagen(img_original)
        yiq = rgb_a_yiq(img_normalizada)

def procesar_imagen():
    if yiq is None:
        label_estado.config(text="Primero debes cargar una imagen.")
        return

    metodo = metodo_var.get()
    if metodo == 'raiz':
        yiq_alterada = ajustar_metodo_raiz(yiq)
    elif metodo == 'lineal':
        Y_modificada = ajustar_lineal_trozos(yiq[:, :, 0], Ymin=0.2, Ymax=0.8)
        yiq_alterada = yiq.copy()
        yiq_alterada[:, :, 0] = Y_modificada
    elif metodo == 'cuadrado':
        yiq_alterada = ajustar_metodo_cuadrado(yiq)
    else:
        label_estado.config(text="Método no reconocido.")
        return

    rgb_alterada = yiq_a_rgb(yiq_alterada)
    rgb_bytes = (rgb_alterada * 255).astype(np.uint8)
    graficar_imagenes(img_original, rgb_bytes, metodo)
    label_estado.config(text=f"Imagen procesada con método: {metodo}")

def centrar_ventana(ventana, ancho, alto):
    ventana.update_idletasks()
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = (pantalla_ancho // 2) - (ancho // 2)
    y = (pantalla_alto // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

# Variables globales
img_original = None
img_normalizada = None
yiq = None

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Prototipo de Procesamiento de Imagen")
centrar_ventana(ventana, 800, 500)
ventana.configure(bg="white")

# Sección izquierda: opciones
frame_izquierdo = tk.Frame(ventana, bg="white")
frame_izquierdo.pack(side="left", padx=20, pady=20)

tk.Label(frame_izquierdo, text="Método de Iluminancia", font=("Arial", 12, "bold"), bg="white").pack(anchor="w")

metodo_var = tk.StringVar(value="raiz")

tk.Radiobutton(frame_izquierdo, text="RAÍZ CUADRADA", variable=metodo_var, value="raiz", bg="white").pack(anchor="w")
tk.Radiobutton(frame_izquierdo, text="LINEAL A TROZOS", variable=metodo_var, value="lineal", bg="white").pack(anchor="w")
tk.Radiobutton(frame_izquierdo, text="POTENCIA", variable=metodo_var, value="cuadrado", bg="white").pack(anchor="w")

tk.Button(frame_izquierdo, text="PROCESAR IMAGEN", command=procesar_imagen, bg="#4CAF50", fg="white").pack(pady=10)

# Sección derecha: imagen
frame_derecho = tk.Frame(ventana, bg="white")
frame_derecho.pack(side="right", padx=20, pady=20)

canvas_imagen = tk.Canvas(frame_derecho, width=300, height=300, bg="gray")
canvas_imagen.pack()

tk.Button(frame_derecho, text="ABRIR IMAGEN", command=abrir_imagen, bg="#2196F3", fg="white").pack(pady=(10, 0))

label_estado = tk.Label(ventana, text="", bg="white", fg="black", font=("Arial", 10))
label_estado.pack(side="bottom", pady=10)

ventana.mainloop()
