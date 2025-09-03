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
    Esto lo hizo la IA, no se muy bien como funciona.
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
        """Inserta carpetas e imágenes en el Treeview"""
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

class BarraLateralImagenes(BarraLateralBase):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        tk.Label(self, text="Herramientas de imágenes").pack(pady=10)
        tk.Button(self, text="Redimensionar").pack(pady=5)
        tk.Button(self, text="Rotar").pack(pady=5)

class BarraLateralGuardado(BarraLateralBase):

    def __init__(self, master,imagen, **kwargs): #trae el objeto CajaImagen, es necesario
        super().__init__(master, **kwargs)
        tk.Label(self, text="Opciones de Guardado").pack(pady=10)
        tk.Button(self, text="Guardar", command=lambda: self.guardar(imagen.imagen)).pack(pady=5)

    def guardar(self, img):
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
        tk.Button(self, text="⚙️", command=lambda: ventana.mostrar_sidebar("configuracion")).pack(ipady=6, ipadx=6)
        tk.Button(self, text="💾", command=lambda: ventana.mostrar_sidebar("guardar")).pack(ipady=7, ipadx=7)



class CajaDeImagen(tk.Frame):
    """
    Con esta clase se interactuara con la imagen, contiene la imagen
    Deberia agregar los metodos para modificar las imagenes aca
    Seria mas recomendable hacer eso en otra clase, principio de responsabilidad
    pero como quedaria muy vacia, se usa preferentemente esta.
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, bg="white", **kwargs)
        self.pack_propagate(False)
        self.label = tk.Label(self, bg="white")
        self.label.pack(expand=True)


    
    def mostrar_imagen(self, ruta_imagen=None):
        """
        importante, al cargar la imagen por primera vez se va a crear un objeto imagen
        al volver a interactuar con la funcion si la ruta imagen es nula y no se ingresa
        entonces esta variable no se sobreescribira.
        Lo que hara es interactuar con la imagen previamente escrita.
        """
        if ruta_imagen:   # cuando no esta cargada la imagen lo cambia
            
            self.imagen = Image.open(ruta_imagen) #esto es mportante, al cargar la imagen en self

        imagen = self.imagen.copy() #copy asegura que no se haga referencia a self.imagen separandolo
                                    #basicamente crea otra instancia de imagen la cual si modificara
        ancho_max = self.winfo_width()
        alto_max = self.winfo_height()
        imagen.thumbnail((ancho_max, alto_max))
        self.foto = ImageTk.PhotoImage(imagen)
        self.label.config(image=self.foto)
        self.label.image = self.foto

    
    
class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Editor de imagenes")
        self.geometry("700x400")

        # Barra de actividades
        self.barra_actividades = BarraDeActividades(self, self)
        self.barra_actividades.pack(side="left", fill="y")

        # Contenedor para las barras laterales
        self.sidebar_container = tk.Frame(self, bg="white", width=150)
        self.sidebar_container.pack(side="left", fill="y")

        # Área principal
        self.main_area = tk.Frame(self, bg="white")
        self.main_area.pack(side="right", fill="both", expand=True)

        # Caja de Imagen (panel derecho)
        self.caja_imagen = CajaDeImagen(self, width=550, height=500)
        self.caja_imagen.pack(side="right", fill="both", expand=True)

        #A partir de aca, se podria poner esta funcionaliadad
        #en la barra de actividades, cambiar despues
        # Instancias de las barras laterales
        self.sidebars = {
            "archivos": BarraLateralArchivos(self.sidebar_container, self.caja_imagen),
            "imagenes": BarraLateralImagenes(self.sidebar_container),
            "config": BarraLateralConfiguracion(self.sidebar_container),
            "guardar": BarraLateralGuardado(self.sidebar_container, self.caja_imagen)
        }
        # Por defecto muestro una
        self.mostrar_sidebar("archivos")


    def mostrar_sidebar(self, cual):
        """Oculta todas y muestra solo la seleccionada."""
        for sidebar in self.sidebars.values():
            sidebar.pack_forget()
        self.sidebars[cual].pack(fill="both", expand=True)


#iniciador
if __name__ == "__main__":
    app = VentanaPrincipal()
    app.mainloop()
