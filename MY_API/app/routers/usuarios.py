from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from app.models.usuario import UsuarioBase
from app.data.database import usuarios
from app.security.auth import verificar_Petcion

from sqlalchemy.orm import Session 
from app.data.usuario import Usuario
from app.data.db import get_db

router = APIRouter(
    prefix= "/v1/usuarios", 
    tags=["Crud Usuario"]
)

#verbos http tarea put, delete
@router.get("/")
async def leer_Usuarios(db: Session = Depends(get_db)): 

    Consultausuarios = db.query(Usuario).all()
    return {
        "status": "200",
        "total": len(Consultausuarios),
        "data": Consultausuarios
    }

@router.post("/", status_code=status.HTTP_201_CREATED) 
async def AgregarUsuarios(usuariop: UsuarioBase, db: Session = Depends(get_db)):
    nuevo_usuario = Usuario(nombre=usuariop.nombre, edad=usuariop.edad)
    
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    
    return {
        "mensaje": "usuario agregado correctamente",
        "datos": nuevo_usuario, 
        "status": 201
    }
    
    
    


# put
@router.put("/{id}", status_code=status.HTTP_200_OK)
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
@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def eliminar_usuario(id: int, usuarioAuth:str= Depends(verificar_Petcion)):
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
    
