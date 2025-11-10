import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import filedialog
from tkinter import messagebox
import numpy as np
from Componentes.PanelesDeEdicion.CajaImagen import CajaDeImagen
from Componentes.BarrasLaterales.BarraLateralBase import BarraLateralBase
from Herramientas.Helper_img import linea_cromatica_Y
from Herramientas.Helper_img import *
from Componentes.PanelesDeEdicion.Panel_tp2_aritmetica_de_pixeles import PanelDeEdicionArimeticaDePixeles as Apixeles
from Componentes.PanelesDeEdicion.Panel_tp3_filtros_luminancia import *



class BarraLateralConfiguracion(BarraLateralBase):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        tk.Label(self, text="Configuración").pack(pady=10)
        tk.Checkbutton(self, text="Opción 1").pack()
