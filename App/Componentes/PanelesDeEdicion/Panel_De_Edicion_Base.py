import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from abc import ABC, abstractmethod
import numpy as np
"""
Se supone que en esta clase deberia estar el corazon de todos los metoods
pero aun no estoy convencido del todo de usarlo
O reemplazar el codigo preexistente
Por el momento sera una ayuda y no se modificara codigo anterior
solo para implementar esto.
"""

class PanelEdicionBase(tk.Frame, ABC):
    """
    Clase base para paneles de edición o análisis de imágenes.
    Define una estructura gráfica común y utilidades compartidas.
    """

    def __init__(self, master, titulo="Panel de edición", **kwargs):
        super().__init__(master, **kwargs)
        self.titulo = titulo

        # Contenedores principales
        self.header = tk.Frame(self)
        self.header.pack(fill="x", pady=5)

        self.body = tk.Frame(self)
        self.body.pack(expand=True, fill="both", pady=5)

        self.footer = tk.Frame(self)
        self.footer.pack(fill="x", pady=5)

        # Elementos comunes
        tk.Label(self.header, text=titulo, font=("Arial", 14, "bold")).pack(side="left", padx=10)

        self.boton_ejecutar = tk.Button(self.footer, text="Ejecutar", command=self._on_ejecutar)
        self.boton_ejecutar.pack(side="right", padx=5)

        self.boton_guardar = tk.Button(self.footer, text="Guardar resultado", command=self.guardar_resultado)
        self.boton_guardar.pack(side="right", padx=5)

        self.boton_salir = tk.Button(self.footer, text="Salir", command=self.destroy)
        self.boton_salir.pack(side="left", padx=5)

        # Donde las subclases colocan sus elementos gráficos
        self.areas_imagen = []
        self.resultado = None


    # --- Botones comunes ---
    def _on_ejecutar(self):
        try:
            self.resultado = self.procesar()
            if isinstance(self.resultado, Image.Image):
                self._mostrar_resultado(self.resultado)
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al procesar:\n{e}")

    def guardar_resultado(self):
        if self.resultado is None:
            messagebox.showwarning("Atención", "No hay resultado para guardar.")
            return
        ruta = filedialog.asksaveasfilename(
            title="Guardar resultado",
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("BMP", "*.bmp")]
        )
        if ruta:
            self.resultado.save(ruta)
            messagebox.showinfo("Éxito", f"Imagen guardada en:\n{ruta}")

    # --- Métodos utilitarios comunes ---
    def _crear_label_imagen(self, parent, titulo="Imagen", ancho=250, alto=250):
        """Crea un label listo para mostrar imágenes y devuelve (frame, label)."""
        frame = tk.Frame(parent)
        frame.pack(side="left", expand=True, fill="both", padx=5, pady=5)

        tk.Label(frame, text=titulo).pack()
        label = tk.Label(frame, bg="lightgray", width=ancho, height=alto)
        label.pack(expand=True, fill="both")

        self.areas_imagen.append(label)
        return label

    def _render_label(self, label, img: Image.Image, max_w=300, max_h=300):
        """Muestra una imagen dentro de un label sin deformarla."""
        if img is None:
            label.config(image="", text="(sin imagen)")
            return
        w, h = img.size
        scale = min(max_w / w, max_h / h, 1.0)
        if scale < 1.0:
            img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
        tk_img = ImageTk.PhotoImage(img)
        label.config(image=tk_img, text="")
        label.image = tk_img  # evitar recolección de basura

    def _crop_center(self, img, w, h):
        W, H = img.size
        left, top = (W - w) // 2, (H - h) // 2
        return img.crop((left, top, left + w, top + h))

    def _mostrar_resultado(self, img):
        """Si el panel tiene un label para el resultado, se muestra ahí."""
        if len(self.areas_imagen) >= 1:
            self._render_label(self.areas_imagen[-1], img)
