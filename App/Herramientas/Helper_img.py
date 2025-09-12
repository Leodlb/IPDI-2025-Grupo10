import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt

def linea_cromatica_X(matriz_imagen, x):
    pass

def linea_cromatica_Y(matriz_imagen: np.uint8,y: int):
    tamanio_matriz = matriz_imagen.shape
    linea = matriz_imagen[y]
    x = np.arange(tamanio_matriz[1])
    plt.plot(x, linea[:, 0], color="red")
    plt.plot(x, linea[:, 1], color="green")
    plt.plot(x, linea[:, 2], color="blue")

    plt.show()

def solo_rojo(matriz_imagen):
    matriz_imagen[:,:,1]=0
    matriz_imagen[:,:,2]=0
    return matriz_imagen

def solo_verde(matriz_imagen):
    matriz_imagen[:,:,0]=0
    matriz_imagen[:,:,2]=0
    return matriz_imagen

def solo_azul(matriz_imagen):
    matriz_imagen[:,:,0]=0
    matriz_imagen[:,:,1]=0
    return matriz_imagen

def gris(matriz_imagen: np.uint8):
    promedios = np.mean(matriz_imagen, axis=-1)
    promedios_repetidos = np.expand_dims(promedios, axis=-1)  # convierte (3,4) -> (3,4,1)
    matriz_promedio = np.repeat(promedios_repetidos, matriz_imagen.shape[-1], axis=-1)
    return matriz_promedio

def punto_cromatico():
    pass

def cuasi_suma_rgb_clampeada(imgA: np.ndarray, imgB: np.ndarray) -> np.ndarray:
    resultado = imgA.astype(np.int32) + imgB.astype(np.int32)
    resultado = np.clip(resultado, 0, 255)
    return resultado.astype(np.uint8)

def cuasi_suma_rgb_promediada(imgA: np.ndarray, imgB: np.ndarray) -> np.ndarray:
    resultado = (imgA.astype(np.int32) + imgB.astype(np.int32)) // 2
    return resultado.astype(np.uint8)

def cuasi_resta_rgb_clampeada(imgA: np.ndarray, imgB: np.ndarray) -> np.ndarray:
    resultado = imgA.astype(np.int32) - imgB.astype(np.int32)
    resultado = np.clip(resultado, 0, 255)
    return resultado.astype(np.uint8)

def cuasi_resta_rgb_promediada(imgA: np.ndarray, imgB: np.ndarray) -> np.ndarray:
    resultado = (imgA.astype(np.int32) - imgB.astype(np.int32)) // 2
    resultado = np.clip(resultado, 0, 255)
    return resultado.astype(np.uint8)

# Conversión RGB <-> YIQ
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

def yiq_to_rgb(yiq: np.ndarray) -> np.ndarray:
    M_inv = np.array([
        [1.000000,  0.956300,  0.621000],
        [1.000000, -0.272100, -0.647400],
        [1.000000, -1.106000,  1.703000],
    ], dtype=np.float32)
    H, W, _ = yiq.shape
    rgb = yiq.reshape(-1,3) @ M_inv.T
    rgb = rgb.reshape(H,W,3)
    rgb = np.clip(rgb, 0.0, 1.0)
    return (rgb * 255).astype(np.uint8)

# -------------------------------
# Cuasi-operaciones en YIQ
# -------------------------------

def cuasi_suma_yiq_clampeada(imgA: np.ndarray, imgB: np.ndarray) -> np.ndarray:
    yiqA = rgb_to_yiq(imgA)
    yiqB = rgb_to_yiq(imgB)
    resultado = yiqA + yiqB
    # Clampeo en los rangos típicos de YIQ
    Y = np.clip(resultado[:,:,0], 0.0, 1.0)
    I = np.clip(resultado[:,:,1], -0.5957, 0.5957)
    Q = np.clip(resultado[:,:,2], -0.5226, 0.5226)
    return yiq_to_rgb(np.stack([Y,I,Q], axis=2))

def cuasi_suma_yiq_promediada(imgA: np.ndarray, imgB: np.ndarray) -> np.ndarray:
    yiqA = rgb_to_yiq(imgA)
    yiqB = rgb_to_yiq(imgB)
    resultado = (yiqA + yiqB) / 2
    return yiq_to_rgb(resultado)

def cuasi_resta_yiq_clampeada(imgA: np.ndarray, imgB: np.ndarray) -> np.ndarray:
    yiqA = rgb_to_yiq(imgA)
    yiqB = rgb_to_yiq(imgB)
    resultado = yiqA - yiqB
    # Clampeo
    Y = np.clip(resultado[:,:,0], 0.0, 1.0)
    I = np.clip(resultado[:,:,1], -0.5957, 0.5957)
    Q = np.clip(resultado[:,:,2], -0.5226, 0.5226)
    return yiq_to_rgb(np.stack([Y,I,Q], axis=2))

def cuasi_resta_yiq_promediada(imgA: np.ndarray, imgB: np.ndarray) -> np.ndarray:
    yiqA = rgb_to_yiq(imgA)
    yiqB = rgb_to_yiq(imgB)
    resultado = (yiqA - yiqB) / 2
    return yiq_to_rgb(resultado)

def producto_rgb(imgA: np.ndarray, imgB: np.ndarray) -> np.ndarray:
    # Convertir a float para evitar overflow
    resultado = (imgA.astype(np.float32) * imgB.astype(np.float32)) / 255.0
    return np.clip(resultado, 0, 255).astype(np.uint8)

def cociente_rgb(imgA: np.ndarray, imgB: np.ndarray) -> np.ndarray:
    imgB_safe = imgB.astype(np.float32) + 1.0   # evitar división por cero
    resultado = (imgA.astype(np.float32) / imgB_safe) * 255.0
    return np.clip(resultado, 0, 255).astype(np.uint8)

def resta_absoluta_rgb(imgA: np.ndarray, imgB: np.ndarray) -> np.ndarray:
    resultado = np.abs(imgA.astype(np.int32) - imgB.astype(np.int32))
    return np.clip(resultado, 0, 255).astype(np.uint8)

def if_darker(imgA: np.ndarray, imgB: np.ndarray) -> np.ndarray:
    return np.minimum(imgA, imgB).astype(np.uint8)

def if_lighter(imgA: np.ndarray, imgB: np.ndarray) -> np.ndarray:
    return np.maximum(imgA, imgB).astype(np.uint8)