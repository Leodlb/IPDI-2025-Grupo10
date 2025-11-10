import numpy as np
import math as mt
from PIL import Image

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



def rgb_to_yiq(img: np.ndarray) -> np.ndarray:
    M = np.array([
        [0.299000,  0.587000,  0.114000],      # Y
        [0.595716, -0.274453, -0.321263],      # I
        [0.211456, -0.522591,  0.311135],      # Q
    ], dtype=np.float32)
    H, W, _ = img.shape
    arr = img.astype(np.float32) / 255.0
    yiq = arr.reshape(-1,3) @ M.T
    return yiq.reshape(H, W, 3)