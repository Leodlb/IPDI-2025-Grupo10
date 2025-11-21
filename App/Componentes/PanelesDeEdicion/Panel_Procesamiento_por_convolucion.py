import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
from Herramientas.Helper_img import * 
from Herramientas.Helper_filtro_convolucion import * 
from Componentes.PanelesDeEdicion.Panel_tp1_edicion_simple import *
from Componentes.PanelesDeEdicion.CajaImagen import *
import matplotlib.pyplot as plt

cadenaGlobal = {"funcion": None}
class PanelDeEdicionConvoluciones(tk.Frame):

    def __init__(self, master, panelDeEdicionSimple: CajaDeImagen, **kwargs):
        super().__init__(master, **kwargs)
        self.panelSimple = panelDeEdicionSimple
        self.imgA = panelDeEdicionSimple.imagen
        self.resultado = None

        # --- Selector de modo ---
        modos = [
            "Convolución Bartlett 3x3",
            "Convolución Bartlett 5x5",
            "Convolución Bartlett 7x7",
            "Convolución Bartlett 9x9",
            "Convolución Gaussiana 3x3",
            "Convolución Gaussiana 5x5", 
            "Convolución Gaussiana 7x7",
            "Convolución Gaussiana 9x9",
            "Convolución Laplace 8 vecinos",
            "Convolución Laplace 4 vecinos",
            "Convolución Laplace v4 Filtro Mejora 0.2",
            "Convolución Laplace v4 Filtro Mejora 0.4",
            "Convolución Laplace v8 Filtro Mejora 0.2",
            "Convolución Laplace v8 Filtro Mejora 0.4",
            "Convolución derecha" ,
            "Convolución izquierda",
            "Convolución arriba",
            "Convolución abajo",
            "Convolución diagonal derecha",
            "Convolución diagonal izquierda",
            "Convolución diagonal abajo izquierda",
            "Convolución diagonala abajo derecha"
        ]

        self.var_cuasi = tk.StringVar(value=modos[0])
        tk.Label(self, text="Opciones de filtro:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        tk.OptionMenu(self, self.var_cuasi, *modos).grid(row=1, column=0, pady=5, sticky="ew")

        tk.Button(self, text="Mostrar histograma", command=self.mostrar_histograma).grid(row=0, column=1, pady=5)
        self.labelA = tk.Label(self, bg="lightgray", text="Imagen A", width=40, height=15)
        self.labelA.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        self.labelR = tk.Label(self, bg="lightgray", text="Resultado", width=40, height=15)
        self.labelR.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)

        tk.Button(self, text="Cargar Imagen A", command=self.cargar_imgA).grid(row=3, column=0, pady=5)
        tk.Button(self, text="Aplicar", command=self.aplicar_filtro).grid(row=3, column=1, pady=5)
        tk.Button(self, text="Guardar resultado", command=self.guardar_resultado).grid(row=4, column=1, pady=5)
        tk.Button(self, text="Salir", command=self.salir).grid(row=5, column=1, pady=5)

        if self.imgA is not None:
            self._render_label(self.labelA, self.imgA)
        for c in range(2):
            self.grid_columnconfigure(c, weight=1)
            self.grid_rowconfigure(2, weight=1)

    # --- Mostrar histograma ---
    def mostrar_histograma(self):
        if self.imgA is None:
            messagebox.showwarning("Atención", "Debes cargar una imagen.")
            return
        arrA = np.asarray(self.imgA, dtype=np.uint8)
        plt.hist(rgb_to_yiq(arrA)[...,0].ravel(), bins=20, edgecolor='black')
        plt.xlabel('Valor'); plt.ylabel('Frecuencia')
        plt.title('Histograma de A')
        plt.show()

    # --- Aplicar filtro / convolución ---
    def aplicar_filtro(self):
        if self.imgA is None:
            messagebox.showwarning("Atención", "Debes cargar la imagen.")
            return

        modo = self.var_cuasi.get()
        arrA = np.asarray(self.imgA, dtype=np.float32)

        # --- NIVEL 1 ---
        if "Bartlett" in modo:
            size = int(modo[-1])
            kernel = matriz_bartlett(size)

        else:
            # --- NIVEL 2 ---
            if "Gaussiana" in modo:
                size = int(modo[-1])
                kernel = matriz_gaussiana(size)

            else:
                # --- NIVEL 3: otros kernels fijos ---
                if modo == "Convolución Laplace 4 vecinos":
                    kernel = KERNELS_CONVOLUCION["Convolución Laplace 4 vecinos"]

                elif modo == "Convolución Laplace 8 vecinos":
                    kernel = KERNELS_CONVOLUCION["Convolución Laplace 8 vecinos"]

                elif modo == "Convolución Laplace v4 Filtro Mejora 0.2":
                    kernel = KERNELS_CONVOLUCION["Convolución Laplace v4 Filtro Mejora 0.2"]

                elif modo == "Convolución Laplace v4 Filtro Mejora 0.4":
                    kernel = KERNELS_CONVOLUCION["Convolución Laplace v4 Filtro Mejora 0.4"]

                elif modo == "Convolución Laplace v8 Filtro Mejora 0.2":
                    kernel = KERNELS_CONVOLUCION["Convolución Laplace v8 Filtro Mejora 0.2"]

                elif modo == "Convolución Laplace v8 Filtro Mejora 0.4":
                    kernel = KERNELS_CONVOLUCION["Convolución Laplace v8 Filtro Mejora 0.4"]

                elif modo == "Convolución derecha":
                    kernel = KERNELS_CONVOLUCION["Convolución derecha"]

                elif modo == "Convolución izquierda":
                    kernel = KERNELS_CONVOLUCION["Convolución izquierda"]

                elif modo == "Convolución arriba":
                    kernel = KERNELS_CONVOLUCION["Convolución arriba"]

                elif modo == "Convolución abajo":
                    kernel = KERNELS_CONVOLUCION["Convolución abajo"]

                elif modo == "Convolución diagonal derecha":
                    kernel = KERNELS_CONVOLUCION["Convolución diagonal derecha"]

                elif modo == "Convolución diagonal izquierda":
                    kernel = KERNELS_CONVOLUCION["Convolución diagonal izquierda"]

                elif modo == "Convolución diagonal abajo izquierda":
                    kernel = KERNELS_CONVOLUCION["Convolución diagonal abajo izquierda"]

                elif modo == "Convolución diagonala abajo derecha":
                    kernel = KERNELS_CONVOLUCION["Convolución diagonala abajo derecha"]

                else:
                    messagebox.showerror("Error", f"No existe kernel para '{modo}'")
                    return

        # --- aplicar el pipeline general ---
        resultado_arr = aplicar_kernel_grises(arrA, kernel)

        # mostrar
        self.resultado = Image.fromarray(resultado_arr)
        self._render_label(self.labelR, self.resultado)


    # --- Auxiliares ---
    def _render_label(self, label, img):
        tk_img = ImageTk.PhotoImage(img.resize((400,400), Image.LANCZOS))
        label.config(image=tk_img)
        label.image = tk_img

    def salir(self):
        self.destroy()
        self.panelSimple.pack(fill="both", expand=True)

    def cargar_imgA(self):
        ruta = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png;*.bmp;*.jpg;*.jpeg")])
        if ruta:
            self.imgA = Image.open(ruta).convert("RGB")
            self._render_label(self.labelA, self.imgA)

    def guardar_resultado(self):
        if self.resultado is None:
            messagebox.showwarning("Atención", "No hay imagen para guardar.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"),
                                                            ("JPEG files", "*.jpg")])
        if file_path:
            self.resultado.save(file_path)