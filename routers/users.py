from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix ="/users",
                   tags = ["users"],
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


@router.get("/")
async def users():
    return user_list












   
    
