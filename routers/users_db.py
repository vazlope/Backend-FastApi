from fastapi import HTTPException, APIRouter, status
from DB.models.user import User
from DB.schemas.user import user_schema, users_schema
from DB.client import db_client
from bson import ObjectId


router = APIRouter(prefix= "/userdb",
                   tags = ["userdb"],
                   responses= {404: {"message":"Not found"}})



user_list = []


def search_user_by_email(email: int):
    try:
        user = db_client.users.find_one({"email": email})
        return User(**user_schema(user))
    except:
        return {"error" : "No user found"}

def search_user(field: int, key):
    try:
        user = db_client.users.find_one({field: key})
        return User(**user_schema(user))
    except:
        return {"error" : "No user found"}


@router.get("/", response_model= list[User]) #! query  
async def users():
    return users_schema(db_client.users.find())

@router.get("/{id}") #! path
async def user(id: str):
    return search_user("_id", ObjectId(id))


@router.get("/") #! query  
async def user(id: str):
    return search_user("_id", ObjectId(id))


@router.post("/", response_model= User ,status_code=status.HTTP_201_CREATED) #! POST
async def user(user: User):
    if type(search_user("email", user.email)) == User:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = "El usuario ya existe")
 
    user_dict = dict(user)
    del user_dict["id"]

    id = db_client.users.insert_one(user_dict).inserted_id

    new_user = user_schema(db_client.users.find_one({"_id": id}))

    return User(**new_user)


@router.put("/", response_model= User) #! PUT
async def user(user: User):
    
    user_dict = dict(user)
    del user_dict["id"]

    try:
        db_client.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)
    
    except:
        return {"error":"No se ha actualizado el usuario"}
    
    return search_user("_id", ObjectId(user.id))
    
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT) #! DELETE
async def user(id: str):
    found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})

    if not found:
        return {"error":"No se ha borrado el usuario"}