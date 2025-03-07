from fastapi import FastAPI
from pydantic import BaseModel
import os

app = FastAPI()

class UpdateChat(BaseModel):
    user: str

class SendChat(BaseModel):
    user: str
    message: str

@app.post("/data")
async def Data(data: UpdateChat):
    return datas

@app.post("/send")
async def Send(data: SendChat):
    datas = data.message
