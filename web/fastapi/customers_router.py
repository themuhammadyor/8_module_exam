from fastapi import APIRouter


order_router = APIRouter(prefix="/customer")

@order_router.get("/")
async def get_orders():
    return {"message": "customer page"}