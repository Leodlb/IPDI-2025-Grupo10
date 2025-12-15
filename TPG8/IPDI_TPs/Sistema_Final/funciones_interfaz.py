from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import Segmentar_ojos as ojs
import app as conv
import my_functions as mf
import procesamiento_por_convolucion as ppc
import Procesamiento_Morfologico as pm
import Procesamiento_Segmentacion as pseg
import cv2


class ImageManager:
    """Gestiona el estado de las imágenes y operaciones básicas"""
    
    def __init__(self):
        self.original_image = None
        self.modified_image = None
        self.secondary_image = None

    def set_original_image(self, img): self.original_image = img
    def get_original_image(self): return self.original_image

    def set_modified_image(self, img): self.modified_image = img
    def get_modified_image(self): return self.modified_image

    def set_secondary_image(self, img): self.secondary_image = img
    def get_secondary_image(self): return self.secondary_image
    
    @staticmethod
    def normalizar_imagen(img):
        """Normaliza una imagen al rango [0, 1]"""
        im = np.array(img)
        return np.clip(im / 255.0, 0.0, 1.0)
    
    @staticmethod
    def pasar_a_pil(img):
        """Convierte un array numpy a imagen PIL (0-255)"""
        img_uint8 = np.clip(img, 0, 255).astype(np.uint8)
        return Image.fromarray(img_uint8)
    
    @staticmethod
    def mostrar_imagen(img, label_widget, tamaño=(700, 700)):
        """Muestra una imagen en un widget de label"""
        img_redimensionada = img.copy()
        img_redimensionada.thumbnail(tamaño, Image.Resampling.LANCZOS)
        imagen_tk = ImageTk.PhotoImage(img_redimensionada)
        label_widget.configure(image=imagen_tk, text="")
        label_widget.image = imagen_tk
        return imagen_tk
    
    def verificar_imagen(self, imagen=None):
        """Verifica si hay una imagen disponible"""
        if imagen is None:
            imagen = self.original_image
        if imagen is None:
            messagebox.showwarning("Advertencia", "Primero abre una imagen.")
            return False
        return True


class FileHandler:
    """Maneja operaciones de archivo"""
    
    def __init__(self, image_manager):
        self.image_manager = image_manager
    
    def abrir_imagen(self, lbl_imagen_original):
        """Abre una imagen desde un diálogo de archivo"""
        ruta = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[("Archivos de imagen", "*.jpg *.png *.jpeg *.bmp *.gif")]
        )
        if not ruta:
            return

        try:
            imagen_original = Image.open(ruta).convert("RGB")
            self.image_manager.set_original_image(imagen_original)
            self.image_manager.mostrar_imagen(imagen_original, lbl_imagen_original)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir la imagen: {e}")
            
    def cargar_imagen_secundaria(self, lbl_imagen_secundaria):
        """Carga la segunda imagen desde un diálogo"""
        ruta = filedialog.askopenfilename(title="Seleccionar segunda imagen")
        if not ruta:
            return
        try:
            img = Image.open(ruta).convert("RGB")
            self.image_manager.set_secondary_image(img)
            self.image_manager.mostrar_imagen(img, lbl_imagen_secundaria)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir la segunda imagen: {e}")
    
    def guardar_imagen(self):
        """Guarda la imagen modificada"""
        if not self.image_manager.verificar_imagen(self.image_manager.get_modified_image()):
            return

        ruta = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png"), ("BMP", "*.bmp")]
        )
        if not ruta:
            return

        try:
            self.image_manager.get_modified_image().save(ruta)
            messagebox.showinfo("Éxito", f"Imagen guardada en: {ruta}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la imagen: {e}")


