from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime

# --- DATOS SIMULADOS ---
citas = [
    {
        "id": 1,
        "nomnre": "gabriel",
        "motivo": "gripe",
        "anio": 1949,
        "mes": 10,
        "dia": 30,
        "confirmacion": True
    },
    {
        "id": 2,
        "nomnre": "edith",
        "motivo": "tos",
        "anio": 1949,
        "mes": 10,
        "dia": 28,
        "confirmacion": False
    },
    {
        "id": 3,
        "nomnre": "isacc",
        "motivo": "chorro",
        "anio": 1949,
        "mes": 10,
        "dia": 18,
        "confirmacion": True
    }
]

agenda = [
    {"cita_id":2, "usuario": "gabriel", "confirmacion":True}
]



# --- MODELOS PYDANTIC --

class citass(BaseModel):
    id: int = Field(..., gt=0, description="Identificador único de la cita")
    nombre: str = Field(..., min_length=3, max_length=50, description="Nombre del usuario")
    anio: int = Field(..., gt=1450, ge=datetime.now().year, description="que no sea mayor a el año actual")
    mes: int = Field(..., ge=1, le=12, description="mes valido del 1 al 12")
    dia: int = Field(..., ge=1, le=31, description="mes valido del 1 al 31")
    confirmacion: bool = Field(..., default= False)



# --- CONFIGURACIÓN DE LA API ---
app = FastAPI(
    title='API de Libros',
    description='AxelGR',
    version='1.0'
)

# --- ENDPOINTS ---

@app.get("/", tags=['Inicio'])
async def inicio():
    return {"mensaje": "Bienvenido a la API de Libros."}

@app.post("/v1/crear_cita/", tags=['citas'], status_code=status.HTTP_201_CREATED)
async def crear_cita(citas: citass):
    for l in citas:
        if l["id"] == citas.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La cita ya existe")
    
    citas.append(citas.model_dump())
    return {"mensaje": "Libro registrado correctamente", "libro": citas}


@app.get("/v1/listar/", tags=['Libros'])
async def listar_listar_citas():
    citas_confirmadas = [l for l in citas if l["confirmacion"] == True]
    return {
        "total_disponibles": len(citas_confirmadas),
        "data": citas_confirmadas
    }
    



@app.get("/v1/libros/disponibles", tags=['Libros'])
async def listar_libros_disponibles():
    libros_disponibles = [l for l in libros if l["estado"] == 1]
    return {
        "total_disponibles": len(libros_disponibles),
        "data": libros_disponibles
    }

@app.get("/v1/libros/buscar", tags=['Libros'])
async def buscar_libro(nombre: str):
    resultados = [l for l in libros if nombre.lower() in l["titulo"].lower()]
    if not resultados:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron libros con ese nombre")
    return resultados


# -- prestamos --
@app.post("/v1/prestamos/{libro_id}", tags=['Préstamos'])
async def registrar_prestamo(libro_id: int, usuario: UsuarioBase):
    for libro in libros:
        if libro["id"] == libro_id:
            if libro["estado"] == 0:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Conflict: El libro ya está prestado")
            
            libro["estado"] = 0
            nuevo_prestamo = {
                "libro_id": libro_id,
                "usuario": usuario.nombre,
                "correo": usuario.correo
            }
            prestamos.append(nuevo_prestamo)
            return {"mensaje": "Préstamo registrado exitosamente", "detalle": nuevo_prestamo}
            
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Libro no encontrado")

@app.put("/v1/libros/devolver/{libro_id}", tags=['Préstamos'], status_code=status.HTTP_200_OK)
async def devolver_libro(libro_id: int):
    for libro in libros:
        if libro["id"] == libro_id:
            if libro["estado"] == 1:
                return {"mensaje": "El libro ya se encontraba disponible (estado 1)"}
            
            libro["estado"] = 1
            return {"mensaje": "Libro devuelto correctamente", "status": 200, "libro": libro}
            
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Libro no encontrado")

@app.delete("/v1/prestamos/eliminar/{libro_id}", tags=['Préstamos'])
async def eliminar_prestamo(libro_id: int):
    for i, p in enumerate(prestamos):
        if p["libro_id"] == libro_id:
            prestamo_eliminado = prestamos.pop(i)
            return {"mensaje": "Registro de préstamo eliminado", "datos": prestamo_eliminado}
            
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT, 
        detail="Conflict: El registro de préstamo ya no existe"
    )