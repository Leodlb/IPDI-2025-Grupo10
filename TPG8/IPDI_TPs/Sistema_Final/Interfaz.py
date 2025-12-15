import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import funciones_interfaz as fi

# Configuración de colores modernos
COLORS = {
    "primary": "#2563eb",
    "secondary": "#7c3aed",
    "success": "#10b981",
    "warning": "#f59e0b",
    "danger": "#ef4444",
    "dark": "#1f2937",
    "light": "#f3f4f6",
    "accent": "#06b6d4",
    "hover_primary": "#1d4ed8",
    "hover_success": "#059669"
}

# --------------------------------------
# Sistema de Visualización Dinámica
# --------------------------------------
class DynamicImageDisplay:
    """Gestiona la visualización dinámica de imágenes según el contexto del menú"""
    
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.current_mode = None
        
        # Frames para diferentes modos
        self.frame_single = None  # 1 imagen original + 1 procesada
        self.frame_dual = None    # 2 imágenes + 1 resultado
        
        # Labels de imagen
        self.lbl_original = None
        self.lbl_secondary = None
        self.lbl_processed = None
        
        self.crear_frames()
    
    def crear_frames(self):
        # Frame para modo single (2 columnas)
        self.frame_single = ctk.CTkFrame(self.parent_frame, fg_color="transparent")
        
        frame_single_top = ctk.CTkFrame(self.frame_single, fg_color="transparent")
        frame_single_top.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Original
        frame_orig = ctk.CTkFrame(frame_single_top)
        frame_orig.pack(side="left", fill="both", expand=True, padx=5)
        ctk.CTkLabel(frame_orig, text="📷 Imagen Original", font=("Arial", 14, "bold")).pack(pady=5)
        self.lbl_original_single = ctk.CTkLabel(frame_orig, text="")
        self.lbl_original_single.pack(pady=10, fill="both", expand=True)
        
        # Procesada
        frame_proc = ctk.CTkFrame(frame_single_top)
        frame_proc.pack(side="right", fill="both", expand=True, padx=5)
        ctk.CTkLabel(frame_proc, text="✨ Imagen Procesada", font=("Arial", 14, "bold")).pack(pady=5)
        self.lbl_processed_single = ctk.CTkLabel(frame_proc, text="")
        self.lbl_processed_single.pack(pady=10, fill="both", expand=True)
        
        # Frame para modo dual (3 paneles)
        self.frame_dual = ctk.CTkFrame(self.parent_frame, fg_color="transparent")
        
        frame_dual_top = ctk.CTkFrame(self.frame_dual, fg_color="transparent")
        frame_dual_top.pack(fill="both", expand=True, padx=10, pady=(10, 5))
        
        # Imagen 1
        frame_img1 = ctk.CTkFrame(frame_dual_top)
        frame_img1.pack(side="left", fill="both", expand=True, padx=5)
        ctk.CTkLabel(frame_img1, text="📷 Imagen 1", font=("Arial", 14, "bold")).pack(pady=5)
        self.lbl_img1 = ctk.CTkLabel(frame_img1, text="")
        self.lbl_img1.pack(pady=10, fill="both", expand=True)
        
        # Imagen 2
        frame_img2 = ctk.CTkFrame(frame_dual_top)
        frame_img2.pack(side="right", fill="both", expand=True, padx=5)
        ctk.CTkLabel(frame_img2, text="📷 Imagen 2", font=("Arial", 14, "bold")).pack(pady=5)
        self.lbl_img2 = ctk.CTkLabel(frame_img2, text="")
        self.lbl_img2.pack(pady=10, fill="both", expand=True)
        
        # Resultado
        frame_dual_bottom = ctk.CTkFrame(self.frame_dual, fg_color="transparent")
        frame_dual_bottom.pack(fill="both", expand=True, padx=10, pady=(5, 10))
        
        frame_result = ctk.CTkFrame(frame_dual_bottom)
        frame_result.pack(fill="both", expand=True, padx=5)
        ctk.CTkLabel(frame_result, text="✨ Resultado", font=("Arial", 14, "bold")).pack(pady=5)
        self.lbl_result = ctk.CTkLabel(frame_result, text="")
        self.lbl_result.pack(pady=10, fill="both", expand=True)
    
    def set_mode(self, mode):
        """Cambia el modo de visualización: 'single' o 'dual'"""
        if self.current_mode == mode:
            return
        
        self.current_mode = mode
        
        # Ocultar ambos frames
        self.frame_single.pack_forget()
        self.frame_dual.pack_forget()
        
        # Mostrar el frame correspondiente
        if mode == "single":
            self.frame_single.pack(fill="both", expand=True)
        elif mode == "dual":
            self.frame_dual.pack(fill="both", expand=True)
    
    def get_labels(self):
        """Retorna los labels según el modo actual"""
        if self.current_mode == "single":
            return {
                "original": self.lbl_original_single,
                "processed": self.lbl_processed_single
            }
        elif self.current_mode == "dual":
            return {
                "img1": self.lbl_img1,
                "img2": self.lbl_img2,
                "result": self.lbl_result
            }
        return {}