class ImageProcessor:
    """Procesa imágenes con diversas operaciones"""
    
    def __init__(self, image_manager):
        self.image_manager = image_manager
    
    def _procesar_imagen(self, procesamiento_func, lbl_imagen_modificada):
        """Función genérica para procesar imágenes"""
        if not self.image_manager.verificar_imagen():
            return
        
        try:
            resultado = procesamiento_func(self.image_manager.get_original_image())
            self.image_manager.set_modified_image(resultado)
            self.image_manager.mostrar_imagen(resultado, lbl_imagen_modificada)
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar la imagen: {e}")
    
    def invertir_colores(self, lbl_imagen_modificada):
        """Invierte los colores de la imagen"""
        def invertir(img):
            img_modificada = img.copy()
            pixeles = img_modificada.load()
            ancho, alto = img_modificada.size
            
            for x in range(ancho):
                for y in range(alto):
                    r, g, b = pixeles[x, y]
                    pixeles[x, y] = (255 - r, 255 - g, 255 - b)
            return img_modificada
        
        self._procesar_imagen(invertir, lbl_imagen_modificada)
    
    def procesar_ojos(self, lbl_imagen_modificada):
        """Procesa la imagen para segmentar los ojos"""
        def segmentar_ojos(img):
            im = self.image_manager.normalizar_imagen(img)
            dark_umbral = 0.20
            dark_mask = (im[:, :, 0] < dark_umbral) & (im[:, :, 1] < dark_umbral) & (im[:, :, 2] < dark_umbral)
            connected_mask = ojs.conectar_pixeles(dark_mask, distance=5)
            filtered_mask = ojs.marcar_ojos(connected_mask)
            segmented_eyes = im.copy()
            for i in range(3):
                segmented_eyes[:, :, i] = im[:, :, i] * filtered_mask
            return self.image_manager.pasar_a_pil(segmented_eyes)
        
        self._procesar_imagen(segmentar_ojos, lbl_imagen_modificada)


class ColorSpaceProcessor:
    """Procesa conversiones entre espacios de color"""
    
    def __init__(self, image_manager):
        self.image_manager = image_manager
    
    def _procesar_espacio_color(self, procesamiento_func, lbl_imagen_modificada):
        """Función genérica para procesamiento de espacios de color"""
        if not self.image_manager.verificar_imagen():
            return
        
        try:
            im = self.image_manager.normalizar_imagen(self.image_manager.get_original_image())
            resultado = procesamiento_func(im)
            img_pil = self.image_manager.pasar_a_pil(resultado * 255.0)
            self.image_manager.set_modified_image(img_pil)
            self.image_manager.mostrar_imagen(img_pil, lbl_imagen_modificada)
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar la imagen: {e}")
    
    def mostrar_canales_yiq(self, label_widget, canales_seleccionados):
        def procesar_yiq(im):
            yiq = conv.rgb_a_yiq(im)
            yiq = conv.verificar_rangos_yiq(yiq)
            normalizadores = {
                "Y": lambda y: y,
                "I": lambda i: (i + 0.5957) / (2 * 0.5957),
                "Q": lambda q: (q + 0.5226) / (2 * 0.5226) 
            }
            canales_activos = [c for c, sel in canales_seleccionados.items() if sel]
            if not canales_activos:
                return np.zeros(im.shape[:2])
            if len(canales_activos) == 1:
                canal_idx = ["Y", "I", "Q"].index(canales_activos[0])
                return normalizadores[canales_activos[0]](yiq[:, :, canal_idx])
            imagen_compuesta = np.zeros(im.shape[:2])
            for canal in canales_activos:
                canal_idx = ["Y", "I", "Q"].index(canal)
                imagen_compuesta += normalizadores[canal](yiq[:, :, canal_idx])
            return imagen_compuesta / len(canales_activos)
        self._procesar_espacio_color(procesar_yiq, label_widget)
    
    def mostrar_canales_rgb(self, label_widget, canales_seleccionados):
        def procesar_rgb(im):
            canales_activos = [c for c, sel in canales_seleccionados.items() if sel]
            if not canales_activos:
                return np.zeros(im.shape)
            if len(canales_activos) == 1:
                idx = ["R", "G", "B"].index(canales_activos[0])
                return im[:, :, idx]
            imagen_compuesta = np.zeros_like(im)
            for canal in canales_activos:
                idx = ["R", "G", "B"].index(canal)
                imagen_compuesta[:, :, idx] = im[:, :, idx]
            return imagen_compuesta
        self._procesar_espacio_color(procesar_rgb, label_widget)
    
    def convertir_yiq_a_rgb(self, label_widget):
        def convertir(im):
            yiq = conv.rgb_a_yiq(im)
            yiq = conv.verificar_rangos_yiq(yiq)
            return conv.yiq_a_rgb(yiq)
        self._procesar_espacio_color(convertir, label_widget)
    
    def mostrar_yiq_en_rgb(self, label_widget, canales_seleccionados):
        def procesar_yiq_rgb(im):
            yiq = conv.rgb_a_yiq(im)
            yiq = conv.verificar_rangos_yiq(yiq)
            imagen_rgb = np.zeros(im.shape)
            if canales_seleccionados.get("Y", False):
                imagen_rgb[:, :, 0] = yiq[:, :, 0]
            if canales_seleccionados.get("I", False):
                imagen_rgb[:, :, 1] = (yiq[:, :, 1] + 0.5957) / (2 * 0.5957)
            if canales_seleccionados.get("Q", False):
                imagen_rgb[:, :, 2] = (yiq[:, :, 2] + 0.5226) / (2 * 0.5226)
            return imagen_rgb
        self._procesar_espacio_color(procesar_yiq_rgb, label_widget)


