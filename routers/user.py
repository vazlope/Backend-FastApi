from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel


router = APIRouter(prefix= "/user",
                   tags = ["user"],
                   responses= {404: {"message":"Not found"}})

#Entidad user
class User(BaseModel):
    id: int
    name: str
    surname: str
    age: int

user_list = [User(id = 1, name='Brais', surname='Moure', age=20),
             User(id = 2, name='Willy', surname='wonka', age=30),
             User(id = 3, name='Carlos', surname='V', age=40),
             User(id =4, name='John', surname='Doe', age=50)]


def search_user(id: int):
    users = filter(lambda user : user.id == id, user_list)
    try:
        return list(users)[0]
    except:
        return {"error" : "No user found"}


@router.get("/all")
async def users():
    return user_list

@router.get("/{id}") #! path
async def userpath(id: int):
    return search_user(id)


@router.get("/") #! query  
async def userquery(id: int):
    return search_user(id)


@router.post("/", response_model= User ,status_code=201) #! POST
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code= 404, detail = "El usuario ya existe")
    else:
        user_list.append(user)
        #save_user_db(user_list)
        return user

@router.put("/") #! PUT
async def user(user: User):
    found = False
    for index, saved_user in enumerate(user_list):
        if saved_user.id == user.id:
            user_list[index] = user
            found = True

    if not found:
        return {"error":"No se ha actualizado el usuario"}
    else:
        #save_user_db(user_list)
        return user
    
@router.delete("/{id}") #! DELETE
async def user(id: int):
    found = False
    for index, saved_user in enumerate(user_list):
        if saved_user.id == id:
            del user_list[index]
            #save_user_db(user_list)
            found = True

    if not found:
        return {"error":"No se ha borrado el usuario"}