# --------------------------------------
# Menú: Espacios Cromáticos
# --------------------------------------
class ColorSpaceMenu:
    def __init__(self, parent_frame, display_system):
        self.parent_frame = parent_frame
        self.display = display_system
        self.frame_menu = ctk.CTkFrame(parent_frame)
        
        # Variables
        self.var_operation = ctk.StringVar(value="Mostrar RGB")
        self.checkboxes_rgb = {}
        self.checkboxes_yiq = {}
        self.canales_rgb = {"R": False, "G": False, "B": False}
        self.canales_yiq = {"Y": False, "I": False, "Q": False}
        
        self.crear_widgets()
    
    def crear_widgets(self):
        ctk.CTkLabel(self.frame_menu, text="🎨 Espacios Cromáticos", 
                    font=("Arial", 16, "bold")).pack(pady=10)
        
        # Botón cargar imagen
        btn_load = ctk.CTkButton(self.frame_menu, text="📁 Subir Imagen",
                                command=self.cargar_imagen,
                                fg_color=COLORS["primary"], hover_color=COLORS["hover_primary"])
        btn_load.pack(pady=5, fill="x", padx=10)
        
        # Selector de operación
        ctk.CTkLabel(self.frame_menu, text="Operación:").pack(pady=(10,0))
        operations = ["Mostrar RGB", "Cambio a YIQ", "Invertir Colores"]
        combo = ctk.CTkOptionMenu(self.frame_menu, values=operations,
                                  variable=self.var_operation,
                                  command=self.actualizar_opciones)
        combo.pack(pady=5, fill="x", padx=10)
        
        # Frame para checkboxes RGB
        self.frame_rgb = ctk.CTkFrame(self.frame_menu, fg_color="transparent")
        ctk.CTkLabel(self.frame_rgb, text="Canales RGB:").pack(pady=5)
        for canal in ["R", "G", "B"]:
            var = ctk.BooleanVar()
            cb = ctk.CTkCheckBox(self.frame_rgb, text=canal, variable=var,
                                command=lambda c=canal: self.toggle_rgb(c))
            cb.pack(anchor="w", padx=20)
            self.checkboxes_rgb[canal] = var
        
        # Frame para checkboxes YIQ
        self.frame_yiq = ctk.CTkFrame(self.frame_menu, fg_color="transparent")
        ctk.CTkLabel(self.frame_yiq, text="Canales YIQ:").pack(pady=5)
        for canal in ["Y", "I", "Q"]:
            var = ctk.BooleanVar()
            cb = ctk.CTkCheckBox(self.frame_yiq, text=canal, variable=var,
                                command=lambda c=canal: self.toggle_yiq(c))
            cb.pack(anchor="w", padx=20)
            self.checkboxes_yiq[canal] = var
        
        # Botón aplicar
        btn_apply = ctk.CTkButton(self.frame_menu, text="✨ Aplicar",
                                 command=self.aplicar_operacion,
                                 fg_color=COLORS["success"], hover_color=COLORS["hover_success"])
        btn_apply.pack(pady=10, fill="x", padx=10)
        
        # Botón guardar
        btn_save = ctk.CTkButton(self.frame_menu, text="💾 Guardar Imagen Modificada",
                                command=fi.guardar_imagen,
                                fg_color=COLORS["warning"])
        btn_save.pack(pady=5, fill="x", padx=10)
    
    def cargar_imagen(self):
        labels = self.display.get_labels()
        fi.abrir_imagen(labels.get("original"))
    
    def actualizar_opciones(self, operation):
        self.frame_rgb.pack_forget()
        self.frame_yiq.pack_forget()
        
        if operation == "Mostrar RGB":
            self.frame_rgb.pack(pady=10, fill="x")
        elif operation == "Cambio a YIQ":
            self.frame_yiq.pack(pady=10, fill="x")
    
    def toggle_rgb(self, canal):
        self.canales_rgb[canal] = self.checkboxes_rgb[canal].get()
    
    def toggle_yiq(self, canal):
        self.canales_yiq[canal] = self.checkboxes_yiq[canal].get()
    
    def aplicar_operacion(self):
        labels = self.display.get_labels()
        operation = self.var_operation.get()
        
        if operation == "Mostrar RGB":
            fi.mostrar_canales_rgb(labels.get("processed"), self.canales_rgb)
        elif operation == "Cambio a YIQ":
            fi.mostrar_canales_yiq(labels.get("processed"), self.canales_yiq)
        elif operation == "Invertir Colores":
            fi.invertir_colores(labels.get("processed"))
    
    def mostrar(self):
        self.display.set_mode("single")
        self.frame_menu.pack(fill="both", expand=True, padx=5, pady=5)
    
    def ocultar(self):
        self.frame_menu.pack_forget()


