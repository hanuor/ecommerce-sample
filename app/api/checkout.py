from fastapi import APIRouter, status

from app.schemas.checkout import (
    CheckoutRequest,
    CheckoutResponse,
)

# from app.services.checkout_service import CheckoutService

router = APIRouter()

# checkout_service = CheckoutService()


@router.post(
    "",
    response_model=CheckoutResponse,
    status_code=status.HTTP_200_OK,
    summary="Checkout cart"
)
async def checkout(request: CheckoutRequest):
    """
    Checkout the user's cart.

    Steps performed:
    - Validate cart exists
    - Validate inventory
    - Validate discount code (if provided)
    - Create order
    - Deduct inventory
    - Generate coupon (every Nth order)
    - Clear cart
    """

    # return await checkout_service.checkout(request)

    return CheckoutResponse(
        order_id=1,
        subtotal=1000,
        discount=100,
        total=900,
        generated_coupon=None,
    )