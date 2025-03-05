from hashlib import sha3_512

def formater(sender, receiver, time, message):
    id = sha3_512(str(sender + message + time).encode("UTF-8")).hexdigest()
    with open(id+".cwei", "w+", encoding="UTF-8") as file:
        content=f"id={id}\nsender={sender}\nreceiver={receiver}\ntime={time}\nmessage={message}"
        file.write(content)

formater("user1", "user2", "2025-03-06-00-16-32", "Hola como estas")