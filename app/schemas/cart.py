from typing import List

from pydantic import BaseModel, Field


class AddToCartRequest(BaseModel):
    user_id: int
    product_id: int
    quantity: int = Field(..., gt=0)


class RemoveFromCartRequest(BaseModel):
    user_id: int
    product_id: int


class CartItem(BaseModel):
    product_id: int
    quantity: int
    price: float
    total_price: float


class CartResponse(BaseModel):
    user_id: int
    items: List[CartItem]
    subtotal: float