# --------------------------------------
# Menú: Aritmética de Píxeles
# --------------------------------------
class PixelArithmeticMenu:
    def __init__(self, parent_frame, display_system):
        self.parent_frame = parent_frame
        self.display = display_system
        self.frame_menu = ctk.CTkFrame(parent_frame)
        
        self.var_operation = ctk.StringVar(value="Cuasi suma RGB (clamp)")
        self.crear_widgets()
    
    def crear_widgets(self):
        ctk.CTkLabel(self.frame_menu, text="🔢 Aritmética de Píxeles",
                    font=("Arial", 16, "bold")).pack(pady=10)
        
        # Botones de carga
        btn_load1 = ctk.CTkButton(self.frame_menu, text="📁 Subir Imagen 1",
                                 command=self.cargar_imagen1,
                                 fg_color=COLORS["primary"], hover_color=COLORS["hover_primary"])
        btn_load1.pack(pady=5, fill="x", padx=10)
        
        btn_load2 = ctk.CTkButton(self.frame_menu, text="📁 Subir Imagen 2",
                                 command=self.cargar_imagen2,
                                 fg_color=COLORS["secondary"])
        btn_load2.pack(pady=5, fill="x", padx=10)
        
        # Selector de operación
        ctk.CTkLabel(self.frame_menu, text="Operación:").pack(pady=(10,0))
        operations = [
            "Cuasi suma RGB (clamp)",
            "Cuasi resta RGB (clamp)",
            "Cuasi suma YIQ (clamp)",
            "If Darker",
            "If Lighter"
        ]
        combo = ctk.CTkOptionMenu(self.frame_menu, values=operations,
                                  variable=self.var_operation)
        combo.pack(pady=5, fill="x", padx=10)
        
        # Botón aplicar
        btn_apply = ctk.CTkButton(self.frame_menu, text="✨ Aplicar Operación",
                                 command=self.aplicar_operacion,
                                 fg_color=COLORS["success"], hover_color=COLORS["hover_success"])
        btn_apply.pack(pady=10, fill="x", padx=10)
        
        # Botón guardar
        btn_save = ctk.CTkButton(self.frame_menu, text="💾 Guardar Imagen Modificada",
                                command=fi.guardar_imagen,
                                fg_color=COLORS["warning"])
        btn_save.pack(pady=5, fill="x", padx=10)
    
    def cargar_imagen1(self):
        labels = self.display.get_labels()
        fi.abrir_imagen(labels.get("img1"))
    
    def cargar_imagen2(self):
        labels = self.display.get_labels()
        fi.cargar_imagen_secundaria(labels.get("img2"))
    
    def aplicar_operacion(self):
        labels = self.display.get_labels()
        operation = self.var_operation.get()
        
        ops = {
            "Cuasi suma RGB (clamp)": fi.cuasi_suma_rgb_clamp,
            "Cuasi resta RGB (clamp)": fi.cuasi_resta_rgb_clamp,
            "Cuasi suma YIQ (clamp)": fi.sum_yiq_clamp,
            "If Darker": fi.if_darker,
            "If Lighter": fi.if_lighter
        }
        
        func = ops.get(operation)
        if func:
            func(fi.image_manager, labels.get("result"))
    
    def mostrar(self):
        self.display.set_mode("dual")
        self.frame_menu.pack(fill="both", expand=True, padx=5, pady=5)
    
    def ocultar(self):
        self.frame_menu.pack_forget()


