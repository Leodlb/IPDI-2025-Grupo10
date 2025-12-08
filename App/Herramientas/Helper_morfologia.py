from Helper_img import yiq_to_rgb, rgb_to_yiq
import numpy as np
import cv2

from PIL import Image
import matplotlib.pyplot as plt

# 1. RGB → Gris por promedio

def rgb_to_gray_mean(img_rgb):
    """
    Convierte una imagen RGB a escala de grises usando el promedio de los canales.
    img_rgb: array (H, W, 3)
    return: array (H, W) en rango 0-255
    """
    if img_rgb.ndim != 3 or img_rgb.shape[2] != 3:
        raise ValueError("La imagen debe ser RGB con forma (H, W, 3)")
    
    return img_rgb.mean(axis=2).astype(np.uint8)


# ----------------------------------------
# 2. RGB → YIQ → Gris usando canal Y
# ----------------------------------------
def rgb_to_gray_yiq(img_rgb):
    """
    Convierte RGB a YIQ y devuelve el canal Y en rango 0-255.
    """
    if img_rgb.ndim != 3 or img_rgb.shape[2] != 3:
        raise ValueError("La imagen debe ser RGB con forma (H, W, 3)")
    
    yiq = rgb_to_yiq(img_rgb)  # Devuelve Y entre 0 y 1
    Y = yiq[:, :, 0]           # Canal de luminancia

    # Escalar a rango 0-255
    Y = (Y * 255.0).clip(0, 255)

    return Y.astype(np.uint8)




# 3. Binarizar imagen (requiere gris)

def binarize(img_gray, threshold):
    """
    Binariza una imagen en escala de grises.
    img_gray: array (H, W) en 0–255
    threshold: valor entre 0 y 255
    return: array (H, W) con valores 0 o 255
    """
    if img_gray.ndim != 2:
        raise ValueError("La imagen debe ser en blanco y negro (H, W).")

    if not (0 <= threshold <= 255):
        raise ValueError("El umbral debe estar entre 0 y 255.")

    return np.where(img_gray >= threshold, 255, 0).astype(np.uint8)


# 4. Invertir imagen

def invert_image(img):
    """
    Invierte los valores de una imagen (RGB o BW).
    img: array (H, W) o (H, W, 3)
    return: array invertida
    """
    return np.abs(255 - img)




def mostrar_img(titulo, img):
    """
    Muestra una imagen que puede ser RGB o gris.
    """
    plt.figure()
    if img.ndim == 2:
        plt.imshow(img, cmap="gray")
    else:
        plt.imshow(img)
    plt.title(titulo)
    plt.axis("off")



#--------------------------------------
#------------- CON CV2 ----------------
#--------------------------------------

def erosionar_cv(img_gray, kernel):
    """
    Erosiona una imagen en escala de grises usando cv2.
    img_gray : (H, W) uint8
    kernel   : matriz con 0/1
    """
    if img_gray.ndim != 2:
        raise ValueError("La imagen debe estar en escala de grises (H, W)")

    # Asegurar uint8
    kern = kernel.astype(np.uint8)

    return cv2.erode(img_gray, kern, iterations=1)

def dilatar_cv(img_gray, kernel):
    """
    Dilata una imagen en escala de grises usando cv2.
    img_gray : (H, W) uint8
    kernel   : matriz con 0/1
    """
    if img_gray.ndim != 2:
        raise ValueError("La imagen debe estar en escala de grises (H, W)")

    kern = kernel.astype(np.uint8)

    return cv2.dilate(img_gray, kern, iterations=1)

def apertura_cv(img_gray, kernel):
    kern = kernel.astype(np.uint8)
    return cv2.morphologyEx(img_gray, cv2.MORPH_OPEN, kern)

def cierre_cv(img_gray, kernel):
    kern = kernel.astype(np.uint8)
    return cv2.morphologyEx(img_gray, cv2.MORPH_CLOSE, kern)


#-------------------------------------
# --------------KERNELS---------------
#-------------------------------------

def kernel_cuadrado(tamano):
    """
    Crea un kernel cuadrado de 1’s.
    tamano: lado del kernel (n)
    return: array (n, n) de 1’s
    """
    return np.ones((tamano, tamano), dtype=np.uint8)

def kernel_circular(radio):
    """
    Crea un kernel circular (disco) con 1's.
    radio: radio del círculo
    return: array (2*radio+1, 2*radio+1)
    """
    d = 2 * radio + 1
    kernel = np.zeros((d, d), dtype=np.uint8)

    cx, cy = radio, radio
    for i in range(d):
        for j in range(d):
            if (i - cx)**2 + (j - cy)**2 <= radio**2:
                kernel[i, j] = 1

    return kernel


