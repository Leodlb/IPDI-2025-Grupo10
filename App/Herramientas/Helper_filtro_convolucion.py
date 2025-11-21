import numpy as np
import math as mt
from PIL import Image
from Herramientas.Helper_img import yiq_to_rgb, rgb_to_yiq



def matriz_bartlett(npn:int):

    matriz = np.zeros((npn,npn))
    mitad = int (mt.ceil(npn/2))

    if(npn%2 != 0):
        matriz[0,:] = bartlett_primera_fila_impar(npn)
        for i in range(1,mitad):
            matriz[i] = matriz[0]*(i+1)
        matriz[mitad-1:] = matriz[:mitad][::-1]
        return matriz

    matriz[0,:] = bartlett_primera_fila_par(npn)
    for i in range(1,mitad):
        matriz[i] = matriz[0]*(i+1)
    matriz[mitad:] = matriz[:mitad][::-1]
    return matriz


def bartlett_primera_fila_impar(npn:int):
    mitad = int (mt.ceil(npn/2))
    primera_fila = np.zeros(npn)
    for i in range(mitad):
        primera_fila[i] = i + 1
    primera_fila[mitad-1:] = primera_fila[:mitad][::-1]
    return(primera_fila)

def bartlett_primera_fila_par(npn:int):
    mitad = int (mt.ceil(npn/2))
    primera_fila = np.zeros(npn)
    for i in range(mitad):
        primera_fila[i] = i + 1
    primera_fila[mitad:] = primera_fila[:mitad][::-1]
    return(primera_fila)


def matriz_gaussiana(npn):
    matriz = np.zeros((npn,npn))
    mitad = int (mt.ceil(npn/2))

    matriz[0,:] = primera_fila_gausseano(npn)
    for i in range(1,npn):
        for j in range(0,npn):
            if(j == 0):
                matriz[i][j] = matriz[0][i]
            else:
                matriz[i][j] = matriz[0][j] * matriz[0][i]
    return matriz

def primera_fila_gausseano(npn):
    fila_0 = np.zeros(npn)
    for i in range(npn):
        fila_0[i] = mt.comb(npn-1,i)
    return fila_0

def convolution(image, kernel=np.ones((1, 1))):
    image = np.asarray(image, dtype=np.float32)
    kernel = np.asarray(kernel, dtype=np.float32)

    # Normalizar kernel
    if np.sum(kernel) != 0:
        kernel = kernel / np.sum(kernel)

    kh, kw = kernel.shape
    pad_h, pad_w = kh // 2, kw // 2

    # Padding (bordes replicados)
    padded = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)), mode='edge')
    convolved = np.zeros_like(image, dtype=np.float32)

    # Convolución manual
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            region = padded[i:i+kh, j:j+kw]
            convolved[i, j] = np.sum(region * kernel)

    return convolved




def aplicar_kernel_grises(img_rgb: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    """
    Aplica un kernel a la imagen pero trabajando en escala de grises,
    para imitar el comportamiento clásico del Laplaciano.
    """

    # Asegurar float32 en rango [0,1]
    img_float = img_rgb.astype(np.float32) / 255.0

    # Convertir a escala de grises (luminancia clásica)
    # misma fórmula que usa CV2
    gris = (img_float[:, :, 0] +img_float[:, :, 1] +img_float[:, :, 2])/3

    # Convolución en gris
    gris_conv = convolution(gris, kernel)

    """# --- Normalización estilo Laplaciano de clase ---
    # Usualmente se usa la magnitud:
    gris_conv = np.abs(gris_conv)
        

    # Evitar división por cero
    if gris_conv.max() > 0:
        gris_conv = gris_conv / gris_conv.max()

    """

    # Convertir a RGB duplicando canales
    rgb_final = np.stack([gris_conv, gris_conv, gris_conv], axis=2)

    # Volver a 0–255 uint8
    rgb_final = np.clip(rgb_final * 255.0, 0, 255).astype(np.uint8)

    return rgb_final









# kernels para aplicar 
_kernel_identidad= np.array([
        [ 0, 0, 0],
        [ 0, 1, 0],
        [ 0, 0, 0]
    ])

KERNELS_CONVOLUCION = {
    "Convolución Bartlett 3x3" : matriz_bartlett(3),
    "Convolución Bartlett 5x5" : matriz_bartlett(5),
    "Convolución Bartlett 7x7" : matriz_bartlett(7),
    "Convolución Bartlett 9x9" : matriz_bartlett(9),

    "Convolución Gaussiana 3x3": matriz_gaussiana(3),
    "Convolución Gaussiana 5x5": matriz_gaussiana(5),
    "Convolución Gaussiana 7x7": matriz_gaussiana(7),
    "Convolución Gaussiana 9x9": matriz_gaussiana(9),

    "Convolución Laplace 4 vecinos": np.array([
        [ 0, -1,  0],
        [-1,  4, -1],
        [ 0, -1,  0]
    ], dtype=np.float32),

    "Convolución Laplace 8 vecinos": np.array([
        [-1, -1, -1],
        [-1,  8, -1],
        [-1, -1, -1]
    ], dtype=np.float32),

    "Convolución Laplace v4 Filtro Mejora 0.2": np.array([
        [ 0, -1,  0],
        [-1,  4, -1],
        [ 0, -1,  0]
    ], dtype=np.float32)*0.2 + _kernel_identidad,

    "Convolución Laplace v4 Filtro Mejora 0.4": np.array([
        [ 0, -1,  0],
        [-1,  4, -1],
        [ 0, -1,  0]
    ], dtype=np.float32) * 0.4 + _kernel_identidad,

    "Convolución Laplace v8 Filtro Mejora 0.2": np.array([
        [-1, -1, -1],
        [-1,  8, -1],
        [-1, -1, -1]
    ], dtype=np.float32)*0.2 + _kernel_identidad,

    "Convolución Laplace v8 Filtro Mejora 0.4": np.array([
        [-1, -1, -1],
        [-1,  8, -1],
        [-1, -1, -1]
    ], dtype=np.float32) * 0.4 + _kernel_identidad,

    "Convolución derecha": np.array([
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ], dtype=np.float32),

    "Convolución izquierda": np.array([
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ], dtype=np.float32) * -1,
    
    "Convolución arriba": np.transpose( np.array([
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ], dtype=np.float32) * -1),

    "Convolución abajo": np.transpose( np.array([
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ], dtype=np.float32)),

    "Convolución diagonal derecha": np.array([
        [0,  -2, -2],
        [2,  0,  -2],
        [2,  2,  0]
    ], dtype=np.float32) * -1,

    "Convolución diagonal izquierda": np.array([
        [2,  2, 0],
        [2,  0,-2],
        [0, -2,-2]
    ], dtype=np.float32),

    "Convolución diagonal abajo izquierda": np.array([
        [0,  -2, -2],
        [2,  0,  -2],
        [2,  2,  0]
    ], dtype=np.float32),

    "Convolución diagonala abajo derecha": np.array([
        [2,  2, 0],
        [2,  0,-2],
        [0, -2,-2]
    ], dtype=np.float32) *-1,
}
