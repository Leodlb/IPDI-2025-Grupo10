import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


#Para implementar en el codigo
#import my_functions as mf
#import importlib
#importlib.reload(mf)


# =========================
# MATRIZ YIQ (constante)
# =========================
MAT_YIQ = np.array([[0.299,     0.587,    0.114],
                    [0.595716, -0.274453, -0.321263],
                    [0.211456, -0.522591,  0.311135]])
MAT_YIQ_INV = np.linalg.inv(MAT_YIQ)

# =========================
# HELPERS DE TIPO / ESCALA
# =========================
def _as_float01(img):
    """Devuelve una copia float en rango [0,1] a partir de uint8 o float arbitrario."""
    arr = np.asarray(img)
    if np.issubdtype(arr.dtype, np.integer):
        return arr.astype(np.float32) / 255.0
    # float: si el máximo es >1 asumimos que está en 0-255 guardado en float
    if arr.dtype.kind == 'f':
        mx = arr.max() if arr.size > 0 else 1.0
        if mx > 1.1:
            return arr.astype(np.float32) / 255.0
        else:
            return arr.astype(np.float32).copy()
    # otros (por seguridad)
    return arr.astype(np.float32)

def _prefer_uint8_like(ref_img):
    """Devuelve True si es preferible devolver uint8 (si la referencia es int o float>1)."""
    arr = np.asarray(ref_img)
    if np.issubdtype(arr.dtype, np.integer):
        return True
    if arr.dtype.kind == 'f' and arr.size>0 and arr.max() > 1.1:
        return True
    return False

def _to_output(img_float01, ref_img):
    """Convierte img_float01 (float [0,1]) al tipo de salida según ref_img."""
    if _prefer_uint8_like(ref_img):
        return np.clip(img_float01 * 255.0, 0, 255).astype(np.uint8)
    else:
        return np.clip(img_float01, 0.0, 1.0)

# =========================
# RGB <-> YIQ (trabajan con floats 0..1)
# =========================
def rgb2yiq(img):
    """Asume img en float [0,1] o lo transforma y devuelve YIQ (float, Y puede estar ~[0,1])."""
    f = _as_float01(img)
    yiq = (f.reshape((-1, 3)) @ MAT_YIQ.T).reshape(f.shape)
    return yiq

def yiq2rgb(yiq):
    """Convierte YIQ a RGB en float y lo recorta a [0,1]."""
    rgb = (yiq.reshape((-1, 3)) @ MAT_YIQ_INV.T).reshape(yiq.shape)
    return np.clip(rgb, 0.0, 1.0)

# =========================
# OPERACIONES (robustas a dtype/escala)
# =========================

def sum_rgb(img1, img2, method):
    a = _as_float01(img1)
    b = _as_float01(img2)
    if method == "clamp":
        c = a + b
        c = np.clip(c, 0.0, 1.0)
    elif method == "mean":
        c = (a + b) / 2.0
    else:
        raise ValueError("method debe ser 'clamp' o 'mean'")
    return _to_output(c, img1)

def diff_rgb(img1, img2, method):
    a = _as_float01(img1)
    b = _as_float01(img2)
    if method == "clamp":
        d = a - b
        d = np.clip(d, 0.0, 1.0)
    elif method == "mean":
        d = (a - b) / 2.0
        d = np.clip(d, 0.0, 1.0)
    else:
        raise ValueError("method debe ser 'clamp' o 'mean'")
    return _to_output(d, img1)

def sum_yiq(img1, img2, method):
    a = _as_float01(img1)
    b = _as_float01(img2)
    yiq1 = rgb2yiq(a)
    yiq2 = rgb2yiq(b)

    Y = yiq1[..., 0] + yiq2[..., 0]
    if method == "clamp":
        Y = np.clip(Y, 0.0, 1.0)
    else:
        Y = (yiq1[..., 0] + yiq2[..., 0]) / 2.0

    denom = (yiq1[..., 0] + yiq2[..., 0]) + 1e-12
    I = (yiq1[..., 1] * yiq1[..., 0] + yiq2[..., 1] * yiq2[..., 0]) / denom
    Q = (yiq1[..., 2] * yiq1[..., 0] + yiq2[..., 2] * yiq2[..., 0]) / denom

    yiq_c = np.stack([Y, I, Q], axis=-1)
    rgb_c = yiq2rgb(yiq_c)
    return _to_output(rgb_c, img1)

def diff_yiq(img1, img2, method):
    a = _as_float01(img1)
    b = _as_float01(img2)
    yiq1 = rgb2yiq(a)
    yiq2 = rgb2yiq(b)

    Y = yiq1[..., 0] - yiq2[..., 0]
    if method == "clamp":
        Y = np.clip(Y, 0.0, 1.0)
    else:
        Y = (yiq1[..., 0] - yiq2[..., 0]) / 2.0

    denom = np.abs(yiq1[..., 0] - yiq2[..., 0]) + 1e-12
    I = (yiq1[..., 1] * yiq1[..., 0] - yiq2[..., 1] * yiq2[..., 0]) / denom
    Q = (yiq1[..., 2] * yiq1[..., 0] - yiq2[..., 2] * yiq2[..., 0]) / denom

    yiq_c = np.stack([Y, I, Q], axis=-1)
    rgb_c = yiq2rgb(yiq_c)
    return _to_output(rgb_c, img1)

def product(img1, img2):
    a = _as_float01(img1)
    b = _as_float01(img2)
    p = a * b          # ya está en [0,1]
    return _to_output(p, img1)

def quotient(img1, img2):
    a = _as_float01(img1)
    b = _as_float01(img2)
    q = a / (b + 1e-12)
    q = np.clip(q, 0.0, 1.0)
    return _to_output(q, img1)

def abs_diff(img1, img2):
    a = _as_float01(img1)
    b = _as_float01(img2)
    d = np.abs(a - b)
    return _to_output(d, img1)

def if_darker(img1, img2):
    a = _as_float01(img1)
    b = _as_float01(img2)
    yiq1 = rgb2yiq(a); yiq2 = rgb2yiq(b)
    lum1 = yiq1[..., 0]; lum2 = yiq2[..., 0]
    mask = lum1 < lum2
    out = np.where(mask[..., None], a, b)
    return _to_output(out, img1)

def if_lighter(img1, img2):
    a = _as_float01(img1)
    b = _as_float01(img2)
    yiq1 = rgb2yiq(a); yiq2 = rgb2yiq(b)
    lum1 = yiq1[..., 0]; lum2 = yiq2[..., 0]
    mask = lum1 > lum2
    out = np.where(mask[..., None], a, b)
    return _to_output(out, img1)
