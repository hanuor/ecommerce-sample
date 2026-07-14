from typing import Optional

from pydantic import BaseModel


class CheckoutRequest(BaseModel):
    user_id: int
    discount_code: Optional[str] = None


class CheckoutResponse(BaseModel):
    order_id: int
    subtotal: float
    discount: float
    total: float
    generated_coupon: Optional[str] = None