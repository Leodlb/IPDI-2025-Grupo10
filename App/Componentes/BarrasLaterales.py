import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import filedialog
import numpy as np
from Componentes.CajaImagen import CajaDeImagen
from Herramientas.Helper_img import linea_cromatica_Y
from Herramientas.Helper_img import *

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


class BarraLateralImagenes(BarraLateralBase):

    
    def __init__(self, master, caja_imagen: CajaDeImagen, **kwargs):
        super().__init__(master, **kwargs)
        self.caja = caja_imagen
        self.bandera_primera_modificacion = True
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


        
         # Crear un menú desplegable
        tk.Label(self, text="Opciones de imagen").pack(pady=4)
        opciones = [
        "ninguna",
        "Solo Red",
        "Solo Green",
        "Solo Blue",
        "En Gris",
        "línea cromática X",
        "Línea cromática horizontal",
        "Punto cromático"
        ]
        variable_seleccionada = tk.StringVar(self)
        variable_seleccionada.set(opciones[0]) # Establece un valor inicial
        
        menu = tk.OptionMenu(self, variable_seleccionada, *opciones, command=self.accion)
        menu.pack(padx=10, pady=10)

    def accion(self, seleccion):
        if(self.bandera_primera_modificacion):
            self.imagen_original = self.caja.imagen.copy()
            self.bandera_primera_modificacion = False
        else:
            self.caja.imagen = self.imagen_original
        if seleccion == "Línea cromática horizontal":
            # Crear ventanita emergente
            top = tk.Toplevel(self)
            top.title("Elegir valor de Y")

            tk.Label(top, text="Ingrese valor de Y:").pack(pady=5)

            var_y = tk.IntVar(value=0)  # valor inicial

            entry = tk.Entry(top, textvariable=var_y)
            entry.pack(pady=5)

            def aplicar():
                y = var_y.get()
                guarda_imagen = self.caja.imagen.copy()
                arr = np.asarray(self.caja.imagen.convert("RGB"), dtype=np.int32)
                arr2 = arr.copy()
                arr2[y, :, :] = 0
                self.caja.imagen = Image.fromarray((arr2).astype("uint8"))
                self.caja._render_image()  
                linea_cromatica_Y(arr, y)

                self.caja.imagen = guarda_imagen
                self.caja._render_image()
                top.destroy()

            tk.Button(top, text="Aceptar", command=aplicar).pack(pady=10)
        
        elif(seleccion == "Solo Green"):

            print("green")
            arr = np.asarray(self.caja.imagen.convert("RGB"), dtype=np.int32)
            arr = solo_verde(arr)
            self.caja.imagen = Image.fromarray((arr).astype("uint8"))
            self.caja._render_image()

        elif(seleccion == "Solo Blue"):
            print("green")
            arr = np.asarray(self.caja.imagen.convert("RGB"), dtype=np.int32)
            arr = solo_azul(arr)
            self.caja.imagen = Image.fromarray((arr).astype("uint8"))
            self.caja._render_image()
        
        elif(seleccion == "Solo Red"):
            print("green")
            arr = np.asarray(self.caja.imagen.convert("RGB"), dtype=np.int32)
            arr = solo_rojo(arr)
            self.caja.imagen = Image.fromarray((arr).astype("uint8"))
            self.caja._render_image()
        
        elif(seleccion == "En Gris"):
            print("green")
            arr = np.asarray(self.caja.imagen.convert("RGB"), dtype=np.int32)
            arr = gris(arr)
            self.caja.imagen = Image.fromarray((arr).astype("uint8"))
            self.caja._render_image()





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
