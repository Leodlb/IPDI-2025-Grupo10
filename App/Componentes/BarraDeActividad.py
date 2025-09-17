import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import filedialog
import numpy as np
from Componentes.BarrasLaterales import *

class BarraDeActividades(tk.Frame):
    def __init__(self, ventana, main_area, **kwargs):
        super().__init__(ventana, bg="darkgray", width=45, **kwargs)
        self.grid(row=0, column=0, sticky="nsew")
        # Crear las sidebars aquí
        self.sidebars = {
            "archivos": BarraLateralArchivos(ventana.sidebar_container, ventana.caja_imagen),
            "imagenes": BarraLateralImagenes(ventana.sidebar_container, main_area, ventana.caja_imagen),
            "config":   BarraLateralConfiguracion(ventana.sidebar_container),
            "guardar":  BarraLateralGuardado(ventana.sidebar_container, ventana.caja_imagen),
        }

        # Botones que muestran cada sidebar
        tk.Button(self, text="📂",
                  command=lambda: ventana.mostrar_sidebar(self.sidebars["archivos"])).pack(ipady=7, ipadx=7)
        tk.Button(self, text="📝",
                  command=lambda: ventana.mostrar_sidebar(self.sidebars["imagenes"])).pack(ipady=7, ipadx=7)
        tk.Button(self, text="⚙️",
                  command=lambda: ventana.mostrar_sidebar(self.sidebars["config"])).pack(ipady=6, ipadx=6)
        tk.Button(self, text="💾",
                  command=lambda: ventana.mostrar_sidebar(self.sidebars["guardar"])).pack(ipady=7, ipadx=7)


