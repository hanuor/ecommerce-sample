from fastapi import HTTPException, status

from app.core.config import settings
from typing import Optional

from app.repositories.cart_repository import CartRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.coupon_repository import CouponRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.stats_repository import StatsRepository

from app.schemas.checkout import (
    CheckoutRequest,
    CheckoutResponse,
    OrderItem,
)


class CheckoutService:

    @staticmethod
    def checkout(request: CheckoutRequest) -> CheckoutResponse:
        cart = CartRepository.get_cart(request.user_id)

        items, subtotal, total_items = CheckoutService._validate_cart(cart)

        discount = CheckoutService._apply_coupon(
            request.discount_code,
            subtotal,
        )

        total = subtotal - discount

        CheckoutService._update_inventory(items)

        order_id = OrderRepository.create_order(
            user_id=request.user_id,
            items=items,
            subtotal=subtotal,
            discount=discount,
            total=total,
        )

        StatsRepository.increment_orders()
        StatsRepository.increment_items(total_items)
        StatsRepository.increment_revenue(total)

        if discount:
            StatsRepository.increment_discount_given(discount)

        if request.discount_code:
            CouponRepository.mark_coupon_used(
                request.discount_code,
                request.user_id,
            )

        generated_coupon = None

        if order_id % settings.NTH_ORDER == 0:
            coupon = CouponRepository.create_coupon(
                percentage=settings.DISCOUNT_PERCENTAGE,
                generated_for_order=order_id,
            )

            StatsRepository.increment_discount_codes_generated()

            generated_coupon = coupon.code

        CartRepository.clear_cart(request.user_id)

        return CheckoutResponse(
            order_id=order_id,
            items=items,
            subtotal=subtotal,
            discount=discount,
            total=total,
            generated_coupon=generated_coupon,
        )
    
    @staticmethod
    def _validate_cart(cart: dict):
        """
        Validates the cart and returns:
        - items
        - subtotal
        - total_items
        """

        if not cart:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cart is empty."
            )

        items = []
        subtotal = 0
        total_items = 0

        for product_id, quantity in cart.items():

            product = ProductRepository.get_product(int(product_id))

            if product is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product {product_id} not found."
                )

            quantity = int(quantity)

            if quantity <= 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid quantity for product {product_id}."
                )

            if quantity > product.stock:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Insufficient stock for product {product_id}."
                )

            subtotal += quantity * product.price
            total_items += quantity

            items.append(
                OrderItem(
                    product_id=product.id,
                    quantity=quantity,
                    price=product.price,
                )
            )

        return items, subtotal, total_items
        
    @staticmethod
    def _apply_coupon(
        coupon_code: Optional[str],
        subtotal: float,
    ) -> float:
        """
        Applies the coupon and returns the discount amount.
        """

        if not coupon_code:
            return 0

        coupon = CouponRepository.validate_coupon(
            coupon_code
        )

        if coupon is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or already used coupon."
            )

        percentage = int(coupon["percentage"])

        return subtotal * percentage / 100
    
    @staticmethod
    def _update_inventory(items: list[OrderItem]):
        """
        Deduct inventory for purchased items.
        """

        for item in items:

            success = ProductRepository.decrement_stock(
                item.product_id,
                item.quantity,
            )

            if not success:
                raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock for product {item.product_id}."
            )