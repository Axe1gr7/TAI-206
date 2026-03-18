#importaciones
from fastapi import FastAPI
from app.routers import usuarios,misc

#inicialiacion 
app= FastAPI(
    title= 'mi primera api',
    description='AxelGR',
    version='1.0'
)

#importamos los imports
app.include_router(usuarios.router)
app.include_router(misc.router)