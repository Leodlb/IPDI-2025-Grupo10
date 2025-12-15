import customtkinter as ctk
import funciones_interfaz as fi



ctk.set_appearance_mode("red")
ctk.set_default_color_theme("blue") 

ventana = ctk.CTk()
ventana.title("Gestor de Imagenes IPDI- Grupo 8")
ventana.geometry("1600x900")

#Frame izquierda
frame_menu = ctk.CTkFrame(ventana, width=200)
frame_menu.pack(side="left", fill="y", padx=5, pady=5)

# Menú desplegable: Imagen
menu_imagen = ctk.CTkOptionMenu(
    frame_menu,
    values=["Subir Imagen", "Guardar Imagen"],
    command=lambda opcion: (
        fi.abrir_imagen(lbl_imagen_original) if opcion == "Subir Imagen" else fi.guardar_imagen()
    )
)
menu_imagen.set("Imagen")
menu_imagen.pack(pady=10, fill="x")

# Menú desplegable de opciones
menu_opciones = ctk.CTkOptionMenu(
    frame_menu,
    values=["Modificar Imagen", "Opción 2", "Opción 3"], 
    command=lambda opcion: (
        fi.modificar_imagen(lbl_imagen_modificada) if opcion == "Modificar Imagen" else "esta"
    )
)
menu_opciones.set("Opciones de Imagen")
menu_opciones.pack(pady=10, fill="x")

# Salir
btn_salir = ctk.CTkButton(frame_menu, text="Salir", command=ventana.destroy)
btn_salir.pack(side="bottom", pady=20, fill="x")

# Frame principal (imágenes)
frame_imagenes = ctk.CTkFrame(ventana)
frame_imagenes.pack(expand=True, fill="both", padx=10, pady=10)

lbl_imagen_original = ctk.CTkLabel(frame_imagenes, text="Imagen Original")
lbl_imagen_original.pack(side="left", padx=50)

lbl_imagen_modificada = ctk.CTkLabel(frame_imagenes, text="Imagen Modificada")
lbl_imagen_modificada.pack(side="right", padx=50)

ventana.mainloop()
