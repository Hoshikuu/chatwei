from random import randint as ri; from hashlib import sha3_256 as sh; h = lambda t: sh(sh(str(t).encode()).hexdigest().encode()).hexdigest()
def cifrarArchivo(mk, cl, msg):
    s = ri(0, 64 - cl); ct, ss, ek = "", "", h(mk)[s:s + cl]
    for i in range(0, len(msg), cl):c = msg[i:i + cl]; sg = "".join(chr(abs(ord(a) + ord(b))) for a, b in zip(c, ek)); ct += sg; ek = h(c+sg)[s:s + cl]; ss += h(sg)
    return h(s) + ct + h(ss)
def descifrarArchivo(mk, cl, msg):
    hs, cs = msg[:64], msg[-64:]; s = next((i for i in range(64) if h(i) == hs)); ek, txt, cks = h(mk)[s:s + cl], "", ""
    for i in range(0, len(msg[64:-64]), cl):c = msg[64:-64][i:i + cl]; txt += "".join(chr(abs(ord(a) - ord(b))) for a, b in zip(c, ek)); cks += h(c); ek = h(txt[-cl:] + c)[s:s + cl]
    return txt if h(cks) == cs else False

with open("aaaaaaaaaaaa.txt", "w+", encoding="UTF-8") as file:
    file.write(cifrarArchivo("secret", 16, "Hola como estas"))