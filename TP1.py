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
        tk.Button(self, text="⚙️", command=lambda: ventana.mostrar_sidebar("config")).pack(ipady=6, ipadx=6) #clave corregida
        tk.Button(self, text="💾", command=lambda: ventana.mostrar_sidebar("guardar")).pack(ipady=7, ipadx=7)

class CajaDeImagen(tk.Frame):
    """
    Con esta clase se interactuara con la imagen, contiene la imagen
    Deberia agregar los metodos para modificar las imagenes aca
    Seria mas recomendable hacer eso en otra clase, principio de responsabilidad
    pero como quedaria muy vacia, se usa preferentemente esta.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.label = tk.Label(self, bg="white")
        self.label.pack(expand=True, fill="both")

        self.imagen = None   # original PIL.Image
        self.foto = None     # PhotoImage actual

        # Vincular evento de cambio de tamaño
        self.bind("<Configure>", self._on_resize)

    def mostrar_imagen(self, ruta_imagen=None):
        if ruta_imagen:
            self.imagen = Image.open(ruta_imagen)
            self._imagen_procesada = None  # al cambiar de archivo, limpiamos resultado

        if not hasattr(self, "imagen") or self.imagen is None:
            return
        self._render_image()

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
        im = img.copy()
        im.thumbnail((ancho_max, alto_max))
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

#codigo anterior de CajaDeImagen, lo dejo comentado por las dudas
""" 
class CajaDeImagen(tk.Frame):
    '''
    Con esta clase se interactuara con la imagen, contiene la imagen
    Deberia agregar los metodos para modificar las imagenes aca
    Seria mas recomendable hacer eso en otra clase, principio de responsabilidad
    pero como quedaria muy vacia, se usa preferentemente esta.
    '''

    def __init__(self, master, **kwargs):
        super().__init__(master, bg="white", **kwargs)
        self.label = tk.Label(self, bg="white")
        self.label.pack(expand=True, fill="both")


    
    def mostrar_imagen(self, ruta_imagen=None):
        '''
        importante, al cargar la imagen por primera vez se va a crear un objeto imagen
        al volver a interactuar con la funcion si la ruta imagen es nula y no se ingresa
        entonces esta variable no se sobreescribira.
        Lo que hara es interactuar con la imagen previamente escrita.
        '''
        if ruta_imagen:   # cuando no esta cargada la imagen lo cambia
            self.imagen = Image.open(ruta_imagen) #esto es mportante, al cargar la imagen en self
        if not hasattr(self, "imagen"):
            return  # nada que mostrar todavía
        self.update_idletasks()
        ancho_max = max(self.winfo_width(), 1)
        alto_max  = max(self.winfo_height(), 1)
        imagen = self.imagen.copy() #copy asegura que no se haga referencia a self.imagen separandolo
                                    #basicamente crea otra instancia de imagen la cual si modificara
        imagen.thumbnail((ancho_max, alto_max))
        self.foto = ImageTk.PhotoImage(imagen)
        self.label.config(image=self.foto, anchor="center")
        self.label.image = self.foto

"""

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
            "imagenes": BarraLateralImagenes(self.sidebar_container, self.caja_imagen),
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
