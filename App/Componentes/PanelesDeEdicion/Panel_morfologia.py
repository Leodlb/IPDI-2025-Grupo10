import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import numpy as np

from Componentes.PanelesDeEdicion.Panel_De_Edicion_Base import PanelEdicionBase

class PanelMorfologia(PanelEdicionBase):

    def __init__(self, master, imagen_inicial: Image.Image = None, **kwargs):
        super().__init__(master, titulo="Panel de Morfología", **kwargs)

        self.imgA = imagen_inicial
        self.resultado = None

        self.modos = []   # <- completar después
        self.var_modo = tk.StringVar(value=self.modos[0] if self.modos else "")

        tk.Label(self.body, text="Seleccione operación morfológica:").pack(pady=5)

        self.selector = tk.OptionMenu(
            self.body,
            self.var_modo,
            *self.modos  # actualmente vacío
        )
        self.selector.pack(pady=5)

        # Área de imágenes
        self.labelA = self._crear_label_imagen(self.body, "Imagen A")
        self.labelR = self._crear_label_imagen(self.body, "Resultado")

        if self.imgA:
            self._render_label(self.labelA, self.imgA)

        # Botón carga
        tk.Button(self.body, text="Cargar Imagen", command=self.cargar_imgA).pack(pady=5)


    def procesar(self):
        if self.imgA is None:
            messagebox.showwarning("Atención", "Debes cargar una imagen primero.")
            return None

        modo = self.var_modo.get()
        if modo == "":
            messagebox.showwarning("Atención", "Todavía no hay operaciones morfológicas cargadas.")
            return None

        messagebox.showinfo(
            "Aviso",
            f"No hay operaciones implementadas todavía.\nModo seleccionado: {modo}"
        )
        return None

 
    def cargar_imgA(self):
        ruta = filedialog.askopenfilename(
            filetypes=[("Imágenes", "*.png;*.bmp;*.jpg;*.jpeg")]
        )
        if ruta:
            self.imgA = Image.open(ruta).convert("RGB")
            self._render_label(self.labelA, self.imgA)
