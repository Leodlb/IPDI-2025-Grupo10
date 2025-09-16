import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import filedialog
import numpy as np


class CajaDeImagen(tk.Frame):
    """
    Con esta clase se interactuara con la imagen, contiene la imagen
    Deberia agregar los metodos para modificar las imagenes aca
    Seria mas recomendable hacer eso en otra clase, principio de responsabilidad
    pero como quedaria muy vacia, se usa preferentemente esta.
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.label = tk.Label(self, bg="white")
        self.label.pack(expand=True, fill="both")

        self.imagen = None   # original PIL.Image
        self.foto = None     # PhotoImage actual

        # Vincular evento de cambio de tamaño
        self.bind("<Configure>", self._on_resize)
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.label = tk.Label(self, bg="white")
        self.label.pack(expand=True, fill="both")

        self.imgA = None   # primera imagen
        self.imgB = None   # segunda imagen
        self.imagen = None  # 🔹 inicializamos acá
        self._imagen_procesada = None
        self.foto = None

        self.bind("<Configure>", self._on_resize)

    def mostrar_imagen(self, ruta_imagen=None):
        if ruta_imagen:
            nueva = Image.open(ruta_imagen).convert("RGB")

            if self.imgA is None:
                # primera imagen
                self.imgA = nueva
                self.imagen = self.imgA
            elif self.imgB is None:
                # segunda imagen, se guarda pero NO se muestra
                self.imgB = nueva
                # seguimos mostrando la A
                self.imagen = self.imgA
            else:
                # si ya hay 2 imágenes cargadas, reemplazamos la B
                self.imgB = nueva
                self.imagen = self.imgA

            self._imagen_procesada = None  

        if not hasattr(self, "imagen") or self.imagen is None:
            return
        self._render_image()

    def obtener_arrays(self):
        """Devuelve imgA y imgB como arrays numpy, si existen."""
        if self.imgA is None or self.imgB is None:
            return None, None
        arrA = np.asarray(self.imgA, dtype=np.uint8)
        arrB = np.asarray(self.imgB, dtype=np.uint8)
        return arrA, arrB

    def _on_resize(self, event):
        if self.imagen:
            self._render_image()

    def _render_image(self):
        img = self._imagen_actual_para_render()
        if img is None:
            return
        self.update_idletasks()
        ancho_max = max(self.winfo_width(), 1)
        alto_max  = max(self.winfo_height(), 1)
        """
        im = img.copy()
        im.thumbnail((ancho_max, alto_max))
        self.foto = ImageTk.PhotoImage(im)
        self.label.config(image=self.foto, anchor="center")
        self.label.image = self.foto
        """
         # mantener proporción
        w, h = img.size
        ratio = min(ancho_max / w, alto_max / h)
        new_size = (int(w * ratio *0.8), int(h * ratio*0.8))

        im = img.resize(new_size, Image.LANCZOS)

        self.foto = ImageTk.PhotoImage(im)
        self.label.config(image=self.foto, anchor="center")
        self.label.image = self.foto

    def aplicar_yiq(self, a=1.0, b=1.0):
        """Aplica Y' = aY, I' = bI, Q' = bQ sobre la imagen original y vuelve a mostrar."""
        if not hasattr(self, "imagen") or self.imagen is None:
            return

        arr = np.asarray(self.imagen.convert("RGB"), dtype=np.float32) / 255.0
        H, W, _ = arr.shape

        # RGB -> YIQ
        M_fwd = np.array([
            [0.299000,  0.587000,  0.114000],      # Y
            [0.595716, -0.274453, -0.321263],      # I
            [0.211456, -0.522591,  0.311135],      # Q
        ], dtype=np.float32)
        yiq = arr.reshape(-1,3) @ M_fwd.T

        # Escalado
        Y = yiq[:,0] * a
        I = yiq[:,1] * b
        Q = yiq[:,2] * b

        # Rangos (slides): Y<=1 ; I,Q acotados
        Y = np.clip(Y, 0.0, 1.0)
        I = np.clip(I, -0.5957, 0.5957)
        Q = np.clip(Q, -0.5226, 0.5226)

        yiq2 = np.stack([Y,I,Q], axis=1)

        # YIQ -> RGB
        M_inv = np.array([
            [1.000000,  0.956300,  0.621000],
            [1.000000, -0.272100, -0.647400],
            [1.000000, -1.106000,  1.703000],
        ], dtype=np.float32)
        rgb = (yiq2 @ M_inv.T).reshape(H,W,3)
        rgb = np.clip(rgb, 0.0, 1.0)

        # Guardamos la imagen procesada y la mostramos redimensionada al frame
        self._imagen_procesada = Image.fromarray((rgb*255).astype("uint8"))
        self._render_image()  # reusa tu resize/centrado



    def _imagen_actual_para_render(self):
        """Devuelve la imagen que debe renderizarse (procesada si existe, si no la original)."""
        if hasattr(self, "_imagen_procesada") and self._imagen_procesada is not None:
            return self._imagen_procesada
        return getattr(self, "imagen", None)
