import base64

# Función para convertir un archivo de bits (1 y 0) en caracteres
def bits_a_caracteres(nombre_archivo_bits):
    with open(nombre_archivo_bits, "r") as archivo_bits:
        # Leer todo el contenido y eliminar saltos de línea
        contenido = archivo_bits.read().replace("\n", "")

    # Agrupar los bits en bloques de 8
    bytes_list = [contenido[i:i+8] for i in range(0, len(contenido), 8)]

    # Convertir cada byte a su carácter correspondiente
    texto = ""
    for byte in bytes_list:
        if len(byte) == 8:  # Asegurarse de que el byte tenga 8 bits
            caracter = chr(int(byte, 2))  # Convertir de binario a carácter
            texto += caracter

    return texto

# Función para codificar texto en Base64 y guardarlo en un archivo
def codificar_base64(texto, nombre_archivo_salida):
    # Codificar el texto en Base64
    texto_codificado = base64.b64encode(texto.encode("utf-8")).decode("utf-8")

    # Guardar el texto codificado en un archivo
    with open(nombre_archivo_salida, "w", encoding="utf-8") as archivo_salida:
        archivo_salida.write(texto_codificado)

    print(f"Texto codificado en Base64 guardado en '{nombre_archivo_salida}'")

# Archivo de entrada (archivo de bits)
archivo_bits = "pixeles_imagen.txt"

# Archivo de salida (archivo de texto en Base64)
archivo_salida = "texto_codificado_base64.txt"

# Convertir bits a caracteres
texto = bits_a_caracteres(archivo_bits)

# Codificar el texto en Base64 y guardarlo
codificar_base64(texto, archivo_salida)