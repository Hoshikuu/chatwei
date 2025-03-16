from hashlib import sha3_256
from random import randint

def sha256(text):
    string = str(text)
    stringsha256 = sha3_256(string.encode("UTF-8")).hexdigest()
    return sha3_256(stringsha256.encode("UTF-8")).hexdigest()

def encriptA(content, chunkLevel, actualKey):
    seed = randint(0, 64 - chunkLevel)
    actualKey = sha256(actualKey)[seed:seed+chunkLevel]
    segments = ""
    result = ""
    for i in range(0, len(content), chunkLevel):
        chunk = content[i:i+chunkLevel]

        seg = ""
        for charC, charK in zip(chunk, actualKey):
            seg += chr(abs(int(format(ord(charC), "08b"), 2) + int(format(ord(charK), "08b"), 2)))
        result += seg
        segments += sha256(seg)
    return sha256(seed) + result + sha256(segments)

def encriptB(allContent, chunkLevel, actualKey):
    segments = ""
    checksum = ""
    seed = 0
    result = ""
    prevSeed = allContent[:64]
    prevChecksum = allContent[-64:]
    fileContent = allContent[64:-64]

    for i in range(64):
        if sha256(i) == prevSeed:
            seed = i
            break

    actualKey = sha256(actualKey)[seed:seed+chunkLevel]

    for i in range(0, len(fileContent), chunkLevel):
        chunk = fileContent[i:i+chunkLevel]
        checksum += sha256(chunk)

        seg = ""
        for charC, charK in zip(chunk, actualKey):
            seg += chr(abs(int(format(ord(charC), "08b"), 2) + int(format(ord(charK), "08b"), 2)))
        result += seg
        segments += sha256(seg)
    checksum = sha256(checksum)

    if checksum == prevChecksum:
        print("OK")
    else:
        print("BAD")
        return "Checksum Problem"
    return sha256(seed) + result + sha256(segments)

def decriptA(allContent, chunkLevel, actualKey):
    segments = ""
    checksum = ""
    seed = 0
    result = ""
    prevSeed = allContent[:64]
    prevChecksum = allContent[-64:]
    fileContent = allContent[64:-64]

    for i in range(64):
        if sha256(i) == prevSeed:
            seed = i
            break

    actualKey = sha256(actualKey)[seed:seed+chunkLevel]

    for i in range(0, len(fileContent), chunkLevel):
        chunk = fileContent[i:i+chunkLevel]
        checksum += sha256(chunk)

        seg = ""
        for charC, charK in zip(chunk, actualKey):
            seg += chr(abs(int(format(ord(charC), "08b"), 2) - int(format(ord(charK), "08b"), 2)))
        result += seg
        segments += sha256(seg)
    checksum = sha256(checksum)

    if checksum == prevChecksum:
        print("OK")
    else:
        print("BAD")
        return "Checksum Problem"
    return sha256(seed) + result + sha256(segments)

def decriptB(allContent, chunkLevel, actualKey):
    checksum = ""
    seed = 0
    result = ""
    prevSeed = allContent[:64]
    prevChecksum = allContent[-64:]
    fileContent = allContent[64:-64]

    for i in range(64):
        if sha256(i) == prevSeed:
            seed = i
            break

    actualKey = sha256(actualKey)[seed:seed+chunkLevel]

    for i in range(0, len(fileContent), chunkLevel):
        chunk = fileContent[i:i+chunkLevel]
        checksum += sha256(chunk)

        seg = ""
        for charC, charK in zip(chunk, actualKey):
            seg += chr(abs(int(format(ord(charC), "08b"), 2) - int(format(ord(charK), "08b"), 2)))
        result += seg
    checksum = sha256(checksum)

    if checksum == prevChecksum:
        print("OK")
    else:
        print("BAD")
        return "Checksum Problem"
    return result

# A = encriptA("Hola buenos dias", 16, "secret")
# print(A)

# B = encriptB(A, 16, "gulag")
# print(B)

# C = decriptA(B, 16, "secret")
# print(C)

# D = decriptB(C, 16, "gulag")
# print(D)

