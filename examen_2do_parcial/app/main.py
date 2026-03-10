from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime

# --- DATOS SIMULADOS ---
citas = [
    {
        "id": 1,
        "nomnre": "gabriel",
        "motivo": "gripe",
        "anio": 2030,
        "mes": 10,
        "dia": 30,
        "confirmacion": True
    },
    {
        "id": 2,
        "nomnre": "edith",
        "motivo": "tos",
        "anio": 2030,
        "mes": 10,
        "dia": 28,
        "confirmacion": False
    },
    {
        "id": 3,
        "nomnre": "isacc",
        "motivo": "chorro",
        "anio": 2030,
        "mes": 10,
        "dia": 18,
        "confirmacion": True
    }
]
# --- MODELOS PYDANTIC --

class citass(BaseModel):
    id: int = Field(..., gt=0, description="Identificador único de la cita")
    nombre: str = Field(..., min_length=3, max_length=50, description="Nombre del usuario")
    anio: int = Field(..., ge=2026, le=2030, description="que no sea mayor a el año actual")
    mes: int = Field(..., ge=1, le=12, description="mes valido del 1 al 12")
    dia: int = Field(..., ge=1, le=31, description="mes valido del 1 al 31")
    confirmacion: bool = Field(default= False)



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
    
    citas.append(citass.model_dump())
    return {"mensaje": "cita registrado correctamente", "cita": citas}

@app.post("/v1/Agregarcitas/{id}", tags=['citas'])
async def Agregarcitas(citas:citass):
    for citas in citass:
        if citas["id"] == citas.id("id"):
            raise HTTPException(
                status_code=400,
                detail="ID existente"
            )
    citas.append(citas)
    return{
        "mensaje":"usuario agregado correctamente",
        "datos":citas,
        "status":200
    } 



@app.get("/v1/listar/", tags=['citas'])
async def listar_listar_citas():
    citas_confirmadas = [l for l in citas if l["confirmacion"] == True]
    return {
        "total_disponibles": len(citas_confirmadas),
        "data": citas_confirmadas
    }
    



@app.get("/v1/citas/buscar/id", tags=['citas'])
async def buscar_citas_id(id: int):
    resultados = [l for l in citas if id in l["id"]]
    if not resultados:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron citas con ese id")
    return resultados

@app.get("/v1/citas/buscar/id_S", tags=['citas'])
async def consultas_citas(id:int = None):
    if id is not None:
        for citass in citas:
            if citass["id"] == id: 
                return {"usuario encontrado": id, "Datos": consultas_citas}
        return {"mensaje": "Usuario no encontrado"}  
    else:
        return {"mensaje": "No se proporciono Id"} 



@app.put("/v1/citas/confirmar/{cita_id}", tags=['citas'], status_code=status.HTTP_200_OK)
async def confirmar_cita(cita_id: int):
    for citass in citas:
        if citas["id"] == cita_id:
            if citas["confirmacion"] == True:
                return {"mensaje": "La cita ya se encontraba confirmada)"}
            
            citas["confirmacion"] = False
            return {"mensaje": "cita confirmada correctamente", "status": 200, "cita": citass}
            
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="cita no encontrada")


