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

#Cosas pa dos img

def igualar_tamanio_izq_sup(im1: np.uint8, im2: np.uint8):
    tamanio1 = np.array(im1.shape)
    tamanio2 = np.array(im2.shape)
    tamanio = np.where(tamanio1 < tamanio2, tamanio1, tamanio2)
    return(im1[:tamanio[0],:tamanio[1],:tamanio[2]], im2[:tamanio[0],:tamanio[1],:tamanio[2]])

def array_img_if_darker(im1: np.uint8, im2: np.uint8):
    im1, im2 = igualar_tamanio_izq_sup(im1, im2)
    return np.where(im1 > im2, im2, im1)

def array_img_if_ligther(im1: np.uint8, im2: np.uint8):
    im1, im2 = igualar_tamanio_izq_sup(im1, im2)
    return np.where(im1 < im2, im2, im1)

def array_img_prod(im1: np.uint8, im2: np.uint8):
    im1, im2 = igualar_tamanio_izq_sup(im1, im2)
    im1 = np.clip(im1/255, 0., 1.)
    im2 = np.clip(im2/255, 0., 1.)

    return np.floor((im1* im2) * 255)

def array_img_abs_rest(im1: np.uint8, im2: np.uint8):
    im1, im2 = igualar_tamanio_izq_sup(im1, im2)
    return np.abs(im1-im2)

"""
imagen1 = Image.open("G://Escritorio//flores.jpeg")
imagen2 = Image.open("G://Escritorio//luna2.png")
plt.imshow(array_img_abs_rest(np.array(imagen1), np.array(imagen2)))
plt.show()
"""