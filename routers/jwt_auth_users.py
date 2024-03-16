from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

#PARAMETERS
ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "52f4905baed79e82f0704b724927d2870345f606a3c51596aec14be0c251fdf2"

#INSTANCIES
router = APIRouter(prefix="/auth",
                   tags = ["auth"],
                   responses= {404: {"message":"Not found"}})

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes= "bcrypt")

#CLASES
class User(BaseModel):
    useraname: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str
users_db = {
    "mouredev": {
        "useraname": "mouredev",
        "full_name": "Brais Moure",
        "email": "braismoure@gmail.com",
        "disabled": False,
        "password": "$2a$12$dtAtcCdiLZK/xOjjoL8al.WkHD7TOHpKvp16F27PBWCdmlvlmzjy6"
    },
    "mouredev2": {
        "useraname": "mouredev2",
        "full_name": "Brais Moure 2",
        "email": "braismoure2@gmail.com",
        "disabled": True,
        "password": "$2a$12$V9YZ7c.K56sOF0n73af9suWL9L8vK0ymw8jrgwPiyOpN09Q5lNSMW"
    } 
}

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

async def auth_user(token: str  = Depends(oauth2)):

    exception = HTTPException(
         status_code= status.HTTP_401_UNAUTHORIZED,
         detail= "Credenciales de autenticación invalidas",
         headers= {"www-Authenticate": "Bearer"})
     
    try:
        username = jwt.decode(token, SECRET, algorithms= [ALGORITHM]).get("sub")
        if username is None:
             raise exception        

    except JWTError:
         raise exception
    
    return search_user(username)
     
     
        

async def current_user(user: User = Depends(auth_user)):
    if not user:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "Credenciales de autenticación invalidas",
            headers= {"www-Authenticate": "Bearer"})
    
    if user.disabled:
                raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= "Usuario Inactivo")

    return user
    

#URL LOGIN
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST, detail= "EL usuario no es correcto")
    
    user = search_user_db(form.username)


    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
    
    
    access_token = {"sub" : user.useraname, 
                    "exp" : datetime.now() + timedelta(minutes=ACCESS_TOKEN_DURATION)}
    
    return {"access_token": jwt.encode(access_token, SECRET,algorithm= ALGORITHM), "token_type": "bearer"}


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user