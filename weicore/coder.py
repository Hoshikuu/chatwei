from base64 import b64encode, b64decode
def encodeb64(text):
    textBase64 = b64encode(text.encode('utf-8'))
    return textBase64.decode('utf-8')
def decodeb64(textBase64):
    text = b64decode(textBase64)
    return text.decode('utf-8')