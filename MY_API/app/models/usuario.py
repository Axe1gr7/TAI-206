#modelo de validacion pydantic
from pydantic import BaseModel, Field
class UsuarioBase(BaseModel):
    nombre : str = Field(...,min_length=3,max_length=50,description="Nombre del usuario",example="axel")
    edad : int = Field(...,ge=0,le=121,description="la edad de 0 a 121",example="21")

