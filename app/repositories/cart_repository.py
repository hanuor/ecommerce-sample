from typing import List

from app.core.redis import redis_client
from app.repositories.product_repository import ProductRepository
from app.schemas.cart import CartItem, CartResponse


class CartRepository:

    @staticmethod
    def add_item(
        user_id: int,
        product_id: int,
        quantity: int,
    ) -> None:
        """
        Adds an item to the cart.
        If already present, increments quantity.
        """

        key = f"cart:{user_id}"

        redis_client.hincrby(
            key,
            product_id,
            quantity
        )

    @staticmethod
    def remove_item(
        user_id: int,
        product_id: int,
    ) -> None:
        """
        Removes a product completely from cart.
        """

        key = f"cart:{user_id}"

        redis_client.hdel(
            key,
            product_id
        )

    @staticmethod
    def clear_cart(user_id: int) -> None:
        """
        Deletes the cart.
        """

        redis_client.delete(
            f"cart:{user_id}"
        )

    @staticmethod
    def get_cart(user_id: int) -> CartResponse:
        """
        Returns complete cart.
        """

        key = f"cart:{user_id}"

        cart = redis_client.hgetall(key)

        items: List[CartItem] = []

        subtotal = 0

        for product_id, quantity in cart.items():

            product = ProductRepository.get_product(
                int(product_id)
            )

            if product is None:
                continue

            quantity = int(quantity)

            total_price = quantity * product.price

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
    def is_empty(user_id: int) -> bool:

        return redis_client.hlen(
            f"cart:{user_id}"
        ) == 0