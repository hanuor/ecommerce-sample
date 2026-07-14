from typing import Optional, List
from pydantic import BaseModel, Field


# -------------------------
# Product
# -------------------------

class ProductCreate(BaseModel):
    name: str = Field(..., example="iPhone 16")
    price: float = Field(..., gt=0, example=99999)
    stock: int = Field(..., ge=0, example=50)


class ProductResponse(ProductCreate):
    id: int


# -------------------------
# Cart
# -------------------------

class AddToCartRequest(BaseModel):
    user_id: int
    product_id: int
    quantity: int = Field(..., gt=0)


class CartItem(BaseModel):
    product_id: int
    quantity: int
    price: float


class CartResponse(BaseModel):
    user_id: int
    items: List[CartItem]
    subtotal: float


# -------------------------
# Checkout
# -------------------------

class CheckoutRequest(BaseModel):
    user_id: int
    discount_code: Optional[str] = None


class CheckoutResponse(BaseModel):
    order_id: int
    subtotal: float
    discount: float
    total: float
    generated_coupon: Optional[str] = None


# -------------------------
# Coupons
# -------------------------

class CouponResponse(BaseModel):
    code: str
    percentage: int
    used: bool


# -------------------------
# Store Statistics
# -------------------------

class StatsResponse(BaseModel):
    total_orders: int
    total_items_purchased: int
    total_revenue: float
    total_discount_codes: int
    total_discount_given: float