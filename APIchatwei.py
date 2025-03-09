from fastapi import FastAPI
from pydantic import BaseModel
from os import system
from sqlite3 import connect
from weicore.coder import decodeb64

app = FastAPI()
database = "database/chatwei.db"

class UpdateChat(BaseModel):
    user: str

class SendChat(BaseModel):
    data: str

class HistoryRecovery(BaseModel):
    user: str

def GetMessage(user):
    conn = connect(database)
    cursor = conn.cursor()
    
    sql = f"""
    SELECT * FROM data 
    WHERE receiver = '{user}' AND isSend = 0 
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

# def GetHistory(user):


@app.post("/data")
async def Data(data: UpdateChat):
    try:
        message = GetMessage(data.user)[0]
        SetIsSend(message[0])

        return message[3]
    except Exception:
        return False

@app.post("/send")
async def Send(data: SendChat):
    AddMessage(data.data)

@app.post("/history")
async def HistoryRecovery(data: HistoryRecovery):
    print(data)

    conn = connect(database)
    cursor = conn.cursor()

    sql = f"""
SELECT * FROM data 
WHERE receiver = '{data.user}' OR sender = '{data.user}' AND isSend = 1 
ORDER BY time ASC;
"""

    cursor.execute(sql)
    resultados = cursor.fetchall()
    print(resultados)
    conn.commit()
    conn.close()
    return resultados

if __name__ == "__main__":
    system("fastapi dev " + __file__)
    