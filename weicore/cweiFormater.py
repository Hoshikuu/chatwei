from hashlib import sha3_512
def formater(sender, receiver, time, message):
    id = sha3_512(str(sender + message + time).encode("UTF-8")).hexdigest()
    return f"id={id}\nsender={sender}\nreceiver={receiver}\ntime={time}\nmessage={message}"