class ConvolutionProcessor:
    """Procesa filtros de convolución"""
    
    def __init__(self, image_manager):
        self.image_manager = image_manager
        
    def _aplicar_filtro(self, kernel, label_widget):
        if not self.image_manager.verificar_imagen():
            return
            
        try:
            # Obtener imagen original
            img = self.image_manager.get_original_image()
            # Convertir a escala de grises (L) o usar canal Y de YIQ
            # Usaremos escala de grises directa de PIL para simplificar
            img_gray = img.convert("L")
            arr_gray = np.array(img_gray, dtype=np.float32) / 255.0
            
            # Aplicar convolución
            resultado = ppc.convolucion(arr_gray, kernel)
            
            # Normalizar resultado para visualización (0-1)
            # Algunos filtros (bordes, pasaaltos) pueden dar negativos o > 1
            # Para visualización, hacemos clip.
            # Opcional: Escalar al rango 0-1 (min-max scaling) si es muy bajo
            
            # Estrategia simple: Clip 0-1
            resultado_vis = np.clip(resultado, 0.0, 1.0)
            
            img_pil = self.image_manager.pasar_a_pil(resultado_vis * 255.0)
            self.image_manager.set_modified_image(img_pil)
            self.image_manager.mostrar_imagen(img_pil, label_widget)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en convolución: {e}")

    def aplicar_pasabajos(self, tipo, size, label_widget):
        try:
            size = int(size)
            if tipo == "Plano":
                kernel = ppc.kernel_plano(size)
            elif tipo == "Bartlett":
                kernel = ppc.kernel_bartlett(size)
            elif tipo == "Gaussiano":
                kernel = ppc.kernel_gaussiano(size, sigma=1.0) # Sigma default
            else:
                return
            self._aplicar_filtro(kernel, label_widget)
        except Exception as e:
             messagebox.showerror("Error", f"Error configurando filtro: {e}")

    def aplicar_bordes(self, tipo, param, label_widget):
        try:
            if tipo == "Laplaciano":
                kernel = ppc.kernel_laplaciano(param) # param es 'v4' o 'v8'
            elif tipo == "Sobel":
                kernel = ppc.kernel_sobel(param) # param es orientacion
            else:
                return
            self._aplicar_filtro(kernel, label_widget)
        except Exception as e:
             messagebox.showerror("Error", f"Error configurando filtro: {e}")

    def aplicar_frecuencia(self, tipo, fc1, fc2, label_widget):
        try:
            fc1 = float(fc1)
            if tipo == "Pasaaltos":
                kernel = ppc.kernel_pasa_altos(fc1)
            elif tipo == "Pasabanda":
                fc2 = float(fc2)
                kernel = ppc.kernel_pasa_banda(fc1, fc2)
            else:
                return
            self._aplicar_filtro(kernel, label_widget)
        except Exception as e:
             messagebox.showerror("Error", f"Error configurando filtro: {e}")


