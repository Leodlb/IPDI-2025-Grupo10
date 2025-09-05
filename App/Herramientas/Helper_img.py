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