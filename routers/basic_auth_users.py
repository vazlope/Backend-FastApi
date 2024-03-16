from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


router = APIRouter(prefix="/basic_auth",
                   tags = ["basic_auth"],
                   responses= {404: {"message":"Not found"}})

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

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
        "password": "123456"
    },
    "mouredev2": {
        "useraname": "mouredev2",
        "full_name": "Brais Moure 2",
        "email": "braismoure2@gmail.com",
        "disabled": True,
        "password": "654321"
    } 
}

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])


async def current_user(token: str = Depends(oauth2)):
    user =  search_user(token)
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


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST, detail= "EL usuario no es correcto")
    
    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
    
    return {"access_token": user.useraname, "token_type": "bearer"}


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