class MorphologyProcessor:
    """Procesa operaciones morfológicas en escala de grises"""
    
    def __init__(self, image_manager):
        self.image_manager = image_manager
        self.morphology = pm.GrayscaleMorphology()
        
    def _aplicar_operacion(self, operacion, kernel_size, label_widget):
        if not self.image_manager.verificar_imagen():
            return
            
        try:
            # Obtener imagen original
            img = self.image_manager.get_original_image()
            # Convertir PIL a numpy array (OpenCV usa BGR)
            img_array = np.array(img)
            # Convertir RGB a BGR para OpenCV
            img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            
            # Aplicar operación morfológica
            resultado = operacion(img_bgr, kernel_size)
            
            # Convertir de vuelta a RGB
            resultado_rgb = cv2.cvtColor(resultado, cv2.COLOR_GRAY2RGB)
            
            img_pil = self.image_manager.pasar_a_pil(resultado_rgb)
            self.image_manager.set_modified_image(img_pil)
            self.image_manager.mostrar_imagen(img_pil, label_widget)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en morfología: {e}")

    def aplicar_erosion(self, kernel_size, label_widget):
        self._aplicar_operacion(self.morphology.erode, kernel_size, label_widget)

    def aplicar_dilatacion(self, kernel_size, label_widget):
        self._aplicar_operacion(self.morphology.dilate, kernel_size, label_widget)

    def aplicar_apertura(self, kernel_size, label_widget):
        self._aplicar_operacion(self.morphology.opening, kernel_size, label_widget)

    def aplicar_cierre(self, kernel_size, label_widget):
        self._aplicar_operacion(self.morphology.closing, kernel_size, label_widget)

    def aplicar_gradiente(self, kernel_size, label_widget):
        self._aplicar_operacion(self.morphology.morphological_gradient, kernel_size, label_widget)

    def aplicar_borde_externo(self, kernel_size, label_widget):
        self._aplicar_operacion(self.morphology.external_boundary, kernel_size, label_widget)

    def aplicar_borde_interno(self, kernel_size, label_widget):
        self._aplicar_operacion(self.morphology.internal_boundary, kernel_size, label_widget)

    def aplicar_mediana(self, kernel_size, label_widget):
        # Mediana solo acepta int, no tupla
        k = kernel_size if isinstance(kernel_size, int) else kernel_size[0]
        self._aplicar_operacion(self.morphology.median_filter, k, label_widget)


