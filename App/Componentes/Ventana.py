import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import filedialog
import numpy as np
from Herramientas.Helper_img import *
from Componentes.CajaImagen  import CajaDeImagen
from Componentes.BarraDeActividad import BarraDeActividades
from Componentes.BarrasLaterales import *


class VentanaPrincipal(tk.Tk):
    """
    En esta clase esta lo que seria conceptualmente la Ventana.
    Para quedar claro esta clase espera que se construyan tres cosas:
        * Barra de actividad 
        * Barras Laterales 
        * Area de trabajo (main_area)
    """
    def __init__(self):
        super().__init__()
        self.title("Editor de imágenes")
        self.geometry("700x400")

        # --- Crear widgets (cualquiera puede ir primero) ---
        self.main_area = tk.Frame(self, bg="white")

        self.caja_imagen = CajaDeImagen(self.main_area, width=550, height=500)

        self.sidebar_container = tk.Frame(self, bg="white", width=150)
        self.barra_actividades = BarraDeActividades(self, self.main_area)

        # --- Empaquetar en el orden visual deseado ---
        self.barra_actividades.pack(side="left", fill="y")     # primero (más a la izquierda)
        self.sidebar_container.pack(side="left", fill="y")     # segundo
        self.main_area.pack(side="left", fill="both", expand=True)  # tercero (a la derecha)

        # Empaquetar la caja de imagen dentro del área principal
        self.caja_imagen.pack(fill="both", expand=True)


    

