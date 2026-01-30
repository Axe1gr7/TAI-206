#importaciones
from typing import Optional
from fastapi import FastAPI
import asyncio
#tiempo de espera de una peticion es de prueba 

usuarios=[
    {"id":1,"nombre":"axel","edad":21},
    {"id":2,"nombre":"chola","edad":17},
    {"id":3,"nombre":"cheyene","edad":90},
]

#inicialiacion 
app= FastAPI(
    title= 'mi primera api',
    description='AxelGR',
    version='1.0'
)
#mostramos ladescripcion de documentacion

#endpoints
@app.get("/", tags=['inicio'])
async def helloworld():
    return {"mensaje":" hello world FastAPI"} 


@app.get("/bienvenidos", tags=['inicio'])
async def bienvenida():
    return {"mensaje":" bienvenido a mi primerita API"}



#27/01/26
@app.get("/v1/calificaciones", tags=['Asincronia'])
#tags nos ayuda a seccionar las partes de nuestra documentacion por apartados
async def calificaciones():
    await asyncio.sleep(7)
    #se muestra la peticion pero con una demora de tiempo pero en cuanto se libere se recibira la peticion 
    return {"mensaje":" Tu calificacion en TAI es 10"} 

#obligatorio
@app.get("/v1/usuarios/{id}", tags=['Parametros Obligatorios'])
async def ConsultaUsuarios(id:int):
    await asyncio.sleep(3)
    return {"Usuario Encontrado":id}

#opcional
@app.get("/v1/usuarios_op/", tags=['Parametros opcionales'])
async def ConsultaOp(id: Optional[int]=None):
    await asyncio.sleep(3)
    if id is not None:
        return {"Usuario Encontrado":id}


@app.get("/v1/usuarios_op/", tags=["Parametro Opcional"])
async def consultaOp(id: Optional[int] = None):
    await asyncio.sleep(3)
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id: 
                return {"usuario encontrado": id, "Datos": usuario}
        return {"mensaje": "Usuario no encontrado"}  
    else:
        return {"mensaje": "No se proporciono Id"} 
    