class SegmentationProcessor:
    """Procesa operaciones de segmentación: binarización, bordes y magic wand"""
    
    def __init__(self, image_manager):
        self.image_manager = image_manager
        self.segmenter = pseg.AdvancedSegmentation()
        
    def _aplicar_segmentacion(self, operacion, label_widget):
        if not self.image_manager.verificar_imagen():
            return
            
        try:
            # Obtener imagen original
            img = self.image_manager.get_original_image()
            # Convertir PIL a numpy array (OpenCV usa BGR)
            img_array = np.array(img)
            # Convertir RGB a BGR para OpenCV
            img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            
            # Aplicar operación de segmentación
            resultado = operacion(img_bgr)
            
            # Convertir de vuelta a RGB si es necesario
            if len(resultado.shape) == 2:  # Imagen en escala de grises
                resultado_rgb = cv2.cvtColor(resultado, cv2.COLOR_GRAY2RGB)
            else:
                resultado_rgb = cv2.cvtColor(resultado, cv2.COLOR_BGR2RGB)
            
            img_pil = self.image_manager.pasar_a_pil(resultado_rgb)
            self.image_manager.set_modified_image(img_pil)
            self.image_manager.mostrar_imagen(img_pil, label_widget)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en segmentación: {e}")
    
    # Métodos de binarización
    def aplicar_binarizacion_50(self, label_widget):
        self._aplicar_segmentacion(self.segmenter.threshold_median_50, label_widget)
    
    def aplicar_binarizacion_bimodal(self, label_widget):
        self._aplicar_segmentacion(self.segmenter.threshold_two_modes, label_widget)
    
    def aplicar_binarizacion_otsu(self, label_widget):
        self._aplicar_segmentacion(self.segmenter.threshold_otsu, label_widget)
    
    # Métodos de detección de bordes
    def aplicar_bordes_laplaciano(self, label_widget):
        self._aplicar_segmentacion(self.segmenter.edge_laplacian, label_widget)
    
    def aplicar_bordes_morfologico(self, kernel_size, label_widget):
        operacion = lambda img: self.segmenter.edge_morphological(img, kernel_size)
        self._aplicar_segmentacion(operacion, label_widget)
    
    def aplicar_marching_squares(self, label_widget):
        self._aplicar_segmentacion(self.segmenter.edge_marching_squares, label_widget)
    
    # Magic Wand
    def aplicar_magic_wand(self, seed_point, tolerance, label_widget):
        if not self.image_manager.verificar_imagen():
            return
            
        try:
            img = self.image_manager.get_original_image()
            img_array = np.array(img)
            img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            
            # Aplicar magic wand
            mask = self.segmenter.magic_wand(img_bgr, seed_point, tolerance)
            
            # Crear imagen con la máscara aplicada
            resultado = img_bgr.copy()
            # Resaltar área seleccionada con color verde
            resultado[mask > 0] = [0, 255, 0]
            
            resultado_rgb = cv2.cvtColor(resultado, cv2.COLOR_BGR2RGB)
            img_pil = self.image_manager.pasar_a_pil(resultado_rgb)
            self.image_manager.set_modified_image(img_pil)
            self.image_manager.mostrar_imagen(img_pil, label_widget)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en magic wand: {e}")



# -------------------------------
# Funciones de aritmética de píxeles
# -------------------------------


def _redimensionar_segunda_al_original(img1, img2):
    """Redimensiona la segunda imagen al tamaño de la primera."""
    if img1.size != img2.size:
        img2 = img2.resize(img1.size, Image.Resampling.LANCZOS)
    return img2

def cuasi_suma_rgb_clamp(image_manager, lbl_resultado):
    """Suma dos imágenes (RGB) y muestra el resultado"""
    if not image_manager.get_original_image() or not image_manager.get_secondary_image():
        messagebox.showwarning("Error", "Primero carga ambas imágenes.")
        return

    img1 = image_manager.get_original_image()
    img2 = _redimensionar_segunda_al_original(img1, image_manager.get_secondary_image())

    arr1 = np.array(img1)
    arr2 = np.array(img2)
    
    resultado = mf.sum_rgb(arr1, arr2, method="mean")  # valores 0-255
    if resultado.max() <= 1.0:
        resultado = resultado * 255.0

    img_pil = image_manager.pasar_a_pil(resultado)
    image_manager.set_modified_image(img_pil)
    image_manager.mostrar_imagen(img_pil, lbl_resultado)

