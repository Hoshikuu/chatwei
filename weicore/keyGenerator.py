from PIL import Image
import random

# Función para generar la imagen mezclada en formato BMP de 1 bit
def generar_imagen_mezclada_bmp(ancho, alto, nombre_archivo):
    # Crear una nueva imagen en modo "1" (1-bit, blanco y negro)
    imagen = Image.new("1", (ancho, alto))

    # Generar píxeles aleatorios
    for y in range(alto):
        for x in range(ancho):
            # 50% de probabilidad de blanco (1) o negro (0)
            color = 1 if random.random() < 0.5 else 0
            imagen.putpixel((x, y), color)

    # Mezclar los píxeles de la imagen
    pixeles = list(imagen.getdata())  # Obtener todos los píxeles como una lista
    random.shuffle(pixeles)  # Barajar la lista de píxeles

    # Crear una nueva imagen con los píxeles mezclados
    imagen_mezclada = Image.new("1", (ancho, alto))
    imagen_mezclada.putdata(pixeles)

    # Guardar la imagen mezclada en formato BMP
    imagen_mezclada.save(nombre_archivo)
    print(f"Imagen mezclada guardada como '{nombre_archivo}'")

    return imagen_mezclada

# Función para leer los píxeles y guardar el contenido en un archivo
def guardar_pixeles_como_binario(imagen, nombre_archivo):
    ancho, alto = imagen.size
    contenido = ""

    # Leer cada píxel y convertirlo a "1" (negro) o "0" (blanco)
    for y in range(alto):
        for x in range(ancho):
            pixel = imagen.getpixel((x, y))
            if pixel == 0:  # Negro
                contenido += "1"
            else:  # Blanco (1)
                contenido += "0"
        # contenido += "\n"  # Nueva línea después de cada fila

    # Guardar el contenido en un archivo de texto
    with open(nombre_archivo, "w") as archivo:
        archivo.write(contenido)
    print(f"Contenido de los píxeles guardado en '{nombre_archivo}'")

# Tamaño de la imagen
ancho, alto = 256, 256

# Generar la imagen mezclada en formato BMP de 1 bit
imagen_mezclada = generar_imagen_mezclada_bmp(ancho, alto, "imagen_mezclada_64x64.bmp")

# Guardar los píxeles como "1" y "0" en un archivo de texto
guardar_pixeles_como_binario(imagen_mezclada, "pixeles_imagen.txt")