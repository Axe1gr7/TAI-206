from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime

# --- DATOS SIMULADOS ---
libros = [
    {
        "id": 3,
        "titulo": "1984",
        "autor": "George Orwell",
        "anio": 1949,
        "paginas": 328,
        "estado": 1
    },
    {
        "id": 4,
        "titulo": "El resplandor",
        "autor": "Stephen King",
        "anio": 1977,
        "paginas": 447,
        "estado": 1
    },
    {
        "id": 5,
        "titulo": "Crónica de una muerte anunciada",
        "autor": "Gabriel García Márquez",
        "anio": 1981,
        "paginas": 150,
        "estado": 1
    },
    {
        "id": 6,
        "titulo": "El código Da Vinci",
        "autor": "Dan Brown",
        "anio": 2003,
        "paginas": 608,
        "estado": 1
    },
    {
        "id": 7,
        "titulo": "La sombra del viento",
        "autor": "Carlos Ruiz Zafón",
        "anio": 2001,
        "paginas": 576,
        "estado": 1
    }
]

prestamos = [
    {"libro_id": 2, "usuario": "Axel", "correo": "axel@ejemplo.com"}
]

# --- MODELOS PYDANTIC ---
class UsuarioBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=50, description="Nombre del usuario")
    correo: str = Field(..., pattern=r"^[^@]+@[^@]+$", description="Correo del usuario (debe contener @ y caracteres)")

class LibroBase(BaseModel):
    id: int = Field(..., gt=0, description="Identificador único del libro")
    titulo: str = Field(..., min_length=2, max_length=100, description="Nombre del libro")
    autor: str = Field(..., min_length=2, max_length=100, description="Autor del libro")
    anio: int = Field(..., gt=1450, le=datetime.now().year, description="Año de publicación (hasta el año actual)")
    paginas: int = Field(..., gt=1, description="Debe tener más de 1 página")
    estado: int = Field(1, ge=0, le=1, description="1 para disponible, 0 para prestado")


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

@app.post("/v1/libros/", tags=['Libros'], status_code=status.HTTP_201_CREATED)
async def registrar_libro(libro: LibroBase):
    for l in libros:
        if l["id"] == libro.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El ID del libro ya existe")
    
    libros.append(libro.model_dump())
    return {"mensaje": "Libro registrado correctamente", "libro": libro}

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