# --------------------------------------
# Menú: Luminancia (Placeholder)
# --------------------------------------
class LuminanceMenu:
    def __init__(self, parent_frame, display_system):
        self.parent_frame = parent_frame
        self.display = display_system
        self.frame_menu = ctk.CTkFrame(parent_frame)
        self.crear_widgets()
    
    def crear_widgets(self):
        ctk.CTkLabel(self.frame_menu, text="💡 Luminancia",
                    font=("Arial", 16, "bold")).pack(pady=10)
        
        info_frame = ctk.CTkFrame(self.frame_menu)
        info_frame.pack(pady=20, padx=10, fill="both", expand=True)
        
        ctk.CTkLabel(info_frame, 
                    text="⚠️ Módulo en Desarrollo",
                    font=("Arial", 14, "bold")).pack(pady=10)
        ctk.CTkLabel(info_frame,
                    text="Las operaciones de luminancia\nserán implementadas próximamente.",
                    justify="center").pack(pady=10)
    
    def mostrar(self):
        self.display.set_mode("single")
        self.frame_menu.pack(fill="both", expand=True, padx=5, pady=5)
    
    def ocultar(self):
        self.frame_menu.pack_forget()


# Continúa en el siguiente mensaje debido al límite de caracteres...
# Continuación de Interfaz_new.py - Parte 2

# --------------------------------------
# Menú: Convolución (Actualizado)
# --------------------------------------
class ConvolutionMenu:
    def __init__(self, parent_frame, display_system):
        self.parent_frame = parent_frame
        self.display = display_system
        self.frame_menu = ctk.CTkFrame(parent_frame)
        
        self.var_tipo_filtro = ctk.StringVar(value="Pasabajos")
        self.var_subtipo = ctk.StringVar(value="Plano")
        self.var_param1 = ctk.StringVar(value="3")
        self.var_param2 = ctk.StringVar(value="0.4")
        
        self.crear_widgets()
    
    def crear_widgets(self):
        ctk.CTkLabel(self.frame_menu, text="🔲 Convolución",
                    font=("Arial", 16, "bold")).pack(pady=10)
        
        # Botón cargar imagen
        btn_load = ctk.CTkButton(self.frame_menu, text="📁 Subir Imagen",
                                command=self.cargar_imagen,
                                fg_color=COLORS["primary"], hover_color=COLORS["hover_primary"])
        btn_load.pack(pady=5, fill="x", padx=10)
        
        # Selector de Categoría
        ctk.CTkLabel(self.frame_menu, text="Tipo de Filtro:").pack(pady=(10,0))
        combo_cat = ctk.CTkOptionMenu(self.frame_menu,
                                      values=["Pasabajos", "Bordes", "Frecuencia"],
                                      variable=self.var_tipo_filtro,
                                      command=self.actualizar_opciones)
        combo_cat.pack(pady=5, fill="x", padx=10)
        
        # Selector de Subtipo
        self.lbl_sub = ctk.CTkLabel(self.frame_menu, text="Subtipo:")
        self.lbl_sub.pack(pady=(5,0))
        self.combo_sub = ctk.CTkOptionMenu(self.frame_menu,
                                          variable=self.var_subtipo,
                                          command=self.actualizar_subtipo)
        self.combo_sub.pack(pady=5, fill="x", padx=10)
        
        # Parámetro 1
        self.lbl_p1 = ctk.CTkLabel(self.frame_menu, text="Tamaño Kernel:")
        self.lbl_p1.pack(pady=(5,0))
        self.combo_p1 = ctk.CTkOptionMenu(self.frame_menu, variable=self.var_param1)
        self.combo_p1.pack(pady=5, fill="x", padx=10)
        
        # Parámetro 2
        self.frame_p2 = ctk.CTkFrame(self.frame_menu, fg_color="transparent")
        self.lbl_p2 = ctk.CTkLabel(self.frame_p2, text="Fc High:")
        self.lbl_p2.pack(pady=(5,0))
        self.entry_p2 = ctk.CTkEntry(self.frame_p2, textvariable=self.var_param2)
        self.entry_p2.pack(pady=5)
        
        # Botón aplicar
        btn_apply = ctk.CTkButton(self.frame_menu, text="✨ Aplicar Filtro",
                                 command=self.aplicar_filtro,
                                 fg_color=COLORS["success"], hover_color=COLORS["hover_success"])
        btn_apply.pack(pady=10, fill="x", padx=10)
        
        # Botón copiar
        btn_copy = ctk.CTkButton(self.frame_menu, text="📋 Copiar a Original",
                                command=fi.copiar_procesada_a_original,
                                fg_color=COLORS["accent"])
        btn_copy.pack(pady=5, fill="x", padx=10)
        
        # Botón guardar
        btn_save = ctk.CTkButton(self.frame_menu, text="💾 Guardar Imagen Modificada",
                                command=fi.guardar_imagen,
                                fg_color=COLORS["warning"])
        btn_save.pack(pady=5, fill="x", padx=10)
        
        self.actualizar_opciones("Pasabajos")
    
    def cargar_imagen(self):
        labels = self.display.get_labels()
        fi.abrir_imagen(labels.get("original"))
    
    def actualizar_opciones(self, categoria):
        self.frame_p2.pack_forget()
        
        if categoria == "Pasabajos":
            self.combo_sub.configure(values=["Plano", "Bartlett", "Gaussiano"])
            self.var_subtipo.set("Plano")
            self.lbl_p1.configure(text="Tamaño Kernel:")
            self.combo_p1.configure(values=["3", "5", "7", "9", "15"])
            self.var_param1.set("3")
        elif categoria == "Bordes":
            self.combo_sub.configure(values=["Laplaciano", "Sobel"])
            self.var_subtipo.set("Laplaciano")
            self.lbl_p1.configure(text="Variante/Orientación:")
            self.combo_p1.configure(values=["v4", "v8"])
            self.var_param1.set("v4")
        elif categoria == "Frecuencia":
            self.combo_sub.configure(values=["Pasaaltos", "Pasabanda"])
            self.var_subtipo.set("Pasaaltos")
            self.lbl_p1.configure(text="Frecuencia Corte (Fc):")
            self.combo_p1.configure(values=["0.1", "0.2", "0.3", "0.4"])
            self.var_param1.set("0.2")
    
    def actualizar_subtipo(self, subtipo):
        if subtipo == "Sobel":
            self.lbl_p1.configure(text="Dirección:")
            self.combo_p1.configure(values=["N", "S", "E", "W", "NE", "NW", "SE", "SW"])
            self.var_param1.set("N")
        elif subtipo == "Laplaciano":
            self.lbl_p1.configure(text="Variante:")
            self.combo_p1.configure(values=["v4", "v8"])
            self.var_param1.set("v4")
    
    def aplicar_filtro(self):
        labels = self.display.get_labels()
        cat = self.var_tipo_filtro.get()
        sub = self.var_subtipo.get()
        p1 = self.var_param1.get()
        
        if cat == "Pasabajos":
            fi.aplicar_filtro_pasabajos(sub, p1, labels.get("processed"))
        elif cat == "Bordes":
            if sub == "Sobel" and p1 in ["v4", "v8"]:
                p1 = "N"
            fi.aplicar_filtro_bordes(sub, p1, labels.get("processed"))
        elif cat == "Frecuencia":
            p2 = self.var_param2.get()
            fi.aplicar_filtro_frecuencia(sub, p1, p2, labels.get("processed"))
    
    def mostrar(self):
        self.display.set_mode("single")
        self.frame_menu.pack(fill="both", expand=True, padx=5, pady=5)
    
    def ocultar(self):
        self.frame_menu.pack_forget()


