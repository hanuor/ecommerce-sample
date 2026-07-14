from pydantic import BaseModel


class CouponResponse(BaseModel):
    code: str
    percentage: int
    used: bool


class StatsResponse(BaseModel):
    total_orders: int
    total_items_purchased: int
    total_revenue: float
    total_discount_codes: int
    total_discount_given: float