#importaciones
from fastapi import FastAPI

#inicialiacion 
app=FastAPI()

#endpoints
@app.get("/")
async def helloworld():
    return {"mensaje":" hello world FastAPI"} 


@app.get("/bienvenidos")
async def bienvenida():
    return {"mensaje":" bienvenido a mi primerita API"}