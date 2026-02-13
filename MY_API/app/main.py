#importaciones
from typing import Optional
from fastapi import FastAPI,status,HTTPException
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
@app.get("/v1/prametroO/{id}", tags=['Parametros Obligatorios'])
async def ConsultaUsuarios(id:int):
    await asyncio.sleep(3)
    return {"Usuario Encontrado":id}

#opcional
@app.get("/v1/parametroOP/", tags=['Parametros opcionales'])
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
    
#verbos http tarea put, delete
@app.get("/v1/usuario/{id}", tags=['Crud Usuario'])
async def ConsultaUsuarios():
    return{
        "status":"200",
        "total":len(usuarios),
        "data":usuarios
    }

@app.post("/v1/AgregarUsuario/{id}", tags=['Crud Usuario'])
async def AgregarUsuarios(usuario:dict):
    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            raise HTTPException(
                status_code=400,
                detail="ID existente"
            )
    usuarios.append(usuario)
    return{
        "mensaje":"usuario agregado correctamente",
        "datos":usuario,
        "status":200
    } 
    
# put
@app.put("/v1/ActualizarUsuario/{id}", tags=['Crud Usuario'])
async def actualizar_usuario(id: int, usuario_actualizado: dict):
    # Buscar el usuario por id
    for usr in usuarios:
        if usr["id"] == id:
            # Actualizar solo los campos proporcionados (nombre, edad)
            if "nombre" in usuario_actualizado:
                usr["nombre"] = usuario_actualizado["nombre"]
            if "edad" in usuario_actualizado:
                usr["edad"] = usuario_actualizado["edad"]
            return {
                "mensaje": "Usuario actualizado correctamente",
                "datos": usr,
                "status": 200
            }
    # Si no se encuentra el id, lanzar excepción 404
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuario no encontrado"
    )


#delete 
@app.delete("/v1/EliminarUsuario/{id}", tags=['Crud Usuario'])
async def eliminar_usuario(id: int):
    # Buscar el índice del usuario por id
    for i, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuario_eliminado = usuarios.pop(i)
            return {
                "mensaje": "Usuario eliminado correctamente",
                "datos": usuario_eliminado,
                "status": 200
            }
    # Si no se encuentra el id, lanzar excepción 404
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuario no encontrado"
    )