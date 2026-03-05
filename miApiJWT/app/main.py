#importaciones
from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from pydantic import BaseModel, Field
import asyncio

# CONFIGURACIÓN DE SEGURIDAD

SECRET_KEY = "1310"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = .5

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# MODELOS PARA AUTENTICACIÓN 

class User(BaseModel):
    username: str
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str


# BASE DE DATOS FICTICIA DE USUARIOS 

usuarios_db = {
    "axel": {
        "username": "axel",
        "hashed_password": pwd_context.hash("1310"),
        "disabled": False,
    }
}


# FUNCIONES AUXILIARES DE AUTENTICACIÓN 
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(usuarios_db, username: str, password: str):
    user = get_user(usuarios_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



# DEPENDENCIAS DE USUARIO
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user_dict = usuarios_db.get(username)
    if user_dict is None:
        raise credentials_exception
    
    return UserInDB(**user_dict)

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Usuario inactivo")
    return current_user


usuarios=[
    {"id":1,"nombre":"axel","edad":21},
    {"id":2,"nombre":"chola","edad":17},
    {"id":3,"nombre":"cheyene","edad":90},
]
#modelo de validacion pydantic
#modelo de validacion pydantic
class UsuarioBase(BaseModel):
    id: int = Field(..., gt=0, description="identificador de usuario", json_schema_extra={"example": 1})
    nombre: str = Field(..., min_length=3, max_length=50, description="Nombre del usuario", json_schema_extra={"example": "axel"})
    edad: int = Field(..., ge=0, le=121, description="la edad de 0 a 121", json_schema_extra={"example": 21})


#inicialiacion 
app= FastAPI(
    title= 'mi primera api',
    description='AxelGR',
    version='1.0'
)




# ENDPOINT DE AUTENTICACIÓN 

@app.post("/token", response_model=dict, tags=["Autenticación"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(usuarios_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

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
async def ConsultaUsuariosObligatorio(id:int): # CORRECCIÓN: Nombre de función duplicado
    await asyncio.sleep(3)
    return {"Usuario Encontrado":id}

#opcional
@app.get("/v1/parametroOP/", tags=['Parametros opcionales'])
async def ConsultaOp(id: Optional[int]=None):
    await asyncio.sleep(3)
    if id is not None:
        return {"Usuario Encontrado":id}


@app.get("/v1/usuarios_op/", tags=["Parametro Opcional"])
async def consultaOpBusqueda(id: Optional[int] = None): # CORRECCIÓN: Nombre de función duplicado
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
async def ConsultaUsuarios(id: int): # CORRECCIÓN: Se agregó el parámetro {id} que faltaba
    return{
        "status":"200",
        "total":len(usuarios),
        "data":usuarios
    }

@app.post("/v1/AgregarUsuario/{id}", tags=['Crud Usuario'])
async def AgregarUsuarios(id: int, usuario: UsuarioBase):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail="ID existente"
            )
            
    usuarios.append(usuario.model_dump()) 
    
    return {
        "mensaje": "usuario agregado correctamente",
        "datos": usuario,
        "status": 200
    }
    
# ENDPOINTS PROTEGIDOS

@app.put("/v1/ActualizarUsuario/{id}", tags=['Crud Usuario'])
async def actualizar_usuario(
    id: int,
    usuario_actualizado: dict,
    current_user: User = Depends(get_current_active_user)
):
    for usr in usuarios:
        if usr["id"] == id:
            if "nombre" in usuario_actualizado:
                usr["nombre"] = usuario_actualizado["nombre"]
            if "edad" in usuario_actualizado:
                usr["edad"] = usuario_actualizado["edad"]
            return {
                "mensaje": "Usuario actualizado correctamente",
                "datos": usr,
                "status": 200
            }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuario no encontrado"
    )

@app.delete("/v1/EliminarUsuario/{id}", tags=['Crud Usuario'])
async def eliminar_usuario(
    id: int,
    current_user: User = Depends(get_current_active_user)
):
    for i, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuario_eliminado = usuarios.pop(i)
            return {
                "mensaje": "Usuario eliminado correctamente",
                "datos": usuario_eliminado,
                "status": 200
            }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuario no encontrado"
    )