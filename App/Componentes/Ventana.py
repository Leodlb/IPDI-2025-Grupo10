import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import filedialog
import numpy as np
from Herramientas.Helper_img import *
from Componentes.CajaImagen  import CajaDeImagen
from Componentes.BarraDeActividad import BarraDeActividades
from Componentes.BarrasLaterales import BarraLateralArchivos, BarraLateralConfiguracion,BarraLateralGuardado,BarraLateralImagenes

class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Editor de imagenes")
        self.geometry("700x400")

        # Barra de actividades
        self.barra_actividades = BarraDeActividades(self, self)
        self.barra_actividades.pack(side="left", fill="y")

        # Contenedor para las barras laterales
        self.sidebar_container = tk.Frame(self, bg="white", width=150)
        self.sidebar_container.pack(side="left", fill="y")

        # Área principal
        self.main_area = tk.Frame(self, bg="white")
        self.main_area.pack(side="right", fill="both", expand=True)

        # Caja de Imagen (panel derecho)
        self.caja_imagen = CajaDeImagen(self, width=550, height=500)
        self.caja_imagen.pack(side="right", fill="both", expand=True)

        # Instancias de las barras laterales
        self.sidebars = {
            "archivos": BarraLateralArchivos(self.sidebar_container, self.caja_imagen),
            "imagenes": BarraLateralImagenes(self.sidebar_container, self.caja_imagen),
            "config": BarraLateralConfiguracion(self.sidebar_container),
            "guardar": BarraLateralGuardado(self.sidebar_container, self.caja_imagen)
        }
        self.mostrar_sidebar("archivos")

    def mostrar_cuasi_operacion(self, modo):
        # Limpia el área principal
        for widget in self.main_area.winfo_children():
            widget.destroy()

        frame_cuasi = tk.Frame(self.main_area, bg="white")
        frame_cuasi.pack(fill="both", expand=True)

        # Menú desplegable
        tk.Label(frame_cuasi, text="Selecciona la operación").grid(row=0, column=0, columnspan=3, pady=5)
        self.opciones_cuasi = [
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
            "If-lighter"
        ]
        self.var_cuasi = tk.StringVar(value=self.opciones_cuasi[0])
        tk.OptionMenu(frame_cuasi, self.var_cuasi, *self.opciones_cuasi).grid(row=1, column=0, columnspan=3, pady=5)

        # Cajas de imagen
        self.cajaA = CajaDeImagen(frame_cuasi, width=200, height=200)
        self.cajaA.grid(row=2, column=0, padx=5, pady=5)
        self.cajaB = CajaDeImagen(frame_cuasi, width=200, height=200)
        self.cajaB.grid(row=2, column=1, padx=5, pady=5)
        self.cajaResultado = CajaDeImagen(frame_cuasi, width=200, height=200)
        self.cajaResultado.grid(row=2, column=2, padx=5, pady=5)

        if self.caja_imagen and self.caja_imagen.imagen is not None:
            self.cajaA.imagen = self.caja_imagen.imagen.copy()
            self.cajaA._render_image()

        if self.caja_imagen:
            self.caja_imagen.pack_forget()

        tk.Button(frame_cuasi, text="Cargar Imagen A",
                command=lambda: self.cargar_img(self.cajaA)).grid(row=3, column=0, pady=5)
        tk.Button(frame_cuasi, text="Cargar Imagen B",
                command=lambda: self.cargar_img(self.cajaB)).grid(row=3, column=1, pady=5)
        tk.Button(frame_cuasi, text="Combinar",
                command=self.combinar_cuasi).grid(row=3, column=2, pady=5)
        tk.Button(frame_cuasi, text="Guardar resultado",
                command=self.guardar_resultado).grid(row=4, column=1, pady=5)
        tk.Button(frame_cuasi, text="salir",
                command= lambda: self.salir(frame_cuasi)).grid(row=5, column=3, pady=5)

    def salir(self, frame):
        frame.destroy()
        self.caja_imagen.pack(side="right", fill="both", expand=True)


    def mostrar_sidebar(self, cual):
        for sidebar in self.sidebars.values():
            sidebar.pack_forget()
        self.sidebars[cual].pack(fill="both", expand=True)

    def cargar_img(self, caja_destino):
        ruta = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg")])
        if not ruta:
            return
        nueva = Image.open(ruta).convert("RGB")
        nueva = nueva.resize((400, 400), Image.LANCZOS)
        caja_destino.imagen = nueva
        caja_destino._imagen_procesada = None
        caja_destino._render_image()

    def combinar_cuasi(self):
        if self.cajaA.imagen is None or self.cajaB.imagen is None:
            tk.messagebox.showwarning("Atención", "Debes cargar las dos imágenes.")
            return

        imgB_resized = self.cajaB.imagen.resize(self.cajaA.imagen.size)
        arrA = np.asarray(self.cajaA.imagen.convert("RGB"), dtype=np.uint8)
        arrB = np.asarray(imgB_resized.convert("RGB"), dtype=np.uint8)

        modo = self.var_cuasi.get()

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

        self.cajaResultado.imagen = Image.fromarray(arr)
        self.cajaResultado._render_image()

    def guardar_resultado(self):
        if not self.cajaResultado.imagen:
            tk.messagebox.showwarning("Atención", "No hay imagen para guardar.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                filetypes=[("PNG files", "*.png"),
                                                            ("JPEG files", "*.jpg")])
        if file_path:
            self.cajaResultado.imagen.save(file_path)
