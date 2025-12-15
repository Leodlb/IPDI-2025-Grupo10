from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

imagen_original = None
imagen_modificada = None
imagen_tk = None


def abrir_imagen(lbl_imagen_original):
    global imagen_original, imagen_tk

    ruta = filedialog.askopenfilename(
        title="Seleccionar imagen",
        filetypes=[("Archivos de imagen", "*.jpg *.png *.jpeg *.bmp *.gif")]
    )
    if not ruta:
        return

    try:
        imagen_original = Image.open(ruta).convert("RGB")
        mostrar_imagen(imagen_original, lbl_imagen_original)
        messagebox.showinfo("Éxito", f"Imagen abierta: {ruta}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir la imagen: {e}")


def modificar_imagen(lbl_imagen_modificada):
    global imagen_modificada, imagen_original

    if imagen_original is None:
        messagebox.showwarning("Advertencia", "Primero abre una imagen.")
        return

    # Copiar la original y modificar
    imagen_modificada = imagen_original.copy()
    pixeles = imagen_modificada.load()
    ancho, alto = imagen_modificada.size

    for x in range(ancho):
        for y in range(alto):
            r, g, b = pixeles[x, y]
            pixeles[x, y] = (255 - r, 255 - g, 255 - b)

    mostrar_imagen(imagen_modificada, lbl_imagen_modificada)
    messagebox.showinfo("Éxito", "Imagen modificada (colores invertidos).")


def guardar_imagen():
    global imagen_modificada

    if imagen_modificada is None:
        messagebox.showwarning("Advertencia", "No hay imagen modificada para guardar.")
        return

    ruta = filedialog.asksaveasfilename(
        defaultextension=".jpg",
        filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png"), ("BMP", "*.bmp")]
    )
    if not ruta:
        return

    try:
        imagen_modificada.save(ruta)
        messagebox.showinfo("Éxito", f"Imagen guardada en: {ruta}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar la imagen: {e}")


def mostrar_imagen(img, label_widget):
    global imagen_tk
    img_redimensionada = img.resize((500, 500)) 
    imagen_tk = ImageTk.PhotoImage(img_redimensionada)
    label_widget.configure(image=imagen_tk, text="") 
    label_widget.image = imagen_tk 
