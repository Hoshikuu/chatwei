from hashlib import sha3_512
def formater(sender, receiver, time, message):
    id = sha3_512(str(sender + message + time).encode("UTF-8")).hexdigest()
    return f"id={id}\nsender={sender}\nreceiver={receiver}\ntime={time}\nmessage={message}"

formater("user1", "user2", "2025-03-06-00-16-32", "08523b639b418c17c0e018d0ef61dc43aa9d4d500189f4d145698c8f644a4459}£¤ÂÐÈÙÚÄÖdc3bb1d3ef606b4e8f903a8428b8ca9d410cd062f4b20618224cdc2664077f9a")