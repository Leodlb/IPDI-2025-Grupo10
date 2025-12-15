import cv2
import numpy as np
import logging
from typing import Union, Tuple

# Configuración de logs errores
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger('IPDI_Core')

class GrayscaleMorphology:


    def _get_kernel(self, size: Union[int, Tuple[int, int]]) -> np.ndarray:
        """Genera kernel rectangular (tupla) o cuadrado (int)."""
        if isinstance(size, int):
            return np.ones((size, size), np.uint8)
        return np.ones(size, np.uint8) 

    def _ensure_grayscale(self, image: np.ndarray) -> np.ndarray:
        """
        Valida y convierte la imagen a escala de grises si es necesario.
        """
        if image is None or image.size == 0:
            raise ValueError("Imagen vacía o nula.")
        
        if len(image.shape) == 3 and image.shape[2] >= 3:
            return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
        return image

    def erode(self, image: np.ndarray, kernel_size: Union[int, Tuple[int, int]] = (2, 3)) -> np.ndarray:
        """Erosión (Mínimo). Default kernel 2x3."""
        try:
            img_gray = self._ensure_grayscale(image)
            kernel = self._get_kernel(kernel_size)
            return cv2.erode(img_gray, kernel, iterations=1)
        except Exception as e:
            logger.error(f"Erosión fallida: {e}")
            raise

    def dilate(self, image: np.ndarray, kernel_size: Union[int, Tuple[int, int]] = (2, 3)) -> np.ndarray:
        """Dilatación (Máximo). Default kernel 2x3."""
        try:
            img_gray = self._ensure_grayscale(image)
            kernel = self._get_kernel(kernel_size)
            return cv2.dilate(img_gray, kernel, iterations=1)
        except Exception as e:
            logger.error(f"Dilatación fallida: {e}")
            raise

    def opening(self, image: np.ndarray, kernel_size: Union[int, Tuple[int, int]] = (2, 3)) -> np.ndarray:
        """Apertura: Erosión -> Dilatación."""
        try:
            eroded = self.erode(image, kernel_size)
            return self.dilate(eroded, kernel_size)
        except Exception as e:
            logger.error(f"Apertura fallida: {e}")
            raise

    def closing(self, image: np.ndarray, kernel_size: Union[int, Tuple[int, int]] = (2, 3)) -> np.ndarray:
        """Cierre: Dilatación -> Erosión."""
        try:
            dilated = self.dilate(image, kernel_size)
            return self.erode(dilated, kernel_size)
        except Exception as e:
            logger.error(f"Cierre fallido: {e}")
            raise

    def external_boundary(self, image: np.ndarray, kernel_size: Union[int, Tuple[int, int]] = (2, 3)) -> np.ndarray:
        """Borde Exterior: Dilatación - Original."""
        try:
            img_gray = self._ensure_grayscale(image)
            dilated = self.dilate(img_gray, kernel_size)
            return cv2.subtract(dilated, img_gray)
        except Exception as e:
            logger.error(f"Borde ext fallido: {e}")
            raise

    def internal_boundary(self, image: np.ndarray, kernel_size: Union[int, Tuple[int, int]] = (2, 3)) -> np.ndarray:
        """Borde Interior: Original - Erosión (PDF Pág 3)."""
        try:
            img_gray = self._ensure_grayscale(image)
            eroded = self.erode(img_gray, kernel_size)
            return cv2.subtract(img_gray, eroded)
        except Exception as e:
            logger.error(f"Borde int fallido: {e}")
            raise

    def morphological_gradient(self, image: np.ndarray, kernel_size: Union[int, Tuple[int, int]] = (2, 3)) -> np.ndarray:
        """Gradiente: Dilatación - Erosión."""
        try:
            img_gray = self._ensure_grayscale(image)
            dilated = self.dilate(img_gray, kernel_size)
            eroded = self.erode(img_gray, kernel_size)
            return cv2.subtract(dilated, eroded)
        except Exception as e:
            logger.error(f"Gradiente fallido: {e}")
            raise

    def median_filter(self, image: np.ndarray, kernel_size: int = 3) -> np.ndarray:
        """Filtro Mediana. Nota: Kernel debe ser impar y cuadrado para medianBlur."""
        try:
            img_gray = self._ensure_grayscale(image)
            k = kernel_size if kernel_size % 2 == 1 else kernel_size + 1
            return cv2.medianBlur(img_gray, k)
        except Exception as e:
            logger.error(f"Mediana fallida: {e}")
            raise