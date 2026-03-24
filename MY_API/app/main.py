from fastapi import FastAPI 
from app.data.db import engine
from app.routers import usuarios,misc
from app.data.db import engine
from app.data import usuario

usuario.Base.metadata.create_all(bind=engine)

#inicialiacion 
app= FastAPI(
    title= 'mi primera api',
    description='AxelGR',
    version='1.0'
)

#importamos los imports
app.include_router(usuarios.router)
app.include_router(misc.router) 