# --------------------------------------
# Menú: Morfología (Actualizado)
# --------------------------------------
class MorphologyMenu:
    def __init__(self, parent_frame, display_system):
        self.parent_frame = parent_frame
        self.display = display_system
        self.frame_menu = ctk.CTkFrame(parent_frame)
        
        self.var_operacion = ctk.StringVar(value="Erosión")
        self.var_kernel_size = ctk.StringVar(value="3")
        
        self.crear_widgets()
    
    def crear_widgets(self):
        ctk.CTkLabel(self.frame_menu, text="🔷 Morfología",
                    font=("Arial", 16, "bold")).pack(pady=10)
        
        # Botón cargar imagen
        btn_load = ctk.CTkButton(self.frame_menu, text="📁 Subir Imagen",
                                command=self.cargar_imagen,
                                fg_color=COLORS["primary"], hover_color=COLORS["hover_primary"])
        btn_load.pack(pady=5, fill="x", padx=10)
        
        # Selector de Operación
        ctk.CTkLabel(self.frame_menu, text="Operación Morfológica:").pack(pady=(10,0))
        operaciones = [
            "Erosión", "Dilatación", "Apertura", "Cierre",
            "Gradiente Morfológico", "Borde Externo", "Borde Interno", "Mediana"
        ]
        combo_op = ctk.CTkOptionMenu(self.frame_menu,
                                     values=operaciones,
                                     variable=self.var_operacion)
        combo_op.pack(pady=5, fill="x", padx=10)
        
        # Selector de Tamaño de Kernel
        ctk.CTkLabel(self.frame_menu, text="Tamaño Kernel:").pack(pady=(10,0))
        combo_kernel = ctk.CTkOptionMenu(self.frame_menu,
                                         values=["3", "5", "7", "9"],
                                         variable=self.var_kernel_size)
        combo_kernel.pack(pady=5, fill="x", padx=10)
        
        # Botón aplicar
        btn_apply = ctk.CTkButton(self.frame_menu, text="✨ Aplicar Operación",
                                 command=self.aplicar_operacion,
                                 fg_color=COLORS["success"], hover_color=COLORS["hover_success"])
        btn_apply.pack(pady=10, fill="x", padx=10)
        
        # Botón copiar
        btn_copy = ctk.CTkButton(self.frame_menu, text="📋 Copiar a Original",
                                command=fi.copiar_procesada_a_original,
                                fg_color=COLORS["accent"])
        btn_copy.pack(pady=5, fill="x", padx=10)
        
        # Botón guardar
        btn_save = ctk.CTkButton(self.frame_menu, text="💾 Guardar Imagen Modificada",
                                command=fi.guardar_imagen,
                                fg_color=COLORS["warning"])
        btn_save.pack(pady=5, fill="x", padx=10)
    
    def cargar_imagen(self):
        labels = self.display.get_labels()
        fi.abrir_imagen(labels.get("original"))
    
    def aplicar_operacion(self):
        labels = self.display.get_labels()
        operacion = self.var_operacion.get()
        kernel_size = int(self.var_kernel_size.get())
        fi.aplicar_morfologia(operacion, kernel_size, labels.get("processed"))
    
    def mostrar(self):
        self.display.set_mode("single")
        self.frame_menu.pack(fill="both", expand=True, padx=5, pady=5)
    
    def ocultar(self):
        self.frame_menu.pack_forget()