def cuasi_resta_rgb_clamp(image_manager, lbl_resultado):
    """Resta dos imágenes (RGB) y muestra el resultado"""
    if not image_manager.get_original_image() or not image_manager.get_secondary_image():
        messagebox.showwarning("Error", "Primero carga ambas imágenes.")
        return

    img1 = image_manager.get_original_image()
    img2 = _redimensionar_segunda_al_original(img1, image_manager.get_secondary_image())

    arr1 = np.array(img1)
    arr2 = np.array(img2)
    
    resultado = mf.diff_rgb(arr1, arr2, method="mean")
    if resultado.max() <= 1.0:
        resultado = resultado * 255.0

    img_pil = image_manager.pasar_a_pil(resultado)
    image_manager.set_modified_image(img_pil)
    image_manager.mostrar_imagen(img_pil, lbl_resultado)


def sum_yiq_clamp(image_manager, lbl_resultado):
    """Suma dos imágenes (YIQ) y muestra el resultado"""
    if not image_manager.get_original_image() or not image_manager.get_secondary_image():
        messagebox.showwarning("Error", "Primero carga ambas imágenes.")
        return

    img1 = image_manager.get_original_image()
    img2 = _redimensionar_segunda_al_original(img1, image_manager.get_secondary_image())

    arr1 = np.array(img1)
    arr2 = np.array(img2)
    
    resultado = mf.sum_yiq(arr1, arr2, method="mean")
    if resultado.max() <= 1.0:
        resultado = resultado * 255.0

    img_pil = image_manager.pasar_a_pil(resultado)
    image_manager.set_modified_image(img_pil)
    image_manager.mostrar_imagen(img_pil, lbl_resultado)

def if_lighter(image_manager, lbl_resultado):
    """Selecciona el pixel más claro entre dos imágenes"""
    if not image_manager.get_original_image() or not image_manager.get_secondary_image():
        messagebox.showwarning("Error", "Primero carga ambas imágenes.")
        return

    img1 = image_manager.get_original_image()
    img2 = _redimensionar_segunda_al_original(img1, image_manager.get_secondary_image())

    arr1 = np.array(img1)
    arr2 = np.array(img2)

    resultado = mf.if_lighter(arr1, arr2)
    if resultado.max() <= 1.0:
        resultado = resultado * 255.0

    img_pil = image_manager.pasar_a_pil(resultado)
    image_manager.set_modified_image(img_pil)
    image_manager.mostrar_imagen(img_pil, lbl_resultado)


def if_darker(image_manager, lbl_resultado):
    """Selecciona el pixel más oscuro entre dos imágenes"""
    if not image_manager.get_original_image() or not image_manager.get_secondary_image():
        messagebox.showwarning("Error", "Primero carga ambas imágenes.")
        return

    img1 = image_manager.get_original_image()
    img2 = _redimensionar_segunda_al_original(img1, image_manager.get_secondary_image())

    arr1 = np.array(img1)
    arr2 = np.array(img2)

    resultado = mf.if_darker(arr1, arr2)
    if resultado.max() <= 1.0:
        resultado = resultado * 255.0

    img_pil = image_manager.pasar_a_pil(resultado)
    image_manager.set_modified_image(img_pil)
    image_manager.mostrar_imagen(img_pil, lbl_resultado)




# -------------------------------
# Instancias globales
# -------------------------------
image_manager = ImageManager()
file_handler = FileHandler(image_manager)
image_processor = ImageProcessor(image_manager)
color_processor = ColorSpaceProcessor(image_manager)
convolution_processor = ConvolutionProcessor(image_manager)
morphology_processor = MorphologyProcessor(image_manager)
segmentation_processor = SegmentationProcessor(image_manager)


# -------------------------------
# Funciones de interfaz
# -------------------------------
def abrir_imagen(lbl_imagen_original):
    file_handler.abrir_imagen(lbl_imagen_original)

def cargar_imagen_secundaria(lbl_imagen_secundaria):
    file_handler.cargar_imagen_secundaria(lbl_imagen_secundaria)

def guardar_imagen():
    file_handler.guardar_imagen()

def verificar_imagen(imagen=None):
    return image_manager.verificar_imagen(imagen)

