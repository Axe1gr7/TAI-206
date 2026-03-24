from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
import os 

#1. definiendo la url de conexion 

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://adm:123456@postgres:5432/DB_miapi"
)

#2. CREAMOS EL MOTOR DE CONEXION 

engine= create_engine(DATABASE_URL)

#3. agregamos el gestor de sesiones 

sesionlocal= sessionmaker(
    autocommit=False,
    autoflush=False,
    bind= engine)

#4 base declarativa para modelos 
Base= declarative_base()

#5 funciones para el manejo en session en los request 

def get_db():
    db= sesionlocal()
    try:
        yield db
    finally:
        db.close()