# Continúa en la siguiente parte...
# Parte 3 - Menú Segmentación y Aplicación Principal

# --------------------------------------
# Menú: Segmentación (Actualizado)
# --------------------------------------
class SegmentationMenu:
    def __init__(self, parent_frame, display_system):
        self.parent_frame = parent_frame
        self.display = display_system
        self.frame_menu = ctk.CTkFrame(parent_frame)
        
        self.var_categoria = ctk.StringVar(value="Binarización")
        self.var_metodo_binarizacion = ctk.StringVar(value="50% Threshold")
        self.var_metodo_bordes = ctk.StringVar(value="Laplaciano")
        self.var_kernel_bordes = ctk.StringVar(value="3")
        self.var_tolerance = ctk.StringVar(value="20")
        self.seed_point = None
        
        self.crear_widgets()
    
    def crear_widgets(self):
        ctk.CTkLabel(self.frame_menu, text="✂️ Segmentación",
                    font=("Arial", 16, "bold")).pack(pady=10)
        
        # Botón cargar imagen
        btn_load = ctk.CTkButton(self.frame_menu, text="📁 Subir Imagen",
                                command=self.cargar_imagen,
                                fg_color=COLORS["primary"], hover_color=COLORS["hover_primary"])
        btn_load.pack(pady=5, fill="x", padx=10)
        
        # Selector de Categoría
        ctk.CTkLabel(self.frame_menu, text="Categoría:").pack(pady=(10,0))
        combo_cat = ctk.CTkOptionMenu(self.frame_menu,
                                      values=["Binarización", "Detección de Bordes", "Magic Wand"],
                                      variable=self.var_categoria,
                                      command=self.actualizar_opciones)
        combo_cat.pack(pady=5, fill="x", padx=10)
        
        # Frame para opciones de Binarización
        self.frame_binarizacion = ctk.CTkFrame(self.frame_menu, fg_color="transparent")
        ctk.CTkLabel(self.frame_binarizacion, text="Método:").pack(pady=(5,0))
        combo_bin = ctk.CTkOptionMenu(self.frame_binarizacion,
                                      values=["50% Threshold", "Bimodal", "Otsu"],
                                      variable=self.var_metodo_binarizacion)
        combo_bin.pack(pady=5, fill="x", padx=10)
        btn_aplicar_bin = ctk.CTkButton(self.frame_binarizacion, text="✨ Aplicar Binarización",
                                       command=self.aplicar_binarizacion,
                                       fg_color=COLORS["success"], hover_color=COLORS["hover_success"])
        btn_aplicar_bin.pack(pady=10, fill="x", padx=10)
        
        # Frame para opciones de Bordes
        self.frame_bordes = ctk.CTkFrame(self.frame_menu, fg_color="transparent")
        ctk.CTkLabel(self.frame_bordes, text="Método:").pack(pady=(5,0))
        combo_bord = ctk.CTkOptionMenu(self.frame_bordes,
                                       values=["Laplaciano", "Morfológico", "Marching Squares"],
                                       variable=self.var_metodo_bordes)
        combo_bord.pack(pady=5, fill="x", padx=10)
        
        ctk.CTkLabel(self.frame_bordes, text="Tamaño Kernel (Morfológico):").pack(pady=(5,0))
        combo_kern = ctk.CTkOptionMenu(self.frame_bordes,
                                       values=["3", "5", "7", "9"],
                                       variable=self.var_kernel_bordes)
        combo_kern.pack(pady=5, fill="x", padx=10)
        
        btn_aplicar_bord = ctk.CTkButton(self.frame_bordes, text="✨ Aplicar Detección",
                                        command=self.aplicar_bordes,
                                        fg_color=COLORS["success"], hover_color=COLORS["hover_success"])
        btn_aplicar_bord.pack(pady=10, fill="x", padx=10)
        
        # Frame para Magic Wand
        self.frame_magic = ctk.CTkFrame(self.frame_menu, fg_color="transparent")
        ctk.CTkLabel(self.frame_magic,
                    text="Haz clic en la imagen\npara seleccionar punto",
                    justify="center").pack(pady=(5,0))
        
        ctk.CTkLabel(self.frame_magic, text="Tolerancia:").pack(pady=(10,0))
        entry_tol = ctk.CTkEntry(self.frame_magic, textvariable=self.var_tolerance, width=100)
        entry_tol.pack(pady=5)
        
        btn_activar = ctk.CTkButton(self.frame_magic, text="🎯 Activar Selección",
                                   command=self.activar_seleccion_punto,
                                   fg_color=COLORS["warning"])
        btn_activar.pack(pady=5, fill="x", padx=10)
        
        self.lbl_punto = ctk.CTkLabel(self.frame_magic, text="Punto: No seleccionado")
        self.lbl_punto.pack(pady=5)
        
        btn_aplicar_magic = ctk.CTkButton(self.frame_magic, text="✨ Aplicar Magic Wand",
                                         command=self.aplicar_magic_wand,
                                         fg_color=COLORS["success"], hover_color=COLORS["hover_success"])
        btn_aplicar_magic.pack(pady=10, fill="x", padx=10)
        
        # Botón copiar
        btn_copy = ctk.CTkButton(self.frame_menu, text="📋 Copiar a Original",
                                command=fi.copiar_procesada_a_original,
                                fg_color=COLORS["accent"])
        btn_copy.pack(pady=5, fill="x", padx=10)
        
        # Botón guardar
        btn_save = ctk.CTkButton(self.frame_menu, text="💾 Guardar Imagen Modificada",
                                command=fi.guardar_imagen,
                                fg_color=COLORS["warning"])
        btn_save.pack(pady=5, fill="x", padx=10)
        
        self.actualizar_opciones("Binarización")
    
    def cargar_imagen(self):
        labels = self.display.get_labels()
        fi.abrir_imagen(labels.get("original"))
    
    def actualizar_opciones(self, categoria):
        self.frame_binarizacion.pack_forget()
        self.frame_bordes.pack_forget()
        self.frame_magic.pack_forget()
        
        if categoria == "Binarización":
            self.frame_binarizacion.pack(pady=10, fill="x")
        elif categoria == "Detección de Bordes":
            self.frame_bordes.pack(pady=10, fill="x")
        elif categoria == "Magic Wand":
            self.frame_magic.pack(pady=10, fill="x")
    
    def aplicar_binarizacion(self):
        labels = self.display.get_labels()
        metodo = self.var_metodo_binarizacion.get()
        fi.aplicar_segmentacion(metodo, None, labels.get("processed"))
    
    def aplicar_bordes(self):
        labels = self.display.get_labels()
        metodo = self.var_metodo_bordes.get()
        kernel_size = int(self.var_kernel_bordes.get()) if metodo == "Morfológico" else None
        fi.aplicar_segmentacion(metodo, kernel_size, labels.get("processed"))
    
    def activar_seleccion_punto(self):
        labels = self.display.get_labels()
        messagebox.showinfo("Selección de Punto",
                          "Haz clic en la imagen original para seleccionar el punto semilla.")
        labels.get("processed").bind("<Button-1>", self.on_image_click)
    
    def on_image_click(self, event):
        self.seed_point = (event.x, event.y)
        self.lbl_punto.configure(text=f"Punto: ({event.x}, {event.y})")
        labels = self.display.get_labels()
        labels.get("processed").unbind("<Button-1>")
    
    def aplicar_magic_wand(self):
        if self.seed_point is None:
            messagebox.showwarning("Advertencia", "Primero selecciona un punto en la imagen.")
            return
        
        try:
            labels = self.display.get_labels()
            tolerance = int(self.var_tolerance.get())
            fi.aplicar_magic_wand(self.seed_point, tolerance, labels.get("processed"))
        except ValueError:
            messagebox.showerror("Error", "La tolerancia debe ser un número entero.")
    
    def mostrar(self):
        self.display.set_mode("single")
        self.frame_menu.pack(fill="both", expand=True, padx=5, pady=5)
    
    def ocultar(self):
        self.frame_menu.pack_forget()


