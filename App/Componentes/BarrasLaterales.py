import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import filedialog
import numpy as np


class BarraLateralBase(tk.Frame):
    """Base para las barras laterales."""
    def __init__(self, master, **kwargs):
        super().__init__(master, bg="lightgray", width=150, **kwargs)
        self.pack_propagate(False)  # evita que se achique al mínimo

class BarraLateralArchivos(tk.Frame):
    """
    No estoy seguro de como funciona
    
    """
    def __init__(self, master, caja_imagen, **kwargs):
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
            elif nombre.lower().endswith((".png",".jpg",".jpeg")):
                self.tree.insert(padre, "end", text=nombre, values=(path,))

    def on_doble_click(self, event):
        item_id = self.tree.selection()[0]
        vals = self.tree.item(item_id, "values")
        if not vals:
            return  # sin ruta, nada que hacer
        path = vals[0]

        if os.path.isdir(path):
            # Es una carpeta: expandirla mostrando su contenido real
            # (limpia el hijo "dummy" si existe y evita reusar la ruta raíz)
            for child in self.tree.get_children(item_id):
                self.tree.delete(child)
            self.insertar_items(item_id, path)
            self.tree.item(item_id, open=True)
        else:
            # Es un archivo: abrir en el visor
            self.caja_imagen.mostrar_imagen(path)


    #dejo esta seccion comentada por las dudas, la de arriba abre subcarpetas
    """def insertar_items(self, padre, ruta): 
        #Inserta carpetas e imágenes en el Treeview
        for elemento in os.listdir(ruta):
            path_completo = os.path.join(ruta, elemento)
            if os.path.isdir(path_completo):
                id_item = self.tree.insert(padre, "end", text=elemento, open=False)
                # Insertar contenido de forma lazy (solo carpeta)
                self.tree.insert(id_item, "end")  # nodo vacío para que se pueda expandir
            elif elemento.lower().endswith((".png", ".jpg", ".jpeg")):
                self.tree.insert(padre, "end", text=elemento, values=(path_completo,))

    def on_doble_click(self, event):
        item_id = self.tree.selection()[0]
        path = self.tree.item(item_id, "values")
        if path:
            # Es un archivo de imagen
            self.caja_imagen.mostrar_imagen(path[0])
        else:
            # Es una carpeta, expandir/colapsar
            if self.tree.get_children(item_id):
                # Ya tiene hijos cargados, expandir
                if self.tree.item(item_id, "open"):
                    self.tree.item(item_id, open=False)
                else:
                    self.tree.item(item_id, open=True)
            else:
                # Insertar contenido
                ruta_carpeta = os.path.join(self.ruta_raiz, self.tree.item(item_id, "text"))
                self.insertar_items(item_id, ruta_carpeta)
                self.tree.item(item_id, open=True)
    """

class BarraLateralImagenes(BarraLateralBase):
    def __init__(self, master, caja_imagen, **kwargs):
        super().__init__(master, **kwargs)
        self.caja = caja_imagen

        tk.Label(self, text="Luminancia (a)").pack(pady=4)
        self.var_a = tk.DoubleVar(value=1.0)
        tk.Scale(self, from_=0.0, to=2.0, resolution=0.05, orient="horizontal",
                 variable=self.var_a,
                 command=lambda _ : self.caja.aplicar_yiq(self.var_a.get(), self.var_b.get())
        ).pack(fill="x", padx=8)

        tk.Label(self, text="Saturación (b)").pack(pady=4)
        self.var_b = tk.DoubleVar(value=1.0)
        tk.Scale(self, from_=0.0, to=2.0, resolution=0.05, orient="horizontal",
                 variable=self.var_b,
                 command=lambda _ : self.caja.aplicar_yiq(self.var_a.get(), self.var_b.get())
        ).pack(fill="x", padx=8)

        # Botón para resetear (a=1, b=1)
        tk.Button(self, text="Reiniciar (a=1, b=1)",
                  command=lambda: (self.var_a.set(1.0), self.var_b.set(1.0),
                                   self.caja.aplicar_yiq(1.0, 1.0))
        ).pack(pady=8)

"""
class BarraLateralImagenes(BarraLateralBase):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        tk.Label(self, text="Herramientas de imágenes").pack(pady=10)
        tk.Button(self, text="Redimensionar").pack(pady=5)
        tk.Button(self, text="Rotar").pack(pady=5)
"""
class BarraLateralGuardado(BarraLateralBase):

    def __init__(self, master,imagen, **kwargs): #trae el objeto CajaImagen, es necesario
        super().__init__(master, **kwargs)
        tk.Label(self, text="Opciones de Guardado").pack(pady=10)
        tk.Button(self, text="Guardar", command=lambda: self.guardar(getattr(imagen, "_imagen_procesada", None) or imagen.imagen)).pack(pady=5)

    def guardar(self, img):
        if img is None: #agregado para evitar errores
            tk.messagebox.showwarning("Atención", "No hay imagen para guardar.")
            return
        # Copiado de internet, funciona
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("Todos los archivos", "*.*")]
        )
        if file_path: 
            img.save(file_path)

class BarraLateralConfiguracion(BarraLateralBase):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        tk.Label(self, text="Configuración").pack(pady=10)
        tk.Checkbutton(self, text="Opción 1").pack()
        tk.Checkbutton(self, text="Opción 2").pack()
