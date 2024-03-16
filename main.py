from enum import Enum
from fastapi import FastAPI
from routers import products, users, user, jwt_auth_users, basic_auth_users, users_db
from fastapi.staticfiles import StaticFiles


app = FastAPI()

#routers
app.include_router(products.router)
app.include_router(users.router)
app.include_router(user.router)
app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)
app.include_router(users_db.router)
#Recursos estaticos
app.mount("/static", StaticFiles(directory="static"), name = "static")

@app.get("/")
async def main():
    return "Hola mundo! y Pily"

@app.get("/url")
async def read_file():
    return {"www.pabloscript.com"}
