from fastapi import FastAPI

from app.api.admin import router as admin_router
from app.api.cart import router as cart_router
from app.api.checkout import router as checkout_router

from app.services.admin_service import AdminService

app = FastAPI(
    title="E-Commerce Store",
    version="1.0.0",
)

app.include_router(
    cart_router,
    prefix="/cart",
    tags=["Cart"]
)

app.include_router(
    checkout_router,
    prefix="/checkout",
    tags=["Checkout"]
)

app.include_router(
    admin_router,
    prefix="/admin",
    tags=["Admin"]
)


# @app.get("/")
# async def health():
#     return {"status": "healthy"}