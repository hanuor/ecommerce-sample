from fastapi import HTTPException, status

from app.repositories.cart_repository import CartRepository
from app.repositories.product_repository import ProductRepository

from app.schemas.cart import (
    AddToCartRequest,
    CartItem,
    CartResponse,
)


class CartService:

    @staticmethod
    def add_item(request: AddToCartRequest) -> CartResponse:
        """
        Add an item to the user's cart.
        """

        product = ProductRepository.get_product(
            request.product_id
        )

        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found."
            )

        if request.quantity > product.stock:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient stock."
            )

        CartRepository.add_item(
            user_id=request.user_id,
            product_id=request.product_id,
            quantity=request.quantity,
        )

        return CartService.get_cart(request.user_id)

    @staticmethod
    def get_cart(user_id: int) -> CartResponse:
        """
        Returns the user's cart.
        """

        cart = CartRepository.get_cart(user_id)

        items = []
        subtotal = 0

        for product_id, quantity in cart.items():

            product = ProductRepository.get_product(
                int(product_id)
            )

            if product is None:
                continue
            print(f"Product: {product}, Quantity: {quantity}")
            total_price = product.price * int(quantity)

            subtotal += total_price

            items.append(
                CartItem(
                    product_id=product.id,
                    quantity=quantity,
                    price=product.price,
                    total_price=total_price,
                )
            )

        return CartResponse(
            user_id=user_id,
            items=items,
            subtotal=subtotal,
        )

    @staticmethod
    def remove_item(
        user_id: int,
        product_id: int,
    ) -> CartResponse:
        """
        Remove a product from the cart.
        """

        CartRepository.remove_item(
            user_id=user_id,
            product_id=product_id,
        )

        return CartService.get_cart(user_id)

    @staticmethod
    def clear_cart(user_id: int) -> None:
        """
        Clears the user's cart.
        """

        CartRepository.clear_cart(user_id)