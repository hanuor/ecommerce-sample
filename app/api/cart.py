from fastapi import APIRouter, status

from app.schemas import (
    AddToCartRequest,
    CartResponse,
)

from app.services.cart_service import CartService

router = APIRouter()

cart_service = CartService()


@router.post(
    "/items",
    response_model=CartResponse,
    status_code=status.HTTP_200_OK,
    summary="Add item to cart"
)
async def add_item_to_cart(request: AddToCartRequest):
    """
    Add or update an item in the user's cart.

    If the product already exists in the cart,
    its quantity will be incremented.
    """

    # return await cart_service.add_item(request)
    return CartService.add_item(request)
    # return CartResponse(
    #     user_id=request.user_id,
    #     items=[],
    #     subtotal=0
    # )


@router.get(
    "/{user_id}",
    response_model=CartResponse,
    summary="Get cart"
)
async def get_cart(user_id: int):
    """
    Retrieve the current shopping cart.
    """

    # return await cart_service.get_cart(user_id)
    return CartService.get_cart(user_id)
    # return CartResponse(
    #     user_id=user_id,
    #     items=[],
    #     subtotal=0
    # )


@router.delete(
    "/{user_id}/items/{product_id}",
    response_model=CartResponse,
    summary="Remove item from cart"
)
async def remove_item_from_cart(
    user_id: int,
    product_id: int
):
    """
    Remove a specific product from the cart.
    """

    # return await cart_service.remove_item(user_id, product_id)
    return CartService.remove_item(user_id, product_id)
    # return CartResponse(
    #     user_id=user_id,
    #     items=[],
    #     subtotal=0
    # )


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Clear cart"
)
async def clear_cart(user_id: int):
    """
    Remove all items from the user's cart.
    """
    CartService.clear_cart(user_id)
    # await cart_service.clear_cart(user_id)

    return