import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
from Herramientas.Helper_img import * 
from Componentes.PanelDeEdicionSimple import * 
from Componentes.CajaImagen import *
import matplotlib.pyplot as plt

cadenaGlobal = {"funcion": None}
class PanelDeEdicionFiltrosDeFunciones(tk.Frame):

    def __init__(self, master, panelDeEdicionSimple: CajaDeImagen, **kwargs):
        super().__init__(master, **kwargs)
        self.panelSimple = panelDeEdicionSimple
        # Imágenes
        self.imgA = panelDeEdicionSimple.imagen
        self.figura = None
        # --- Selector de modo de combinación ---
        modos = [
        "Filtro Raiz",
        "Filtro Cuadratico",
        "Filtro Lineal a Trozos"
        ]
        # Crear la variable una sola vez y antes de construir el OptionMenu.
        self.var_cuasi = tk.StringVar(value=modos[0])

        tk.Label(self, text="Opciones de filtro:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        opciones = tk.OptionMenu(self, self.var_cuasi, *modos)
        opciones.grid(row=1, column=0, columnspan=1, pady=5, sticky="ew")

        tk.Button(self, text="Mostrar histograma", command=self.mostrar_histograma).grid(row=0, column=1, pady=5)

        # --- Tres labels para A, B y Resultado ---
        self.labelA = tk.Label(self, bg="lightgray", text="Imagen A", width=40, height=15)
        self.labelA.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)


        self.labelR = tk.Label(self, bg="lightgray", text="Resultado", width=40, height=15)
        self.labelR.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)


        # Botones (fila separada para evitar solapamientos)
        tk.Button(self, text="Cargar Imagen A", command=self.cargar_imgA).grid(row=3, column=0, pady=5)
        tk.Button(self, text="Aplicar", command= self.aplicar_filtro).grid(row=3, column=1, pady=5)


        tk.Button(self, text="Guardar resultado", command=self.guardar_resultado).grid(row=4, column=1, pady=5)
        tk.Button(self, text="Salir", command=self.salir).grid(row=5, column=1, pady=5)

        if(not (self.imgA is None)):
            self._render_label(self.labelA, self.imgA)
        # Configuración del grid para que las columnas crezcan de forma proporcionada
        for c in range(2):
            self.grid_columnconfigure(c, weight=1)
            # Permitimos que la fila de las imágenes crezca cuando redimensionamos
            self.grid_rowconfigure(2, weight=1)

    def mostrar_histograma(self):
        """Combina imgA e imgB según var_cuasi"""
        if self.imgA is None:
            messagebox.showwarning("Atención", "Debes cargar las dos imágenes.")
            return

        # Redimensionar imgA
        arrA = np.asarray(self.imgA.copy(), dtype=np.uint8)
        plt.hist(rgb_to_yiq(arrA)[...,0].ravel(), bins=10, edgecolor='black')
        plt.xlabel('Valor')
        plt.ylabel('Frecuencia')
        plt.title('Histograma de A')
        plt.show()
        return


    def aplicar_filtro(self):
        """Combina imgA e imgB según var_cuasi"""
        if self.imgA is None:
            messagebox.showwarning("Atención", "Debes cargar las dos imágenes.")
            return

        # Redimensionar imgA
        arrA = np.asarray(self.imgA, dtype=np.uint8)
 
        modo = self.var_cuasi.get()

        # Funciones según modo
        if modo == "Filtro Raiz":
            arr = fx_str_array("math.sqrt(x)" ,arrA)
        elif modo == "Filtro Cuadratico":
            arr = fx_str_array("pow(x, 2)",arrA)
        elif modo == "Filtro Lineal a Trozos":
            def obtener_funcion():
                ventana = tk.Toplevel()
                ventana.title("Ingresar números")
                ventana.geometry("250x150")

                tk.Label(ventana, text="acotacion inferior:").pack(pady=5)
                entrada1 = tk.Entry(ventana)
                entrada1.pack()

                tk.Label(ventana, text="acotacion superior: ").pack(pady=5)
                entrada2 = tk.Entry(ventana)
                entrada2.pack()

                def aceptar():
                    try:
                        a = float(entrada1.get())
                        b = float(entrada2.get())
                        cadenaGlobal["funcion"] = f"1/({b-a})*x-1/({b-a})*{a}"
                        ventana.destroy()
                    except ValueError:
                        messagebox.showerror("Error", "Por favor ingresa números válidos.")

                tk.Button(ventana, text="Aceptar", command=aceptar).pack(pady=10)

                ventana.grab_set()
                ventana.wait_window()
            obtener_funcion()
            arr = fx_str_array(cadenaGlobal["funcion"],arrA)
        else:
            messagebox.showwarning("Atención", "Modo no reconocido.")
            return

        # Guardar resultado y renderizar
        self.resultado = Image.fromarray(arr)
        self._render_label(self.labelR, self.resultado)


        # --- Funciones auxiliares ---
    def _render_label(self, label, img):
        """Muestra img en un Label dado y guarda la referencia para evitar GC"""
        tk_img = ImageTk.PhotoImage(img)
        label.config(image=tk_img)
        label.image = tk_img  # guardamos la referencia en el label

    def salir(self):
        self.destroy()
        self.panelSimple.pack(fill="both", expand=True)

    def cargar_imgA(self):
        ruta = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg")])
        if ruta:
            self.imgA = Image.open(ruta).convert("RGB")
            self._render_label(self.labelA, self.imgA.copy().resize((400, 400), Image.LANCZOS))

    def guardar_resultado(self):
        if self.resultado is None:
            messagebox.showwarning("Atención", "No hay imagen para guardar.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"),
                                                            ("JPEG files", "*.jpg")])
        if file_path:
            self.resultado.save(file_path)



