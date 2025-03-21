from fastapi import FastAPI
from pydantic import BaseModel
from os import system
from sqlite3 import connect
from weicore.coder import decodeb64
from hashlib import sha3_512
import json

app = FastAPI()
database = "database/chatweiV2.db"

def sha512(text):
    string = str(text)
    stringsha256 = sha3_512(string.encode("UTF-8")).hexdigest()
    return sha3_512(stringsha256.encode("UTF-8")).hexdigest()

# Modelo base para swap
class swap(BaseModel):
    chatid: str
    id: str
    receiver: str
    message: str
    fase: str

# Modelo base para getswap   
class getswap(BaseModel):
    chatid: str
    receiver: str

# Crea la tabla de swap para el chat si no existe
def CreateSwapTable(chatid):
    conn = connect(database)
    cursor = conn.cursor()
    
    # Crear la tabla de swap si no existe
    #! fase tiene que marcar la fase de encriptacion en la que esta, por ejemplo, encriptado por 1, encriptado por 1 y 2, encriptado por 2, desencriptado
    #* fase 1 = encriptado por usuario 1
    #* fase 2 = encriptado por usuario 1 y 2
    #* fase 3 = encriptado por usuario 2
    #* fase 4 = desencriptado (contenido en fase3) es un marcador de que ya se ha completado
    sql = f'''
        CREATE TABLE "{chatid}_swap" (
        "id"	TEXT NOT NULL UNIQUE,
        "receiver"	TEXT NOT NULL,
        "message"	TEXT NOT NULL,
        "time"      TEXT NOT NULL,
        "fase"	INTEGER NOT NULL DEFAULT 1,
	    PRIMARY KEY("id")
    );''' 
    cursor.execute(sql)
    conn.commit()
    
    conn.close()
    
# Esto se hara cargo de introducir datos en la tabla de swap de cada chat.
#* Los chats se crean a base de una ID unica de chat que se introducira en una tabla tambien.
@app.post("/swap")
async def Swap(data: swap):
    conn = connect(database)
    cursor = conn.cursor()
    
    CreateSwapTable(data.chatid)

    # Añadir los datos a la tabla
    sql = f'''
        INSERT INTO {data.chatid}_swap (id, receiver, message, fase)
        VALUES ("{data.id}", "{data.receiver}", "{data.message}", "{data.fase}"
    )'''
    cursor.execute(sql)
    conn.commit()
    
    conn.close()

# Obtener los datos en la tabla de swap
@app.post("/getswap")
async def GetSwap(data: getswap):
    
    #? Falta añadir alguna funcion que limpie esta tabla de los mensajes ya pasados al otro usuario, por ejemplo los mensajes que esten en fase 4 significa que ya fueron desencriptados
    #? Limpiar la tabla de fase 4 y mover los datos a una tabla a parte donde se guardaran los mensajes enviados por cada uno, en fase 1 y fase 4 que es como pueden leer los usuarios
    #? Con sus claves de encriptacion, en la tabla id_data contendra mensajes de esta forma siendo usuario 1 de ejemplo, mensajes en fase 1 porque usa mi encriptacion
    #? Mensajes en fase 3 porque es donde se usa mi encriptacion al recibirlo.
    
    conn = connect(database)
    cursor = conn.cursor()
    
    CreateSwapTable(data.chatid)
    
    sql = f'''
        SELECT * FROM {data.chatid}_swap
        WHERE receiver = "{data.receiver}"
    '''
    cursor.execute(sql)
    resultados = json.dumps(cursor.fetchall())
    
    conn.close()
    return resultados
    
if __name__ == "__main__":
    system(f'fastapi dev "{__file__}"')