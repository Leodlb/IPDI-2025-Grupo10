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
from Componentes.PanelesDeEdicion.Panel_Procesamiento_por_convolucion import *


class BarraLateralImagenes(BarraLateralBase):
    def __init__(self, master, main_area, caja_imagen: CajaDeImagen, **kwargs):
        super().__init__(master, **kwargs)
        self.main_area = main_area
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

        # Botón para resetear
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
            "Línea cromática horizontal",
            "Punto cromático",
            "Cuasi-operaciones"
        ]
        variable_seleccionada = tk.StringVar(self)
        variable_seleccionada.set(opciones[0]) 
        
        menu = tk.OptionMenu(self, variable_seleccionada, *opciones, command=self.accion)
        menu.pack(padx=10, pady=10)

        tk.Button(self, text="Filtros luminancia",
                  command= self.pdefdf
        ).pack(pady=8)
        tk.Button(self, text="Convolucion",
                  command= self.pdefdf2
        ).pack(pady=8)

    def pdefdf2(self):
        self.caja.forget()
        PanelDeEdicionConvoluciones(self.main_area, self.caja).pack(expand=True, fill="both")
        return


    def pdefdf(self):
        self.caja.forget()
        PanelDeEdicionFiltrosDeFunciones(self.main_area, self.caja).pack(expand=True, fill="both")
        return


    def accion(self, seleccion):
        if self.bandera_primera_modificacion:
            self.imagen_original = self.caja.imagen.copy()
            self.bandera_primera_modificacion = False
        else:
            self.caja.imagen = self.imagen_original

        if seleccion == "Cuasi-operaciones":
            self.caja.forget()
            Ap = Apixeles(self.main_area, self.caja)
            Ap.pack(expand=True, fill="both")
            return

        elif(seleccion == "Solo Green"):
            arr = np.asarray(self.caja.imagen.convert("RGB"), dtype=np.int32)
            arr = solo_verde(arr)
            self.caja._imagen_procesada = Image.fromarray(arr.astype("uint8"))
            self.caja._render_image()

        elif(seleccion == "Solo Blue"):
            arr = np.asarray(self.caja.imagen.convert("RGB"), dtype=np.int32)
            arr = solo_azul(arr)
            self.caja._imagen_procesada = Image.fromarray(arr.astype("uint8"))
            self.caja._render_image()

        elif(seleccion == "Solo Red"):
            arr = np.asarray(self.caja.imagen.convert("RGB"), dtype=np.int32)
            arr = solo_rojo(arr)
            self.caja._imagen_procesada = Image.fromarray(arr.astype("uint8"))
            self.caja._render_image()

        elif(seleccion == "En Gris"):
            arr = np.asarray(self.caja.imagen.convert("RGB"), dtype=np.int32)
            arr = gris(arr)
            self.caja._imagen_procesada = Image.fromarray(arr.astype("uint8"))
            self.caja._render_image()

        elif seleccion == "Línea cromática horizontal":
            top = tk.Toplevel(self)
            top.title("Elegir valor de Y")

            tk.Label(top, text="Ingrese valor de Y:").pack(pady=5)
            var_y = tk.IntVar(value=0)
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

