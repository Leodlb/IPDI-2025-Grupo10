import imageio
import numpy as np
import matplotlib.pyplot as plt

def cargar_imagen(ruta):
    """Carga una imagen desde un archivo."""
    return imageio.imread(ruta)

def normalizar_imagen(img):
    """Normaliza la imagen a valores entre 0 y 1."""
    return np.clip(img / 255., 0., 1.)

def rgb_a_yiq(img):
    """Convierte una imagen RGB a YIQ."""
    yiq = np.zeros(img.shape)
    yiq[:, :, 0] = 0.229 * img[:, :, 0] + 0.587 * img[:, :, 1] + 0.114 * img[:, :, 2]
    yiq[:, :, 1] = 0.595716 * img[:, :, 0] - 0.274453 * img[:, :, 1] - 0.321263 * img[:, :, 2]
    yiq[:, :, 2] = 0.211456 * img[:, :, 0] - 0.522591 * img[:, :, 1] + 0.311135 * img[:, :, 2]
    return yiq

def verificar_rangos_yiq(yiq):
    """Verifica y recorta los valores de YIQ a sus rangos válidos."""
    if np.any(yiq[:, :, 0] > 1):
        print("Advertencia: Valores de Y' mayores que 1 detectados. Se recortarán a 1.")
        yiq[:, :, 0] = np.clip(yiq[:, :, 0], 0, 1)

    if np.any(yiq[:, :, 1] < -0.5957) or np.any(yiq[:, :, 1] > 0.5957):
        print("Advertencia: Valores de I' fuera del rango [-0.5957, 0.5957] detectados. Se recortarán al rango.")
        yiq[:, :, 1] = np.clip(yiq[:, :, 1], -0.5957, 0.5957)

    if np.any(yiq[:, :, 2] < -0.5226) or np.any(yiq[:, :, 2] > 0.5226):
        print("Advertencia: Valores de Q' fuera del rango [-0.5226, 0.5226] detectados. Se recortarán al rango.")
        yiq[:, :, 2] = np.clip(yiq[:, :, 2], -0.5226, 0.5226)
    return yiq

def yiq_a_rgb(yiq):
    """Convierte una imagen YIQ a RGB."""
    rgb = np.zeros(yiq.shape)
    rgb[:, :, 0] = yiq[:, :, 0] + 0.9663 * yiq[:, :, 1] + 0.6210 * yiq[:, :, 2]
    rgb[:, :, 1] = yiq[:, :, 0] - 0.2721 * yiq[:, :, 1] - 0.6474 * yiq[:, :, 2]
    rgb[:, :, 2] = yiq[:, :, 0] - 1.1070 * yiq[:, :, 1] + 1.7046 * yiq[:, :, 2]
    return rgb

def graficar_rgb_yiq(img, yiq):
    """Grafica los canales YIQ y la imagen original."""
    titles = ['Imagen Original', 'Y (Luminancia)', 'I (Crominancia)', 'Q (Color)']
    plt.figure(figsize=(8, 4))
    plt.subplot(1, 4, 1)
    plt.imshow(img,'gray')
    plt.title(titles[0])
    plt.axis('off')

    for i in range(3):
        plt.subplot(1, 4, i + 2)
        plt.imshow(yiq[:, :, i], 'gray', vmin=np.min(yiq[:, :, i]), vmax=np.max(yiq[:, :, i]))
        plt.title(titles[i + 1])
        plt.axis('off')
    plt.show()

ruta_imagen = "./img/chelsea.png"
img = cargar_imagen(ruta_imagen)
print(img.shape, img.dtype)
img = normalizar_imagen(img)
yiq = rgb_a_yiq(img)
yiq = verificar_rangos_yiq(yiq)
rgb = yiq_a_rgb(yiq)
rgb_bytes = (rgb * 255).astype(np.uint8)
graficar_rgb_yiq(img, rgb_bytes)