# --------------------------------------
# Aplicación Principal
# --------------------------------------
class ModernApplication:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.ventana = ctk.CTk()
        self.ventana.title("Gestor de Imágenes IPDI - Grupo 8")
        self.ventana.geometry("1600x900")
        
        # Frame principal con sidebar
        self.frame_sidebar = ctk.CTkFrame(self.ventana, width=250, corner_radius=0)
        self.frame_sidebar.pack(side="left", fill="y", padx=0, pady=0)
        self.frame_sidebar.pack_propagate(False)
        
        # Frame principal para contenido
        self.frame_main = ctk.CTkFrame(self.ventana, corner_radius=0)
        self.frame_main.pack(side="right", fill="both", expand=True, padx=0, pady=0)
        
        # Sistema de visualización dinámica
        self.display_system = DynamicImageDisplay(self.frame_main)
        
        # Crear menús
        self.crear_menus()
        self.crear_sidebar()
        
        # Menú activo
        self.active_menu = None
    
    def crear_menus(self):
        """Crea todas las instancias de menús"""
        self.menu_color_space = ColorSpaceMenu(self.frame_sidebar, self.display_system)
        self.menu_arithmetic = PixelArithmeticMenu(self.frame_sidebar, self.display_system)
        self.menu_luminance = LuminanceMenu(self.frame_sidebar, self.display_system)
        self.menu_convolution = ConvolutionMenu(self.frame_sidebar, self.display_system)
        self.menu_morphology = MorphologyMenu(self.frame_sidebar, self.display_system)
        self.menu_segmentation = SegmentationMenu(self.frame_sidebar, self.display_system)
    
    def crear_sidebar(self):
        """Crea el sidebar con botones de menú"""
        # Título
        title_frame = ctk.CTkFrame(self.frame_sidebar, fg_color=COLORS["primary"], corner_radius=0)
        title_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(title_frame, text="IPDI - Grupo 8",
                    font=("Arial", 18, "bold"),
                    text_color="white").pack(pady=15)
        
        # Botones de menú
        self.btn_color_space = self.crear_boton_menu(
            "🎨 Menu Espacios Cromáticos",
            lambda: self.cambiar_menu(self.menu_color_space)
        )
        
        self.btn_arithmetic = self.crear_boton_menu(
            "🔢 Menu Aritmética de Píxeles",
            lambda: self.cambiar_menu(self.menu_arithmetic)
        )
        
        self.btn_luminance = self.crear_boton_menu(
            "💡 Menu Luminancia",
            lambda: self.cambiar_menu(self.menu_luminance)
        )
        
        self.btn_convolution = self.crear_boton_menu(
            "🔲 Menu Convolución",
            lambda: self.cambiar_menu(self.menu_convolution)
        )
        
        self.btn_morphology = self.crear_boton_menu(
            "🔷 Menu Morfología",
            lambda: self.cambiar_menu(self.menu_morphology)
        )
        
        self.btn_segmentation = self.crear_boton_menu(
            "✂️ Menu Segmentación",
            lambda: self.cambiar_menu(self.menu_segmentation)
        )
        
        # Separador
        ctk.CTkFrame(self.frame_sidebar, height=2, fg_color=COLORS["dark"]).pack(fill="x", pady=20)
        
        # Botón salir
        btn_exit = ctk.CTkButton(
            self.frame_sidebar,
            text="❌ Salir",
            command=self.ventana.destroy,
            fg_color=COLORS["danger"],
            hover_color="#dc2626",
            height=40,
            font=("Arial", 12, "bold")
        )
        btn_exit.pack(side="bottom", pady=20, padx=10, fill="x")
    
    def crear_boton_menu(self, text, command):
        """Crea un botón de menú estilizado"""
        btn = ctk.CTkButton(
            self.frame_sidebar,
            text=text,
            command=command,
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            height=45,
            anchor="w",
            font=("Arial", 12)
        )
        btn.pack(pady=2, padx=5, fill="x")
        return btn
    
    def cambiar_menu(self, nuevo_menu):
        """Cambia el menú activo"""
        # Ocultar menú anterior
        if self.active_menu:
            self.active_menu.ocultar()
        
        # Mostrar nuevo menú
        nuevo_menu.mostrar()
        self.active_menu = nuevo_menu
    
    def run(self):
        """Inicia la aplicación"""
        self.ventana.mainloop()


# --------------------------------------
# Inicio
# --------------------------------------
if __name__ == "__main__":
    app = ModernApplication()
    app.run()
