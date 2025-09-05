import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import filedialog
import numpy as np


class BarraDeActividades(tk.Frame):
    """
    Cambia de Barra laterales. 
    Para futuros cambios agregar metodos como "guardar"
    Y "guardar Como"
    Se aceptan sujerencias sobre imagen o stiker que deberia contener los botones
    """
    def __init__(self, master, ventana, **kwargs):
        super().__init__(master, bg="darkgray", width=45, **kwargs)
        self.ventana = ventana
        self.pack_propagate(False)

        tk.Button(self, text="📂", command=lambda: ventana.mostrar_sidebar("archivos")).pack(ipady=7, ipadx=7)
        tk.Button(self, text="📝", command=lambda: ventana.mostrar_sidebar("imagenes")).pack(ipady=7, ipadx=7)
        tk.Button(self, text="⚙️", command=lambda: ventana.mostrar_sidebar("config")).pack(ipady=6, ipadx=6) #clave corregida
        tk.Button(self, text="💾", command=lambda: ventana.mostrar_sidebar("guardar")).pack(ipady=7, ipadx=7)
