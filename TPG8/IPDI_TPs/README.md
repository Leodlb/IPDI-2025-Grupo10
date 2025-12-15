# Sistema de Procesamiento Digital de Imágenes - IPDI Grupo 8

## Descripción del Proyecto

ATENCION: El sistema funcional completo con interfaz grafica esta en la carpeta "Sistema_Final". ejecute "Interfaz.py" para iniciar el sistema. Las Carpetas T0* tienen solo las funciones de las tareas 0*.

Este proyecto implementa un sistema completo de procesamiento digital de imágenes desarrollado en Python. La aplicación cuenta con una interfaz gráfica que permite realizar diversas operaciones de procesamiento de imágenes.

## Requisitos del Sistema

### Software Necesario

- Python 3.10 o superior
- pip (gestor de paquetes de Python)
- Git (para clonar el repositorio)

### Sistemas Operativos Compatibles

- Windows 10/11
- Linux (Ubuntu 20.04 o superior)
- macOS 10.15 o superior

## Instalación

### Paso 1: Clonar el Repositorio

Abra una terminal o línea de comandos y ejecute:

```bash
git clone https://github.com/SbaMndz/IPDI-2025-Grupo8.git
cd IPDI-2025-Grupo8
```

### Paso 2: Navegar al Directorio del Sistema

```bash
cd Sistema_Final
```

### Paso 3: Crear el Entorno Virtual

Es recomendable utilizar un entorno virtual para evitar conflictos con otras instalaciones de Python.

En Windows:
```bash
python -m venv vIPDI
```

En Linux/macOS:
```bash
python3 -m venv vIPDI
```

### Paso 4: Activar el Entorno Virtual

En Windows (PowerShell):
```bash
.\vIPDI\Scripts\Activate.ps1
```

En Windows (CMD):
```bash
.\vIPDI\Scripts\activate.bat
```

En Linux/macOS:
```bash
source vIPDI/bin/activate
```

Nota: Si aparece un error de permisos en Windows PowerShell, ejecute primero:
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Paso 5: Instalar Dependencias

Con el entorno virtual activado, instale todas las dependencias necesarias:

```bash
pip install -r requirements.txt
```

Este comando instalará las siguientes bibliotecas:
- imageio: Lectura y escritura de imágenes
- numpy: Operaciones numéricas y matriciales
- matplotlib: Visualización de datos
- pillow: Manipulación de imágenes
- customtkinter: Interfaz gráfica moderna
- opencv-python: Procesamiento de imágenes
- scikit-image: Algoritmos avanzados de procesamiento

## Ejecución del Programa

### Método 1: Ejecución Directa

Con el entorno virtual activado, ejecute:

```bash
python Interfaz.py
```

### Método 2: Ejecución con Ruta Completa (Windows)

Si el entorno virtual está activado:
```bash
.\vIPDI\Scripts\python.exe Interfaz.py
```

### Método 3: Ejecución con Ruta Completa (Linux/macOS)

```bash
./vIPDI/bin/python Interfaz.py
```

## Estructura del Proyecto

```
Sistema_Final/
├── Interfaz.py                          # Interfaz gráfica principal
├── funciones_interfaz.py                # Funciones de procesamiento
├── Procesamiento_Morfologico.py         # Operaciones morfológicas
├── Procesamiento_Segmentacion.py        # Algoritmos de segmentación
├── procesamiento_por_convolucion.py     # Filtros de convolución
├── Segmentar_ojos.py                    # Segmentación específica
├── app.py                               # Conversión de espacios cromáticos
├── my_functions.py                      # Funciones auxiliares
├── requirements.txt                     # Dependencias del proyecto
└── vIPDI/                               # Entorno virtual (no incluido en git)
```

## Funcionalidades del Sistema

### 1. Menu Espacios Cromáticos

Permite trabajar con diferentes representaciones de color:
- Visualización de canales RGB individuales o combinados
- Conversión entre espacios RGB y YIQ
- Visualización de canales YIQ
- Inversión de colores

### 2. Menu Aritmética de Píxeles

Operaciones entre dos imágenes:
- Suma de imágenes en RGB con clamp
- Resta de imágenes en RGB con clamp
- Suma de imágenes en YIQ con clamp
- Operador If Darker (selecciona píxeles más oscuros)
- Operador If Lighter (selecciona píxeles más claros)

### 3. Menu Convolución

Aplicación de filtros mediante convolución:

