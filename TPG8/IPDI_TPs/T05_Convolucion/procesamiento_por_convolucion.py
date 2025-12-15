import numpy as np
from PIL import Image
import math

def convolucion(imagen, kernel):
    """
    Aplica una convolución manual a una imagen (array numpy 2D) usando un kernel.
    Manejo de bordes: Repetir (copiar la última fila/columna válida).
    """
    # Asegurar que la imagen sea float para evitar desbordamientos durante el cálculo
    img_h, img_w = imagen.shape
    k_h, k_w = kernel.shape
    
    pad_h = k_h // 2
    pad_w = k_w // 2
    
    # Crear imagen con padding (bordes repetidos)
    # np.pad con mode='edge' repite el valor del borde
    img_padded = np.pad(imagen, ((pad_h, pad_h), (pad_w, pad_w)), mode='edge')
    
    output = np.zeros_like(imagen, dtype=np.float32)
    
    # Convolución manual
    # Iteramos sobre los píxeles de la imagen original
    for i in range(img_h):
        for j in range(img_w):
            # Extraer la región de interés (ROI)
            # La ROI en la imagen paddeada corresponde a [i:i+k_h, j:j+k_w]
            roi = img_padded[i:i+k_h, j:j+k_w]
            
            # Aplicar el kernel (multiplicación elemento a elemento y suma)
            val = np.sum(roi * kernel)
            output[i, j] = val
            
    return output

# --- 1. Pasabajos ---

def kernel_plano(size):
    """Retorna un kernel de promedio (Box Filter) de tamaño size x size."""
    return np.ones((size, size)) / (size * size)

def kernel_bartlett(size):
    """Retorna un kernel de Bartlett (triangular) de tamaño size x size."""
    # Crear vector triangular 1D
    # Ejemplo size 3: [1, 2, 1] / 4
    # Ejemplo size 5: [1, 2, 3, 2, 1] / 9
    
    if size % 2 == 0:
        raise ValueError("El tamaño debe ser impar")
        
    center = size // 2
    row = []
    for i in range(size):
        val = center + 1 - abs(center - i)
        row.append(val)
    
    row = np.array(row)
    # Producto externo para crear 2D
    kernel = np.outer(row, row)
    # Normalizar
    return kernel / np.sum(kernel)

def kernel_gaussiano(size, sigma=1.0):
    """Retorna un kernel Gaussiano de tamaño size x size."""
    if size % 2 == 0:
        raise ValueError("El tamaño debe ser impar")
        
    k = size // 2
    x, y = np.mgrid[-k:k+1, -k:k+1]
    g = np.exp(-(x**2 + y**2) / (2 * sigma**2))
    return g / g.sum()

# --- 2. Detectores de Bordes ---

def kernel_laplaciano(variante='v4'):
    """
    Retorna kernel Laplaciano.
    variante: 'v4' (cruz) o 'v8' (completo con diagonales)
    """
    if variante == 'v4':
        return np.array([[0, -1, 0],
                         [-1, 4, -1],
                         [0, -1, 0]])
    elif variante == 'v8':
        return np.array([[-1, -1, -1],
                         [-1, 8, -1],
                         [-1, -1, -1]])
    else:
        raise ValueError("Variante desconocida. Use 'v4' o 'v8'.")

def kernel_sobel(orientacion):
    """
    Retorna kernel Sobel para una de las 8 orientaciones.
    orientacion: 'N', 'S', 'E', 'W', 'NE', 'NW', 'SE', 'SW'
    """
    # Sobel base Gx (Bordes verticales, detecta cambios horizontales) -> W-E
    # -1 0 1
    # -2 0 2
    # -1 0 1
    
    # Sobel base Gy (Bordes horizontales, detecta cambios verticales) -> N-S
    # -1 -2 -1
    #  0  0  0
    #  1  2  1
    
    # Definimos los básicos
    S_N = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]]) # Norte (Top) - Detecta borde inferior? Usualmente Gy
    # Nota: La dirección suele referirse a hacia dónde crece el brillo o la dirección del gradiente.
    # Asumiremos la convención estándar de máscaras direccionales.
    
    kernels = {
        'N':  np.array([[-1, -2, -1], 
                        [ 0,  0,  0], 
                        [ 1,  2,  1]]),
        'S':  np.array([[ 1,  2,  1], 
                        [ 0,  0,  0], 
                        [-1, -2, -1]]),
        'E':  np.array([[-1,  0,  1], 
                        [-2,  0,  2], 
                        [-1,  0,  1]]),
        'W':  np.array([[ 1,  0, -1], 
                        [ 2,  0, -2], 
                        [ 1,  0, -1]]),
        'NE': np.array([[ 0, -1, -2], 
                        [ 1,  0, -1], 
                        [ 2,  1,  0]]), # Diagonal
        'NW': np.array([[-2, -1,  0], 
                        [-1,  0,  1], 
                        [ 0,  1,  2]]),
        'SE': np.array([[ 0,  1,  2], 
                        [-1,  0,  1], 
                        [-2, -1,  0]]),
        'SW': np.array([[ 2,  1,  0], 
                        [ 1,  0, -1], 
                        [ 0, -1, -2]])
    }
    
    return kernels.get(orientacion.upper())

