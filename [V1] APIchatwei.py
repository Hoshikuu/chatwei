from fastapi import FastAPI
from pydantic import BaseModel
from os import system
from sqlite3 import connect
from weicore.coder import decodeb64

#TODO Volver a hacer el archivo, ha habido muchos cambios que ya no es sostenible modificar el archivo
#TODO Nueva API debe contener, las siguientes cosas
#TODO Una funcion para crear pasar handshake entre usuarios, archivos entremedias de encriptacion hasta poder obtener el mensaje desencriptado, hay 4 niveles
#TODO Encriptado por usuario A, encriptado por usuario A y B, desencriptado por usuario A (encriptado por usuario B), desencriptado por usuario B (texto en plano)
#TODO Otra funcion para almacenar las dos versiones encriptadas, una por el usuario A y otra por el usuario B, para que funcione como historial
#? Maybe hacerlo de forma local, tener generar archivos encriptados que contengan esos datos y se vaya actualizando y no tener que llamar al servidor cada vez
#TODO Otra funcion para enviar mensajes que posteriormente se van a meter a la tabla de base de datos handshake
#TODO Por ultimo implmentar el generador de claves aleatorias en el cliente, se hizo con imagenes porque ocupa mucho menos que el texto plano, por cada chat
#TODO Se va a generar una clave aleatoria de 256x256 en otras palabras 65.536 bits, binarias de 1 y 0, pedir al usuario que no pierda las claves estaran guardadas en una carpeta
#TODO Esa clave servira para encriptar los mensajes del chat.

app = FastAPI()
database = "database/chatwei.db"

class Default(BaseModel):
    user: str
    otherUser: str

class SendChat(BaseModel):
    data: str

class Hand(BaseModel):
    receiver: str
    fase: str

def GetMessage(user, otherUser):
    conn = connect(database)
    cursor = conn.cursor()
    
    sql = f"""
    SELECT * FROM data 
    WHERE receiver = '{user}' AND sender = '{otherUser}' AND isSend = 0 
    LIMIT 1;
    """

    cursor.execute(sql)
    resultados = cursor.fetchall()
    conn.commit()
    conn.close()
    return resultados

def SetIsSend(id):
    conn = connect(database)
    cursor = conn.cursor()
    
    sql = f"""
    UPDATE data
    SET isSend = 1
    WHERE id = '{id}'
    """

    cursor.execute(sql)
    conn.commit()
    conn.close()

def AddMessage(data):
    conn = connect(database)
    cursor = conn.cursor()

    mes = decodeb64(data).split("\n")
    mesId = mes[0].split("=")[1]
    mesSender = mes[1].split("=")[1]
    mesReceiver = mes[2].split("=")[1]
    mesTime = mes[3].split("=")[1]
    mesMessage = mes[4].split("=")[1]

    sql = f"""
INSERT INTO data (id, sender, receiver, message, time, isSend)
VALUES ('{mesId}', '{mesSender}', '{mesReceiver}', '{mesMessage}', '{mesTime}', 0)
"""

    cursor.execute(sql)
    conn.commit()
    conn.close()

@app.post("/data")
async def Data(data: Default):
    try:
        message = GetMessage(data.user, data.otherUser)[0]
        SetIsSend(message[0])

        return message
    except Exception:
        return False

@app.post("/send")
async def Send(data: SendChat):
    AddMessage(data.data)

@app.post("/last")
async def Send(data: Default):
    conn = connect(database)
    cursor = conn.cursor()

    sql = f"""
SELECT * FROM data 
WHERE receiver = '{data.user}' AND sender = '{data.otherUser}' AND isSend = 1 OR receiver = '{data.otherUser}' AND sender = '{data.user}'
ORDER BY time DESC LIMIT 1;
"""
    
    cursor.execute(sql)
    resultados = cursor.fetchall()
    conn.commit()
    conn.close()
    print(resultados)
    if resultados != "":
        return resultados
    return ""

@app.post("/history")
async def HistoryRecovery(data: Default):
    conn = connect(database)
    cursor = conn.cursor()

    sql = f"""
SELECT * FROM data 
WHERE receiver = '{data.user}' AND sender = '{data.otherUser}' AND isSend = 1 OR receiver = '{data.otherUser}' AND sender = '{data.user}'
ORDER BY time ASC;
"""

    cursor.execute(sql)
    resultados = cursor.fetchall()
    conn.commit()
    conn.close()
    return resultados

async def HandShake():
    conn = connect(database)
    cursor = conn.cursor()

if __name__ == "__main__":
    system(f'fastapi dev "{__file__}"')
    