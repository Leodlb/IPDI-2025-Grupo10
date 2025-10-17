import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
from Herramientas.Helper_img import *
from Componentes.PanelDeEdicionSimple import *
from Componentes.CajaImagen import *

class PanelDeEdicionArimeticaDePixeles(tk.Frame):
    def __init__(self, master, panelDeEdicionSimple: CajaDeImagen, **kwargs):
        super().__init__(master, **kwargs)
        self.panelSimple = panelDeEdicionSimple
        self.imgA = panelDeEdicionSimple.imagen
        self.imgB = None
        self.resultado = None

        # --- Modo de combinación ---
        modos = [
            "Cuasi-suma RGB clampeada",
            "Cuasi-suma RGB promediada",
            "Cuasi-resta RGB clampeada",
            "Cuasi-resta RGB promediada",
            "Cuasi-suma YIQ clampeada",
            "Cuasi-suma YIQ promediada",
            "Cuasi-resta YIQ clampeada",
            "Cuasi-resta YIQ promediada",
            "Producto RGB",
            "Cociente RGB",
            "Resta absoluta RGB",
            "If-darker",
            "If-lighter",
        ]
        self.var_cuasi = tk.StringVar(value=modos[0])

        tk.Label(self, text="Modo de combinación:").grid(row=0, column=0, pady=5)
        opciones = tk.OptionMenu(self, self.var_cuasi, *modos)
        opciones.grid(row=1, column=0, pady=5, sticky="ew")

        # --- Modo de igualación de tamaño ---
        self.var_tamano = tk.StringVar(value="Redimensionar al tamaño más grande")
        modos_tamano = [
            "Usar formato manual",
            "Redimensionar al tamaño más grande",
            "Redimensionar al tamaño más pequeño",
            "Recortar al tamaño común (mínimo)"
        ]
        tk.Label(self, text="Ajuste de tamaño:").grid(row=0, column=1, pady=5)
        opciones_tamano = tk.OptionMenu(self, self.var_tamano, *modos_tamano)
        opciones_tamano.grid(row=1, column=1, pady=5, sticky="ew")

        # --- Labels de imágenes ---
        self.labelA = tk.Label(self, bg="lightgray", text="Imagen A", width=40, height=15)
        self.labelA.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

        self.labelB = tk.Label(self, bg="lightgray", text="Imagen B", width=40, height=15)
        self.labelB.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)

        self.labelR = tk.Label(self, bg="lightgray", text="Resultado", width=40, height=15)
        self.labelR.grid(row=2, column=2, sticky="nsew", padx=5, pady=5)

        self._render_label(self.labelA, self.imgA)

        # --- Botones ---
        tk.Button(self, text="Cargar Imagen A", command=self.cargar_imgA).grid(row=3, column=0, pady=5)
        tk.Button(self, text="Cargar Imagen B", command=self.cargar_imgB).grid(row=3, column=1, pady=5)
        tk.Button(self, text="Combinar", command=self.combinar_cuasi).grid(row=3, column=2, pady=5)
        tk.Button(self, text="Guardar resultado", command=self.guardar_resultado).grid(row=4, column=1, pady=5)
        tk.Button(self, text="Salir", command=self.salir).grid(row=4, column=2, pady=5)

        for c in range(3):
            self.grid_columnconfigure(c, weight=1)
            self.grid_rowconfigure(2, weight=1)

    # --- Métodos de carga de imágenes ---
    def cargar_imgA(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar Imagen A",
            filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg;*.bmp")]
        )
        if not ruta:
            return
        self.imgA = Image.open(ruta).convert("RGB")
        self._render_label(self.labelA, self.imgA)

    def cargar_imgB(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar Imagen B",
            filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg;*.bmp")]
        )
        if not ruta:
            return
        self.imgB = Image.open(ruta).convert("RGB")
        self._render_label(self.labelB, self.imgB)

    # --- Guardar resultado ---
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

    # --- Salir del panel ---
    def salir(self):
        self.destroy()

    def _render_label(self, label, img):
        if img is None:
            label.config(image="", text="(sin imagen)")
            return

        # (6 cm x 9 cm) 
        max_w, max_h = 227, 340
        w, h = img.size
        scale = min(max_w / w, max_h / h, 1.0)  # solo reduce, no agranda
        if scale < 1.0:
            new_size = (int(w * scale), int(h * scale))
            img = img.resize(new_size, Image.LANCZOS)

        tk_img = ImageTk.PhotoImage(img)
        label.config(image=tk_img, text="")
        label.image = tk_img  # evita que el GC la elimine

    # --- Combinar imágenes ---
    def combinar_cuasi(self):
        if self.imgA is None or self.imgB is None:
            messagebox.showwarning("Atención", "Debes cargar las dos imágenes.")
            return

        modo_tam = self.var_tamano.get()
        imgA, imgB = self.imgA.copy(), self.imgB.copy()

        # --- Ajuste de tamaño ---
        if modo_tam != "Usar formato manual":
            wA, hA = imgA.size
            wB, hB = imgB.size
            if modo_tam == "Redimensionar al tamaño más grande":
                new_size = (max(wA, wB), max(hA, hB))
            elif modo_tam == "Redimensionar al tamaño más pequeño":
                new_size = (min(wA, wB), min(hA, hB))
            elif modo_tam == "Recortar al tamaño común (mínimo)":
                min_w, min_h = min(wA, wB), min(hA, hB)
                imgA = self._crop_center(imgA, min_w, min_h)
                imgB = self._crop_center(imgB, min_w, min_h)
                new_size = None
            if new_size:
                imgA = imgA.resize(new_size, Image.LANCZOS)
                imgB = imgB.resize(new_size, Image.LANCZOS)

        arrA = np.asarray(imgA, dtype=np.uint8)
        arrB = np.asarray(imgB, dtype=np.uint8)
        modo = self.var_cuasi.get()

        # --- Operaciones ---
        if modo == "Cuasi-suma RGB clampeada":
            arr = cuasi_suma_rgb_clampeada(arrA, arrB)
        elif modo == "Cuasi-suma RGB promediada":
            arr = cuasi_suma_rgb_promediada(arrA, arrB)
        elif modo == "Cuasi-resta RGB clampeada":
            arr = cuasi_resta_rgb_clampeada(arrA, arrB)
        elif modo == "Cuasi-resta RGB promediada":
            arr = cuasi_resta_rgb_promediada(arrA, arrB)
        elif modo == "Cuasi-suma YIQ clampeada":
            arr = cuasi_suma_yiq_clampeada(arrA, arrB)
        elif modo == "Cuasi-suma YIQ promediada":
            arr = cuasi_suma_yiq_promediada(arrA, arrB)
        elif modo == "Cuasi-resta YIQ clampeada":
            arr = cuasi_resta_yiq_clampeada(arrA, arrB)
        elif modo == "Cuasi-resta YIQ promediada":
            arr = cuasi_resta_yiq_promediada(arrA, arrB)
        elif modo == "Producto RGB":
            arr = producto_rgb(arrA, arrB)
        elif modo == "Cociente RGB":
            arr = cociente_rgb(arrA, arrB)
        elif modo == "Resta absoluta RGB":
            arr = resta_absoluta_rgb(arrA, arrB)
        elif modo == "If-darker":
            arr = if_darker(arrA, arrB)
        elif modo == "If-lighter":
            arr = if_lighter(arrA, arrB)
        else:
            messagebox.showwarning("Atención", "Modo no reconocido.")
            return

        self.resultado = Image.fromarray(arr)
        self._render_label(self.labelR, self.resultado)

    # --- Recorte central ---
    def _crop_center(self, img, w, h):
        W, H = img.size
        left = (W - w) // 2
        top = (H - h) // 2
        right = left + w
        bottom = top + h
        return img.crop((left, top, right, bottom))
