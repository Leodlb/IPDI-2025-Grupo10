
import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt

def linea_cromatica_Y(matriz_imagen: np.uint8,y):
    tamanio_matriz = matriz_imagen.shape
    linea = matriz_imagen[y]
    rojo = linea[:, 0]
    plt.plot(np.linspace(0,tamanio_matriz[1],tamanio_matriz[1]),linea)
    plt.show()


imagen = np.array([
    [ [255,   0,   0], [128,   0,   0], [ 64,   0,   0], [  0,   0,   0] ],  # fila 0
    [ [  0, 255,   0], [  0, 128,   0], [  0,  64,   0], [  0,   0,   0] ],  # fila 1
    [ [  0,   0, 255], [  0,   0, 128], [  0,   0,  64], [  0,   0,   0] ]   # fila 2
], dtype=np.uint8)

linea_cromatica_Y(imagen, 1)