def erosionar(img, kernel):
    """
    Erosion: toma el mínimo en la vecindad indicada por el kernel.
    img: imagen gris o binaria (H, W)
    kernel: matriz de 0/1 (kH, kW)
    """
    kh, kw = kernel.shape
    ph, pw = kh // 2, kw // 2

    H, W = img.shape
    salida = np.zeros((H, W), dtype=np.uint8)

    padded = np.pad(img, ((ph, ph), (pw, pw)), mode='edge')

    for y in range(H):
        for x in range(W):
            region = padded[y:y+kh, x:x+kw]
            valores = region[kernel == 1]
            salida[y, x] = np.min(valores)

    return salida


def dilatar(img, kernel):
    """
    Dilation: toma el máximo en la vecindad indicada por el kernel.
    img: imagen gris o binaria (H, W)
    kernel: matriz de 0/1 (kH, kW)
    """
    kh, kw = kernel.shape
    ph, pw = kh // 2, kw // 2

    H, W = img.shape
    salida = np.zeros((H, W), dtype=np.uint8)

    # Pad
    padded = np.pad(img, ((ph, ph), (pw, pw)), mode='edge')

    for y in range(H):
        for x in range(W):
            region = padded[y:y+kh, x:x+kw]
            valores = region[kernel == 1]
            salida[y, x] = np.max(valores)

    return salida


# ---------------------------------------------------------
# PRUEBAS 
# ---------------------------------------------------------

"""
img_color = Image.open("F:\escritorio\Quizas Basura\luna.png").convert("RGB")

if img_color is None:
    print("Error: no se pudo cargar la imagen. Asegurate de que 'mi_imagen.jpg' exista.")
else:
    # 2) Convertir a gris
    img_gray = binarize(rgb_to_gray_yiq(np.array(img_color)),150)

    # 3) Definir kernels
    k_cuad = kernel_cuadrado(5)
    k_circ = kernel_circular(3)

    # 4) Aplicar operaciones
    ero_cuad = erosionar(img_gray, k_cuad)
    dil_cuad = dilatar(img_gray, k_cuad)

    ero_circ = erosionar(img_gray, k_circ)
    dil_circ = dilatar(img_gray, k_circ)

    # 5) Mostrar resultados
    plt.figure(figsize=(12, 10))

    plt.subplot(2, 3, 1)
    plt.title("Original")
    plt.imshow(img_gray, cmap="gray")
    plt.axis("off")

    plt.subplot(2, 3, 2)
    plt.title("Erosión cuadrado")
    plt.imshow(ero_cuad, cmap="gray")
    plt.axis("off")

    plt.subplot(2, 3, 3)
    plt.title("Dilatación cuadrado")
    plt.imshow(dil_cuad, cmap="gray")
    plt.axis("off")

    plt.subplot(2, 3, 4)
    plt.title("Erosión circular")
    plt.imshow(ero_circ, cmap="gray")
    plt.axis("off")

    plt.subplot(2, 3, 5)
    plt.title("Dilatación circular")
    plt.imshow(dil_circ, cmap="gray")
    plt.axis("off")

    plt.tight_layout()
    plt.show()
    """
"""
# ---------------------------------------------------------
# PRUEBAS ;v
# ---------------------------------------------------------



if __name__ == "__main__":
    # ---- 1. Cargar una imagen real ----
    ruta = "F:\escritorio\Quizas Basura\Pascualina.png"  # Cambiá la ruta por la imagen que subas
    img = Image.open(ruta).convert("RGB")

    # ---- 2. Convertir a array ----
    imagen = np.array(img)

    # ---- 3. Mostrar en consola el array de la imagen ----
    print("ARRAY DE LA IMAGEN ORIGINAL:")
    print(imagen)
    print("Forma:", imagen.shape)
    print("Tipo:", imagen.dtype)

    # ---- 4. Procesar con tus funciones ----
    gris_mean = rgb_to_gray_mean(imagen)
    gris_yiq = rgb_to_gray_yiq(imagen)
    binaria = binarize(gris_mean, 128)
    invertida = invert_image(imagen)

    # ---- 5. Mostrar todo como imágenes ----
    mostrar_img("Original", imagen)
    mostrar_img("Gris (promedio)", gris_mean)
    mostrar_img("Gris (YIQ - canal Y)", gris_yiq)
    mostrar_img("Binaria", binaria)
    mostrar_img("Invertida", invertida)

    plt.show()"""