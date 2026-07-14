from fastapi import APIRouter, status

from app.schemas.checkout import (
    CheckoutRequest,
    CheckoutResponse,
)
from app.services.checkout_service import CheckoutService

router = APIRouter()


@router.post(
    "",
    response_model=CheckoutResponse,
    status_code=status.HTTP_200_OK,
    summary="Checkout cart",
)
async def checkout(request: CheckoutRequest):
    """
    Checkout the user's cart.
    """
    return CheckoutService.checkout(request)