def invertir_colores(lbl_imagen_modificada):
    image_processor.invertir_colores(lbl_imagen_modificada)

def procesar_ojos(lbl_imagen_modificada):
    image_processor.procesar_ojos(lbl_imagen_modificada)

def mostrar_imagen(img, label_widget):
    return image_manager.mostrar_imagen(img, label_widget)

def mostrar_canales_yiq(label_widget, canales_seleccionados):
    color_processor.mostrar_canales_yiq(label_widget, canales_seleccionados)

def mostrar_canales_rgb(label_widget, canales_seleccionados):
    color_processor.mostrar_canales_rgb(label_widget, canales_seleccionados)

def mostrar_yiq_en_rgb(label_widget, canales_seleccionados):
    color_processor.mostrar_yiq_en_rgb(label_widget, canales_seleccionados)

def convertir_yiq_a_rgb(label_widget):
    color_processor.convertir_yiq_a_rgb(label_widget)

def normalizar_imagen(img):
    return image_manager.normalizar_imagen(img)

def pasar_a_pil(img):
    return image_manager.pasar_a_pil(img)

# Wrappers para convolución
def aplicar_filtro_pasabajos(tipo, size, lbl):
    convolution_processor.aplicar_pasabajos(tipo, size, lbl)

def aplicar_filtro_bordes(tipo, param, lbl):
    convolution_processor.aplicar_bordes(tipo, param, lbl)

def aplicar_filtro_frecuencia(tipo, fc1, fc2, lbl):
    convolution_processor.aplicar_frecuencia(tipo, fc1, fc2, lbl)

# Wrappers para morfología
def aplicar_morfologia(operacion, kernel_size, lbl):
    ops = {
        "Erosión": morphology_processor.aplicar_erosion,
        "Dilatación": morphology_processor.aplicar_dilatacion,
        "Apertura": morphology_processor.aplicar_apertura,
        "Cierre": morphology_processor.aplicar_cierre,
        "Gradiente Morfológico": morphology_processor.aplicar_gradiente,
        "Borde Externo": morphology_processor.aplicar_borde_externo,
        "Borde Interno": morphology_processor.aplicar_borde_interno,
        "Mediana": morphology_processor.aplicar_mediana
    }
    func = ops.get(operacion)
    if func:
        func(kernel_size, lbl)

def copiar_procesada_a_original():
    """Copia la imagen modificada a la original para procesamiento secuencial"""
    if image_manager.get_modified_image():
        image_manager.set_original_image(image_manager.get_modified_image())
        messagebox.showinfo("Éxito", "Imagen procesada copiada a original.")
    else:
        messagebox.showwarning("Advertencia", "No hay imagen procesada para copiar.")

# Wrappers para segmentación
def aplicar_segmentacion(operacion, param, lbl):
    """Aplica operaciones de segmentación según el tipo"""
    ops_binarizacion = {
        "50% Threshold": segmentation_processor.aplicar_binarizacion_50,
        "Bimodal": segmentation_processor.aplicar_binarizacion_bimodal,
        "Otsu": segmentation_processor.aplicar_binarizacion_otsu
    }
    
    ops_bordes = {
        "Laplaciano": segmentation_processor.aplicar_bordes_laplaciano,
        "Morfológico": lambda lbl: segmentation_processor.aplicar_bordes_morfologico(param, lbl),
        "Marching Squares": segmentation_processor.aplicar_marching_squares
    }
    
    # Intentar en binarización
    func = ops_binarizacion.get(operacion)
    if func:
        func(lbl)
        return
    
    # Intentar en bordes
    func = ops_bordes.get(operacion)
    if func:
        func(lbl)
        return

def aplicar_magic_wand(seed_point, tolerance, lbl):
    """Aplica la herramienta varita mágica"""
    segmentation_processor.aplicar_magic_wand(seed_point, tolerance, lbl)