Filtros Pasabajos:
- Filtro Plano (promedio simple)
- Filtro Bartlett (promedio ponderado triangular)
- Filtro Gaussiano (suavizado con distribución gaussiana)

Detección de Bordes:
- Operador Laplaciano (variantes de 4 y 8 vecinos)
- Operador Sobel (8 direcciones: N, S, E, W, NE, NW, SE, SW)

Filtros de Frecuencia:
- Filtro Pasaaltos
- Filtro Pasabanda

### 4. Menu Morfología

Operaciones morfológicas en escala de grises:
- Erosión
- Dilatación
- Apertura (erosión seguida de dilatación)
- Cierre (dilatación seguida de erosión)
- Gradiente Morfológico
- Borde Externo
- Borde Interno
- Filtro de Mediana

### 5. Menu Segmentación

Técnicas de segmentación de imágenes:

Binarización:
- Umbral del 50% (basado en la mediana)
- Binarización Bimodal (dos modas en el histograma)
- Método de Otsu (umbralización automática)

Detección de Bordes:
- Laplaciano
- Gradiente Morfológico
- Marching Squares (contornos mediante isosuperficies)

Segmentación por Región:
- Magic Wand (varita mágica con tolerancia ajustable)

### 6. Menu Luminancia

Módulo preparado para futuras implementaciones de operaciones de luminancia.

## Guía de Uso

### Carga de Imágenes

1. Seleccione el menú deseado en el panel lateral izquierdo
2. Haga clic en el botón "Subir Imagen"
3. Navegue hasta la ubicación de su imagen
4. Seleccione la imagen y confirme

Para operaciones que requieren dos imágenes (Aritmética de Píxeles):
1. Haga clic en "Subir Imagen 1"
2. Haga clic en "Subir Imagen 2"

### Aplicación de Operaciones

1. Configure los parámetros de la operación deseada
2. Haga clic en el botón "Aplicar" correspondiente
3. El resultado aparecerá en el panel de imagen procesada

### Procesamiento Secuencial

Para aplicar múltiples operaciones en secuencia:
1. Aplique la primera operación
2. Haga clic en "Copiar a Original"
3. La imagen procesada se convierte en la nueva imagen original
4. Aplique la siguiente operación
5. Repita según sea necesario

### Guardar Resultados

1. Una vez procesada la imagen, haga clic en "Guardar Imagen Modificada"
2. Seleccione la ubicación y nombre del archivo
3. Elija el formato deseado (JPG, PNG, BMP)
4. Confirme para guardar

## Solución de Problemas Comunes

### Error: "No module named 'customtkinter'"

Solución: Asegúrese de que el entorno virtual esté activado y ejecute:
```bash
pip install -r requirements.txt
```

### Error: "Permission denied" al activar el entorno virtual en Windows

Solución: Ejecute PowerShell como administrador y ejecute:
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### La interfaz no se muestra correctamente

Solución: Verifique que todas las dependencias estén instaladas correctamente:
```bash
pip list
```

Si falta alguna biblioteca, reinstale las dependencias:
```bash
pip install -r requirements.txt --force-reinstall
```

### Error al cargar imágenes muy grandes

Solución: El sistema redimensiona automáticamente las imágenes para visualización. Si persiste el error, intente con una imagen de menor resolución o aumente la memoria disponible para Python.

### Advertencia sobre HighDPI en Windows

Esta advertencia es normal y no afecta el funcionamiento del programa. Se debe a que PIL ImageTk no está optimizado para pantallas de alta resolución, pero la funcionalidad permanece intacta.

## Desactivar el Entorno Virtual

Cuando termine de usar el programa, puede desactivar el entorno virtual ejecutando:

```bash
deactivate
```

## Actualización del Proyecto

Para obtener las últimas actualizaciones del repositorio:

```bash
git pull origin main
```

Luego, actualice las dependencias si es necesario:

```bash
pip install -r requirements.txt --upgrade
```

## Información Adicional

### Formatos de Imagen Soportados

- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- GIF (.gif)
- TIFF (.tiff, .tif)

### Rendimiento

El rendimiento del sistema depende de:
- Resolución de las imágenes procesadas
- Complejidad de las operaciones aplicadas
- Especificaciones del hardware

Para imágenes de alta resolución, algunas operaciones pueden tomar varios segundos.

## Contacto y Soporte

Para reportar problemas o sugerencias, por favor utilice el sistema de issues del repositorio de GitHub.

## Licencia

Este proyecto fue desarrollado con fines académicos para el curso de Procesamiento Digital de Imágenes.
