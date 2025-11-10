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


class BarraLateralArchivos(tk.Frame):
    """
    Barra lateral de archivos.
    """
    def __init__(self, master, caja_imagen : CajaDeImagen, **kwargs):
        super().__init__(master, bg="lightgray", width=250, **kwargs)
        self.caja_imagen = caja_imagen
        self.pack_propagate(False)

        # Botón para seleccionar carpeta raíz
        tk.Button(self, text="Seleccionar carpeta", command=self.cargar_carpeta).pack(pady=5)

        # Treeview para mostrar carpetas/archivos
        self.tree = ttk.Treeview(self)
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<Double-1>", self.on_doble_click)

        # Guardar ruta raíz
        self.ruta_raiz = ""

    def cargar_carpeta(self):
        carpeta = filedialog.askdirectory()
        if not carpeta:
            return
        self.ruta_raiz = carpeta
        self.tree.delete(*self.tree.get_children())
        self.insertar_items("", carpeta)

    def insertar_items(self, padre, ruta):
        for nombre in os.listdir(ruta):
            path = os.path.join(ruta, nombre)
            if os.path.isdir(path):
                id_item = self.tree.insert(padre, "end", text=nombre, values=(path,), open=False)
                self.tree.insert(id_item, "end")
            elif nombre.lower().endswith((".png", ".jpg", ".jpeg", ".bmp")):
                self.tree.insert(padre, "end", text=nombre, values=(path,))

    def on_doble_click(self, event):
        item_id = self.tree.selection()[0]
        vals = self.tree.item(item_id, "values")
        if not vals:
            return  # sin ruta, nada que hacer
        path = vals[0]

        if os.path.isdir(path):
            for child in self.tree.get_children(item_id):
                self.tree.delete(child)
            self.insertar_items(item_id, path)
            self.tree.item(item_id, open=True)
        else:
            self.caja_imagen.mostrar_imagen(path)