from PIL.Image import new, open as openI
from random import random, shuffle
from base64 import b64encode

def GenerateKey(width, height, filename):
    image = new("1", (width, height))

    for y in range(height):
        for x in range(width):
            color = 1 if random() < 0.5 else 0
            image.putpixel((x, y), color)

    pixels = list(image.getdata())
    shuffle(pixels)

    imageShuffle = new("1", (width, height))
    imageShuffle.putdata(pixels)

    imageShuffle.save(filename)

def GetKey(path):
    imagen = openI(path)
    width, height = imagen.size
    content = ""

    for y in range(height):
        for x in range(width):
            pixel = imagen.getpixel((x, y))
            if pixel == 0:
                content += "1"
            else:
                content += "0"
                
    content = content.replace("\n", "")

    bytes_list = [content[i:i+8] for i in range(0, len(content), 8)]

    texto = ""
    for byte in bytes_list:
        if len(byte) == 8:
            caracter = chr(int(byte, 2))
            texto += caracter
            
    keyBase64 = b64encode(texto.encode("utf-8")).decode("utf-8")
    return keyBase64