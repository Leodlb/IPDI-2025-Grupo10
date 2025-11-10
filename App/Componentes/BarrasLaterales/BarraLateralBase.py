import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import filedialog
from tkinter import messagebox
import numpy as np
from Componentes.PanelesDeEdicion.CajaImagen import CajaDeImagen
from Herramientas.Helper_img import linea_cromatica_Y
from Herramientas.Helper_img import *
from Componentes.PanelesDeEdicion.Panel_tp2_aritmetica_de_pixeles import PanelDeEdicionArimeticaDePixeles as Apixeles
from Componentes.PanelesDeEdicion.Panel_tp3_filtros_luminancia import *


class BarraLateralBase(tk.Frame):
    """Base para las barras laterales."""
    def __init__(self, master, **kwargs):
        super().__init__(master, bg="lightgray", width=150, **kwargs)
        self.pack_propagate(False)


class BarrasLaterales(BarraLateralBase):
    def __init__(self, master, caja_imagen: CajaDeImagen, **kwargs):
        super().__init__(master, **kwargs)
    
   