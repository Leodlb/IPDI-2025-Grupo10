import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import filedialog
import numpy as np
from Componentes.BarrasLaterales import *

class BarraDeActividades(tk.Frame):
    """
    Contiene solo los botontes de activacion para la barra laterales
    Junto con el metodo para verlos
    """
    def __init__(self, ventana, main_area, **kwargs):
        super().__init__(ventana, bg="darkgray", width=45, **kwargs)
        self.grid(row=0, column=0, sticky="nsew")

        self.sidebar_container = ventana.sidebar_container

        self.sidebars = {
            "archivos": BarraLateralArchivos(self.sidebar_container, ventana.caja_imagen),
            "imagenes": BarraLateralImagenes(self.sidebar_container, main_area, ventana.caja_imagen),
            "config":   BarraLateralConfiguracion(self.sidebar_container),
            "guardar":  BarraLateralGuardado(self.sidebar_container, ventana.caja_imagen),
        }

        # Botones que muestran cada sidebar
        tk.Button(self, text="📂",
                  command=lambda: self.mostrar_sidebar(self.sidebars["archivos"])).pack(ipady=7, ipadx=7)
        tk.Button(self, text="📝",
                  command=lambda: self.mostrar_sidebar(self.sidebars["imagenes"])).pack(ipady=7, ipadx=7)
        tk.Button(self, text="⚙️",
                  command=lambda: self.mostrar_sidebar(self.sidebars["config"])).pack(ipady=6, ipadx=6)
        tk.Button(self, text="💾",
                  command=lambda: self.mostrar_sidebar(self.sidebars["guardar"])).pack(ipady=7, ipadx=7)

    def mostrar_sidebar(self, widget):
        """Oculta cualquier sidebar actual y muestra el widget dado."""
        for child in self.sidebar_container.winfo_children():
            child.pack_forget()
        widget.pack(fill="y", expand=True)

