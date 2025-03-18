# cipwei [V2]

#TODO Cambiar el sistema de Seed, se puede cambiar en vez de usar un sha256 usar un caracter, asi es mas eficiente por ejemplo, tengo seed 45 usar el caracter ascii 45 asi tiene mas rendimiento
#TODO Cambiar el sistema de encriptado, en vez de una suma unica podemos cojer 2 seeds aleatorios que se declararan al principio del archivo, 2 caracteres, el primero sera para
#TODO La primera seed el segundo para la segunda, luego usar un hash sha512, para mayor tamaño y mayor aleatoridad, una vez hecho eso, podemos pasar por la encriptacion, separarlo en
#TODO 2 claves distintos, clave1 y clave2, y que la clave1 en cifrado sea sumar al caracter y clave2 sea restar, luego en el descifrado sea al reves clave1 para restar y clave2 para sumar

#! TIENE PEQUEÑOS ERRORES AL DESENCRIPTAR INTENTAR VER LA CAUSA # FIXED

from hashlib import sha3_512
from random import randint

def sha512(text):
    string = str(text)
    stringsha256 = sha3_512(string.encode("UTF-8")).hexdigest()
    return sha3_512(stringsha256.encode("UTF-8")).hexdigest()

def encriptA(content, chunkLevel, masterKey):
    seed1 = randint(0, 128 - chunkLevel)
    seed2 = randint(0, 128 - chunkLevel)
    key1 = sha512(masterKey)[seed1:seed1+chunkLevel]
    key2 = sha512(masterKey)[seed2:seed2+chunkLevel]
    segments = ""
    result = ""
    for i in range(0, len(content), chunkLevel):
        chunk = content[i:i+chunkLevel]
        
        seg = ""
        for charC, charK1, charK2 in zip(chunk, key1, key2):
            print(charC, charK1, charK2)
            print(int(format(ord(charC), "08b"), 2), int(format(ord(charK1), "08b"), 2), int(format(ord(charK2), "08b"), 2))
            seg += chr(abs(int(format(ord(charC), "08b"), 2) + int(format(ord(charK1), "08b"), 2) * 2 - int(format(ord(charK2), "08b"), 2)))
        result += seg
        segments += sha512(seg)
    print("\n\n")
    return f"wei]\n{chr(seed1)}{chr(seed2)}{result}\n{sha512(segments)}"

def encriptB(allContent, chunkLevel, masterKey):
    segments = ""
    checksum = ""
    result = ""
    seed1 = int(format(ord(allContent[5:6]), "08b"), 2)
    seed2 = int(format(ord(allContent[6:7]), "08b"), 2)
    prevChecksum = allContent[-128:]
    fileContent = allContent[7:-129]

    key1 = sha512(masterKey)[seed1:seed1+chunkLevel]
    key2 = sha512(masterKey)[seed2:seed2+chunkLevel]

    for i in range(0, len(fileContent), chunkLevel):
        chunk = fileContent[i:i+chunkLevel]
        checksum += sha512(chunk)

        seg = ""
        for charC, charK1, charK2 in zip(chunk, key1, key2):
            print(charC, charK1, charK2)
            print(int(format(ord(charC), "08b"), 2), int(format(ord(charK1), "08b"), 2), int(format(ord(charK2), "08b"), 2))
            seg += chr(abs(int(format(ord(charC), "08b"), 2) + int(format(ord(charK1), "08b"), 2) * 2 - int(format(ord(charK2), "08b"), 2)))
        result += seg
        segments += sha512(seg)
    checksum = sha512(checksum)

    if checksum == prevChecksum:
        print("OK")
    else:
        print("BAD")
        return "Checksum Problem"
    print("\n\n")
    return f"wei]\n{chr(seed1)}{chr(seed2)}{result}\n{sha512(segments)}"

def decriptA(allContent, chunkLevel, masterKey):
    segments = ""
    checksum = ""
    result = ""
    seed1 = int(format(ord(allContent[5:6]), "08b"), 2)
    seed2 = int(format(ord(allContent[6:7]), "08b"), 2)
    prevChecksum = allContent[-128:]
    fileContent = allContent[7:-129]

    key1 = sha512(masterKey)[seed1:seed1+chunkLevel]
    key2 = sha512(masterKey)[seed2:seed2+chunkLevel]

    for i in range(0, len(fileContent), chunkLevel):
        chunk = fileContent[i:i+chunkLevel]
        checksum += sha512(chunk)

        seg = ""
        for charC, charK1, charK2 in zip(chunk, key1, key2):
            print(charC, charK1, charK2)
            print(int(format(ord(charC), "08b"), 2), int(format(ord(charK1), "08b"), 2), int(format(ord(charK2), "08b"), 2))
            seg += chr(abs(int(format(ord(charC), "08b"), 2) - int(format(ord(charK1), "08b"), 2) * 2 + int(format(ord(charK2), "08b"), 2)))
        result += seg
        segments += sha512(seg)
    checksum = sha512(checksum)

    if checksum == prevChecksum:
        print("OK")
    else:
        print("BAD")
        return "Checksum Problem"
    print("\n\n")
    return f"wei]\n{chr(seed1)}{chr(seed2)}{result}\n{sha512(segments)}"

def decriptB(allContent, chunkLevel, masterKey):
    checksum = ""
    result = ""
    seed1 = int(format(ord(allContent[5:6]), "08b"), 2)
    seed2 = int(format(ord(allContent[6:7]), "08b"), 2)
    prevChecksum = allContent[-128:]
    fileContent = allContent[7:-129]

    key1 = sha512(masterKey)[seed1:seed1+chunkLevel]
    key2 = sha512(masterKey)[seed2:seed2+chunkLevel]

    for i in range(0, len(fileContent), chunkLevel):
        chunk = fileContent[i:i+chunkLevel]
        checksum += sha512(chunk)

        seg = ""
        for charC, charK1, charK2 in zip(chunk, key1, key2):
            print(charC, charK1, charK2)
            print(int(format(ord(charC), "08b"), 2), int(format(ord(charK1), "08b"), 2), int(format(ord(charK2), "08b"), 2))
            seg += chr(abs(int(format(ord(charC), "08b"), 2) - int(format(ord(charK1), "08b"), 2) * 2 + int(format(ord(charK2), "08b"), 2)))
        result += seg
    checksum = sha512(checksum)

    if checksum == prevChecksum:
        print("OK")
    else:
        print("BAD")
        return "Checksum Problem"
    print("\n\n")
    return result

A = encriptA("Hola buenos dias a todos", 16, "secret")
with open("a", "w+", encoding="UTF-8") as file:
    file.write(A)

B = encriptB(A, 16, "gulag")
with open("b", "w+", encoding="UTF-8") as file:
    file.write(B)

C = decriptA(B, 16, "secret")
with open("c", "w+", encoding="UTF-8") as file:
    file.write(C)

D = decriptB(C, 16, "gulag")
with open("d", "w+", encoding="UTF-8") as file:
    file.write(D)

