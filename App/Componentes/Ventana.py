import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import filedialog
import numpy as np
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

        #A partir de aca, se podria poner esta funcionaliadad
        #en la barra de actividades, cambiar despues
        # Instancias de las barras laterales
        self.sidebars = {
            "archivos": BarraLateralArchivos(self.sidebar_container, self.caja_imagen),
            "imagenes": BarraLateralImagenes(self.sidebar_container, self.caja_imagen),
            "config": BarraLateralConfiguracion(self.sidebar_container),
            "guardar": BarraLateralGuardado(self.sidebar_container, self.caja_imagen)
        }
        # Por defecto muestro una
        self.mostrar_sidebar("archivos")


    def mostrar_sidebar(self, cual):
        """Oculta todas y muestra solo la seleccionada."""
        for sidebar in self.sidebars.values():
            sidebar.pack_forget()
        self.sidebars[cual].pack(fill="both", expand=True)

