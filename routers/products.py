from fastapi import APIRouter


router = APIRouter(prefix="/products",
                   tags = ["products"],
                   responses= {404: {"message":"Not found"}})

product_list = ["Producto 1", "Producto 2","Producto 3","Producto 4","Producto 5"]

@router.get("/")
async def products():
    return product_list

@router.get("/{id}")
async def products(id: int):
    return product_list[id]

    










   
    
