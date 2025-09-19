import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
from Herramientas.Helper_img import *
from Componentes.PanelDeEdicionSimple import *
from Componentes.CajaImagen import *


class PanelDeEdicionArimeticaDePixeles(tk.Frame):
    

    def __init__(self, master, panelDeEdicionSimple: CajaDeImagen, **kwargs):
        super().__init__(master, **kwargs)
        self.panelSimple = panelDeEdicionSimple
        # Imágenes
        self.imgA = panelDeEdicionSimple.imagen
        self.imgB = None
        self.resultado = None
        # --- Selector de modo de combinación ---
        modos = [
        "Cuasi-suma RGB clampeada",
        "Cuasi-suma RGB promediada",
        "Cuasi-resta RGB clampeada",
        "Cuasi-resta RGB promediada",
        "Cuasi-suma YIQ clampeada",
        "Cuasi-suma YIQ promediada",
        "Cuasi-resta YIQ clampeada",
        "Cuasi-resta YIQ promediada",
        "Producto RGB",
        "Cociente RGB",
        "Resta absoluta RGB",
        "If-darker",
        "If-lighter",
        ]


        # Crear la variable una sola vez y antes de construir el OptionMenu.
        self.var_cuasi = tk.StringVar(value=modos[0])


        tk.Label(self, text="Modo de combinación:").grid(row=0, column=0, columnspan=1, pady=5)

        opciones = tk.OptionMenu(self, self.var_cuasi, *modos)
        opciones.grid(row=1, column=0, columnspan=1, pady=5, sticky="ew")


        # --- Tres labels para A, B y Resultado ---
        self.labelA = tk.Label(self, bg="lightgray", text="Imagen A", width=40, height=15)
        self.labelA.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)


        self.labelB = tk.Label(self, bg="lightgray", text="Imagen B", width=40, height=15)
        self.labelB.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)


        self.labelR = tk.Label(self, bg="lightgray", text="Resultado", width=40, height=15)
        self.labelR.grid(row=2, column=2, sticky="nsew", padx=5, pady=5)

        self._render_label(self.labelA, self.imgA)
        # Botones (fila separada para evitar solapamientos)
        tk.Button(self, text="Cargar Imagen A", command=self.cargar_imgA).grid(row=3, column=0, pady=5)
        tk.Button(self, text="Cargar Imagen B", command=self.cargar_imgB).grid(row=3, column=1, pady=5)
        tk.Button(self, text="Combinar", command=self.combinar_cuasi).grid(row=3, column=2, pady=5)


        tk.Button(self, text="Guardar resultado", command=self.guardar_resultado).grid(row=4, column=1, pady=5)
        tk.Button(self, text="Salir", command=self.salir).grid(row=4, column=2, pady=5)

        # Configuración del grid para que las columnas crezcan de forma proporcionada
        for c in range(3):
            self.grid_columnconfigure(c, weight=1)
            # Permitimos que la fila de las imágenes crezca cuando redimensionamos
            self.grid_rowconfigure(2, weight=1)

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
            self.imgA = Image.open(ruta).convert("RGB").resize((400, 400), Image.LANCZOS)
            self._render_label(self.labelA, self.imgA)

    def cargar_imgB(self):
        ruta = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg")])
        if ruta:
            self.imgB = Image.open(ruta).convert("RGB").resize((400, 400), Image.LANCZOS)
            self._render_label(self.labelB, self.imgB)

    def guardar_resultado(self):
        if self.resultado is None:
            messagebox.showwarning("Atención", "No hay imagen para guardar.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"),
                                                            ("JPEG files", "*.jpg")])
        if file_path:
            self.resultado.save(file_path)


    def combinar_cuasi(self):
        """Combina imgA e imgB según var_cuasi"""
        if self.imgA is None or self.imgB is None:
            messagebox.showwarning("Atención", "Debes cargar las dos imágenes.")
            return

        # Redimensionar imgB para que coincida con imgA
        imgB_resized = self.imgB.resize(self.imgA.size)
        arrA = np.asarray(self.imgA, dtype=np.uint8)
        arrB = np.asarray(imgB_resized, dtype=np.uint8)

        modo = self.var_cuasi.get()

        # Funciones según modo
        if modo == "Cuasi-suma RGB clampeada":
            arr = cuasi_suma_rgb_clampeada(arrA, arrB)
        elif modo == "Cuasi-suma RGB promediada":
            arr = cuasi_suma_rgb_promediada(arrA, arrB)
        elif modo == "Cuasi-resta RGB clampeada":
            arr = cuasi_resta_rgb_clampeada(arrA, arrB)
        elif modo == "Cuasi-resta RGB promediada":
            arr = cuasi_resta_rgb_promediada(arrA, arrB)
        elif modo == "Cuasi-suma YIQ clampeada":
            arr = cuasi_suma_yiq_clampeada(arrA, arrB)
        elif modo == "Cuasi-suma YIQ promediada":
            arr = cuasi_suma_yiq_promediada(arrA, arrB)
        elif modo == "Cuasi-resta YIQ clampeada":
            arr = cuasi_resta_yiq_clampeada(arrA, arrB)
        elif modo == "Cuasi-resta YIQ promediada":
            arr = cuasi_resta_yiq_promediada(arrA, arrB)
        elif modo == "Producto RGB":
            arr = producto_rgb(arrA, arrB)
        elif modo == "Cociente RGB":
            arr = cociente_rgb(arrA, arrB)
        elif modo == "Resta absoluta RGB":
            arr = resta_absoluta_rgb(arrA, arrB)
        elif modo == "If-darker":
            arr = if_darker(arrA, arrB)
        elif modo == "If-lighter":
            arr = if_lighter(arrA, arrB)
        else:
            messagebox.showwarning("Atención", "Modo no reconocido.")
            return

        # Guardar resultado y renderizar
        self.resultado = Image.fromarray(arr)
        self._render_label(self.labelR, self.resultado)
