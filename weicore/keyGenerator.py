from PIL import Image
import random

def GenerateKey(width, height, filename):
    image = Image.new("1", (width, height))

    for y in range(height):
        for x in range(width):
            color = 1 if random.random() < 0.5 else 0
            image.putpixel((x, y), color)

    pixels = list(image.getdata())
    random.shuffle(pixels)

    imageShuffle = Image.new("1", (width, height))
    imageShuffle.putdata(pixels)

    imageShuffle.save(filename)

def ConvertKey(imagen, filename):
    width, height = imagen.size
    content = ""

    for y in range(height):
        for x in range(width):
            pixel = imagen.getpixel((x, y))
            if pixel == 0:
                content += "1"
            else:
                content += "0"

    return content