# --- 3. Pasabanda y Pasaaltos ---

def kernel_pasa_altos(fc, size=3):
    """
    Crea un filtro pasa altos simple.
    Una forma común es: Identidad - PasaBajos.
    O usando un diseño específico (-1 alrededor, centro positivo).
    Para este ejercicio, usaremos un filtro High Pass básico de 3x3 sum=0.
    Si fc es específico, se requeriría un diseño más complejo (Windowed Sinc).
    
    Dado el requerimiento de fc=0.2 y 0.4, usaremos el método de Windowed Sinc 1D -> 2D
    para generar un kernel más preciso.
    """
    # Diseño simple usando Windowed Sinc para Pasa Bajos y luego conversión espectral
    # HighPass = Delta - LowPass
    
    # 1. Crear Low Pass con esa frecuencia de corte
    lp_kernel = kernel_sinc_windowed(fc, size)
    
    # 2. Crear Delta (Impulso unitario)
    delta = np.zeros_like(lp_kernel)
    center = size // 2
    delta[center, center] = 1.0
    
    # 3. Restar
    hp_kernel = delta - lp_kernel
    return hp_kernel

def kernel_pasa_banda(fc_low, fc_high, size=9):
    """
    Crea un filtro pasa banda.
    BandPass = LowPass(fc_high) - LowPass(fc_low)
    """
    lp_high = kernel_sinc_windowed(fc_high, size)
    lp_low = kernel_sinc_windowed(fc_low, size)
    
    bp_kernel = lp_high - lp_low
    return bp_kernel

def kernel_sinc_windowed(fc, size):
    """
    Genera un kernel pasabajos 2D usando ventana de Blackman o Hamming.
    fc: Frecuencia de corte normalizada (0.0 a 0.5).
    """
    if size % 2 == 0: size += 1
    center = size // 2
    
    # Crear kernel 1D
    x = np.arange(size) - center
    # Evitar división por cero
    # sinc(x) = sin(2*pi*fc*x) / (pi*x)
    # Nota: np.sinc incluye el pi, es sin(pi*x)/(pi*x). Ajustamos.
    
    # Usamos la definición matemática sinc(t) = sin(pi*t)/(pi*t) de numpy
    # Queremos corte en fc. La función sinc de numpy tiene cruces en enteros.
    # sin(2*pi*fc*x) / (pi*x) = 2*fc * sinc(2*fc*x)
    
    h = 2 * fc * np.sinc(2 * fc * x)
    
    # Ventana de Blackman para suavizar
    window = np.blackman(size)
    h = h * window
    
    # Normalizar ganancia unitaria en DC
    h = h / np.sum(h)
    
    # Convertir a 2D (Transformada separable -> h_2d = h_1d' * h_1d)
    # Esto crea un filtro con simetría circular aproximada (cuadrada en realidad si es separable)
    # Para simetría circular real se usa rotación, pero separable es estándar en PDI básico.
    kernel_2d = np.outer(h, h)
    return kernel_2d / np.sum(kernel_2d)


# --- Bloque de Prueba ---
if __name__ == "__main__":
    # Crear una imagen de prueba simple si no hay una
    print("Iniciando pruebas de convolución...")
    
    # Generar imagen de prueba (patrón de tablero)
    img_test = np.zeros((100, 100))
    img_test[25:75, 25:75] = 1.0 # Cuadrado blanco
    
    # Probar Convolución con Bartlett 5x5
    kb = kernel_bartlett(5)
    res_bartlett = convolucion(img_test, kb)
    print(f"Bartlett 5x5 aplicado. Shape: {res_bartlett.shape}")
    
    # Probar Sobel Norte
    ks = kernel_sobel('N')
    res_sobel = convolucion(img_test, ks)
    print(f"Sobel N aplicado. Max val: {np.max(res_sobel)}")
    
    print("Pruebas finalizadas.")
