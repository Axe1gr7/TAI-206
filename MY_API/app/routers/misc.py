from fastapi import APIRouter
import asyncio
from typing import Optional
from app.data.database import usuarios

router = APIRouter(tags=["miscelanius"])


#endpoints
@router.get("/")
async def helloworld():
    return {"mensaje":" hello world FastAPI"} 


@router.get("/bienvenidos")
async def bienvenida():
    return {"mensaje":" bienvenido a mi primerita API"}



#27/01/26
@router.get("/v1/calificaciones")
#tags nos ayuda a seccionar las partes de nuestra documentacion por apartados
async def calificaciones():
    await asyncio.sleep(7)
    #se muestra la peticion pero con una demora de tiempo pero en cuanto se libere se recibira la peticion 
    return {"mensaje":" Tu calificacion en TAI es 10"} 

#obligatorio
@router.get("/v1/prametroO/{id}")
async def ConsultaUsuarios(id:int):
    await asyncio.sleep(3)
    return {"Usuario Encontrado":id}

#opcional
@router.get("/v1/parametroOP/")
async def ConsultaOp(id: Optional[int]=None):
    await asyncio.sleep(3)
    if id is not None:
        return {"Usuario Encontrado":id}


@router.get("/v1/usuarios_op/")
async def consultaOp(id: Optional[int] = None):
    await asyncio.sleep(3)
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id: 
                return {"usuario encontrado": id, "Datos": usuario}
        return {"mensaje": "Usuario no encontrado"}  
    else:
        return {"mensaje": "No se proporciono Id"} 
    

