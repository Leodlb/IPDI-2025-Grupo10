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




class BarraLateralGuardado(BarraLateralBase):

    def __init__(self, master,imagen, **kwargs):
        super().__init__(master, **kwargs)
        tk.Label(self, text="Opciones de Guardado").pack(pady=10)
        tk.Button(self, text="Guardar", command=lambda: self.guardar(getattr(imagen, "_imagen_procesada", None) or imagen.imagen)).pack(pady=5)

    def guardar(self, img):
        if img is None:
            tk.messagebox.showwarning("Atención", "No hay imagen para guardar.")
            return
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("Todos los archivos", "*.*")]
        )
        if file_path: 
            img.save(file_path)