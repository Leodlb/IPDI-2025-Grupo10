import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import filedialog

class Ventana:
    def __init__(self, root):
        self.indice = 0
        self.root = root
        root.geometry("500x300")
        self.root.title("Visor de Imágenes")
        
        self.label = ttk.Label(self.root)
        self.label.pack(pady=10)

        # --- Frame para los botones ---
        frame_botones = ttk.Frame(self.root)
        frame_botones.pack(pady=10)

        ttk.Button(frame_botones, text="Anterior", command=self.anterior).pack(side="left", padx=5)
        ttk.Button(frame_botones, text="Cargar", command=self.mostrar_imagen).pack(side="left", padx=5)
        ttk.Button(frame_botones, text="Siguiente", command=self.siguiente).pack(side="left", padx=5)

        self.imagenes_de_mi_carpeta = []  

    def siguiente(self):
        if self.imagenes_de_mi_carpeta:
            self.indice = (self.indice + 1) % len(self.imagenes_de_mi_carpeta)
            self.mostrar_imagen()

    def anterior(self):
        if self.imagenes_de_mi_carpeta:
            self.indice = (self.indice - 1) % len(self.imagenes_de_mi_carpeta)
            self.mostrar_imagen()
        
    def buscarImagenes(self):
        carpeta = self.seleccionar_carpeta()
        if not carpeta:
            return []
        imagenesLista = []
        for elemento in os.listdir(carpeta):
            if elemento.lower().endswith((".png", ".jpg", ".jpeg")):
                imagenesLista.append(os.path.join(carpeta, elemento))
        return imagenesLista

    def mostrar_imagen(self):
        if not self.imagenes_de_mi_carpeta:
            self.imagenes_de_mi_carpeta = self.buscarImagenes()
            self.indice = 0
        if self.imagenes_de_mi_carpeta:
            imagen_original = Image.open(self.imagenes_de_mi_carpeta[self.indice])
            imagen_redimensionada = imagen_original.resize((300, 200))
            self.image = ImageTk.PhotoImage(imagen_redimensionada)
            self.label.config(image=self.image)
            self.label.image = self.image 

    def seleccionar_carpeta(self):
        return filedialog.askdirectory()


    def seleccionar_carpeta(self):
        carpeta = filedialog.askdirectory()  
        if carpeta:
            return(carpeta)






if __name__ == "__main__":
    root = tk.Tk()
    app = Ventana(root)
    root.mainloop()

