import cv2
import numpy as np
import logging
from typing import Tuple, List, Optional, Union
from skimage import measure

# Configuración de logs comentarios
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger('IPDI_Segmentacion')

class AdvancedSegmentation:
    """
    Implementación de algoritmos de segmentación avanzada, binarización adaptativa
    y detección de bordes mediante métodos estadísticos y morfológicos.
    """

    def _ensure_grayscale(self, image: np.ndarray) -> np.ndarray:
        """Convierte imagen a escala de grises si es color."""
        if image.ndim == 3:
            return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return image

    def _validate(self, image: np.ndarray) -> None:
        """Valida que la imagen no esté vacía."""
        if image is None or image.size == 0:
            raise ValueError("La imagen de entrada es nula o vacía.")

    # --- Métodos de Binarización ---

    def threshold_median_50(self, image: np.ndarray) -> np.ndarray:
        """
        Realiza binarización estadística utilizando la mediana de intensidad 
        como umbral para equilibrar la distribución de píxeles negros y blancos (aprox 50%).
        """
        try:
            self._validate(image)
            img_gray = self._ensure_grayscale(image)
            
            median_val = np.median(img_gray)
            _, binary = cv2.threshold(img_gray, median_val, 255, cv2.THRESH_BINARY)
            
            return binary
        except Exception as e:
            logger.error(f"Fallo en binarización por mediana: {e}")
            raise

    def threshold_two_modes(self, image: np.ndarray) -> np.ndarray:
        """
        Binarización bimodal. Identifica las dos modas principales (clara y oscura) 
        en el histograma suavizado y establece el umbral por distancia mínima (punto medio).
        """
        try:
            self._validate(image)
            img_gray = self._ensure_grayscale(image)

            # 1. Calcular Histograma
            hist = cv2.calcHist([img_gray], [0], None, [256], [0, 256]).flatten()
            
            # 2. Suavizar histograma para eliminar ruido local
            kernel_smooth = cv2.getGaussianKernel(9, 2)
            hist_smooth = cv2.filter2D(hist, -1, kernel_smooth).flatten()

            # 3. Encontrar picos (modas) dividiendo el espectro por la media
            mean_val = int(np.mean(img_gray))
            
            mode_dark = np.argmax(hist_smooth[:mean_val])
            mode_light = np.argmax(hist_smooth[mean_val:]) + mean_val

            # 4. Umbral de distancia mínima (promedio entre picos)
            threshold = int((mode_dark + mode_light) / 2)
            
            _, binary = cv2.threshold(img_gray, threshold, 255, cv2.THRESH_BINARY)
            return binary

        except Exception as e:
            logger.error(f"Fallo en binarización bimodal: {e}")
            raise

    def threshold_otsu(self, image: np.ndarray) -> np.ndarray:
        """
        Ejecuta el algoritmo de Otsu para determinar automáticamente el umbral óptimo
        que maximiza la varianza entre clases (separabilidad).
        """
        try:
            self._validate(image)
            img_gray = self._ensure_grayscale(image)
            
            otsu_thresh, binary = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            return binary
        except Exception as e:
            logger.error(f"Fallo en algoritmo Otsu: {e}")
            raise

    # --- Detección de Bordes y Contornos ---

    def edge_laplacian(self, image: np.ndarray) -> np.ndarray:
        """
        Detecta bordes utilizando el operador Laplaciano (derivada de segundo orden),
        capturando transiciones rápidas de intensidad.
        """
        try:
            self._validate(image)
            img_gray = self._ensure_grayscale(image)
            
            # Usar CV_64F para precisión en derivadas negativas
            lap = cv2.Laplacian(img_gray, cv2.CV_64F)
            lap_abs = cv2.convertScaleAbs(lap)
            return lap_abs
        except Exception as e:
            logger.error(f"Fallo en operador Laplaciano: {e}")
            raise

    def edge_morphological(self, image: np.ndarray, kernel_size: int = 3) -> np.ndarray:
        """
        Calcula el gradiente morfológico (diferencia entre dilatación y erosión)
        para resaltar transiciones de bordes.
        """
        try:
            self._validate(image)
            img_gray = self._ensure_grayscale(image)
            
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
            gradient = cv2.morphologyEx(img_gray, cv2.MORPH_GRADIENT, kernel)
            return gradient
        except Exception as e:
            logger.error(f"Fallo en borde morfológico: {e}")
            raise

    def edge_marching_squares(self, image: np.ndarray, level: float = 0.5) -> np.ndarray:
        """
        Aplica el algoritmo Marching Squares para encontrar contornos (isosuperficies)
        en una imagen 2D. Genera una representación visual de los contornos hallados.
        """
        try:
            self._validate(image)
            img_gray = self._ensure_grayscale(image)
            
            # Determinar nivel de isocontorno mediante Otsu para robustez
            thresh_val, _ = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            contours = measure.find_contours(img_gray, thresh_val)
            
            canvas = np.zeros_like(img_gray)
            for contour in contours:
                pts = np.flip(contour, axis=1).astype(np.int32)
                cv2.polylines(canvas, [pts], isClosed=False, color=255, thickness=1)
                
            return canvas
        except Exception as e:
            logger.error(f"Fallo en Marching Squares: {e}")
            raise

    # --- Segmentación de Regiones ---

    def magic_wand(self, image: np.ndarray, seed_point: Tuple[int, int], tolerance: int = 20) -> np.ndarray:
        """
        Implementa segmentación por crecimiento de regiones (Flood Fill) similar a la
        herramienta 'Varita Mágica', seleccionando áreas contiguas de color similar.
        
        Args:
            seed_point: Coordenadas (x, y) del punto inicial.
            tolerance: Rango de tolerancia para la diferencia de color.
        """
        try:
            self._validate(image)
            work_img = image.copy()
            h, w = work_img.shape[:2]
            
            mask = np.zeros((h + 2, w + 2), np.uint8)
            
            # Configuración FloodFill: 4-conectividad, rango fijo
            flags = 4 | (255 << 8) | cv2.FLOODFILL_FIXED_RANGE
            
            cv2.floodFill(
                work_img, 
                mask, 
                seed_point, 
                newVal=(0, 255, 0),
                loDiff=(tolerance,) * 3, 
                upDiff=(tolerance,) * 3, 
                flags=flags
            )
            
            return mask[1:-1, 1:-1]
            
        except Exception as e:
            logger.error(f"Fallo en Magic Wand: {e}")
            raise

if __name__ == "__main__":
    # Verificación de integridad básica
    x = np.linspace(0, 255, 100)
    y = np.linspace(0, 255, 100)
    xv, yv = np.meshgrid(x, y)
    grad_img = np.uint8((xv + yv) / 2)

    segmenter = AdvancedSegmentation()
    res_otsu = segmenter.threshold_otsu(grad_img)
    print("Módulo AdvancedSegmentation inicializado correctamente.")