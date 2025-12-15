import imageio
import numpy as np
import matplotlib.pyplot as plt

im = imageio.imread('imageio:chelsea.png')/255.

dark_umbral = 0.20
dark_mask = (im[:, :, 0] < dark_umbral) & (im[:, :, 1] < dark_umbral) & (im[:, :, 2] < dark_umbral)

#Conectar pixeles cercanos
def conectar_pixeles(mask, distance=5):
    connected_mask = mask.copy()
    h, w = mask.shape
    #recorrer mascara
    for i in range(h):
        for j in range(w):
            if mask[i, j]:
                # Marcar en true a x distancia del pixel true original
                for di in range(-distance, distance+1):
                    for dj in range(-distance, distance+1):
                        ni, nj = i + di, j + dj
                        if 0 <= ni < h and 0 <= nj < w:
                            connected_mask[ni, nj] = True
    return connected_mask

connected_mask = conectar_pixeles(dark_mask, distance=5)

#marcar los objetos mas grandes
def marcar_ojos(mask):
    labeled = np.zeros_like(mask, dtype=int)
    current_label = 1
    tamanio_ojos = {}
    
    for i in range(mask.shape[0]):
        for j in range(mask.shape[1]):
            if mask[i, j] and labeled[i, j] == 0:
                stack = [(i, j)]
                labeled[i, j] = current_label
                size = 1
                
                while stack:
                    x, y = stack.pop()
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = x + dx, y + dy
                        if (0 <= nx < mask.shape[0] and 
                            0 <= ny < mask.shape[1] and 
                            mask[nx, ny] and labeled[nx, ny] == 0):
                            labeled[nx, ny] = current_label
                            stack.append((nx, ny))
                            size += 1
                
                tamanio_ojos[current_label] = size
                current_label += 1

    if not tamanio_ojos:
        return mask
    
    sorted_components = sorted(tamanio_ojos.items(), key=lambda x: x[1], reverse=True)
    largest_labels = [label for label, size in sorted_components[:2]]

    #Mascara con los componentes grandes
    result_mask = np.isin(labeled, largest_labels)
    return result_mask


filtered_mask = marcar_ojos(connected_mask)

#Aplicar mascara
segmented_eyes = im.copy()
for i in range(3):
    segmented_eyes[:, :, i] = im[:, :, i] * filtered_mask

# Mostrar resultados
plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
plt.imshow(im)
plt.title('Imagen Original')
plt.axis('off')

plt.subplot(1, 3, 2)
plt.imshow(filtered_mask, cmap='gray')
plt.title('Máscara con los 2 Objetos Más Grandes')
plt.axis('off')

plt.subplot(1, 3, 3)
plt.imshow(segmented_eyes)
plt.title('Ojos Segmentados')
plt.axis('off')

plt.tight_layout()
plt.show()