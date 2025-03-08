from fastapi import FastAPI
from pydantic import BaseModel
import os
import sqlite3
from base64 import b64encode, b64decode

app = FastAPI()

class UpdateChat(BaseModel):
    user: str

class SendChat(BaseModel):
    data: str

def decode_base64(encoded_text):
    decoded_bytes = b64decode(encoded_text)
    return decoded_bytes.decode('utf-8')

@app.post("/data")
async def Data(data: UpdateChat):
    try:
        conn = sqlite3.connect("chatwei.db")
        cursor = conn.cursor()

        cursor.execute(f"""
    SELECT * FROM data 
    WHERE receiver = '{data.user}' AND isSend = 0 
    LIMIT 1;
    """)
        resultados = cursor.fetchall()

        
        cursor.execute(f"""
    UPDATE data
    SET isSend = 1
    WHERE id = '{resultados[0][0]}'
    """)
        
        
        conn.commit()
        conn.close()

        return resultados[0][3]
    except Exception:
        return False

@app.post("/send")
async def Send(data: SendChat):
    print(data.data)

    conn = sqlite3.connect("chatwei.db")
    cursor = conn.cursor()

    mes = decode_base64(data.data).split("\n")
    mesId = mes[0].split("=")[1]
    mesSender = mes[1].split("=")[1]
    mesReceiver = mes[2].split("=")[1]
    mesTime = mes[3].split("=")[1]
    mesMessage = mes[4].split("=")[1]

    cursor.execute(f"""
INSERT INTO data (id, sender, receiver, message, time, isSend)
VALUES ('{mesId}', '{mesSender}', '{mesReceiver}', '{mesMessage}', '{mesTime}', 0)
""")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    os.system("fastapi dev " + __file__)
    