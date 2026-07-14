import json
from datetime import datetime
from typing import List

from app.core.redis import redis_client
from app.schemas.checkout import OrderItem


class OrderRepository:

    ORDER_COUNTER = "counter:orders"
    ORDER_SET = "orders"

    @staticmethod
    def create_order(
        user_id: int,
        items: List[OrderItem],
        subtotal: float,
        discount: float,
        total: float,
    ) -> int:
        """
        Creates a new order.

        Returns the generated order id.
        """

        order_id = redis_client.incr(
            OrderRepository.ORDER_COUNTER
        )

        order_key = f"order:{order_id}"

        redis_client.hset(
            order_key,
            mapping={
                "id": order_id,
                "user_id": user_id,
                "subtotal": subtotal,
                "discount": discount,
                "total": total,
                "created_at": datetime.utcnow().isoformat(),
            },
        )

        items_key = f"order:{order_id}:items"

        for item in items:

            redis_client.rpush(
                items_key,
                item.model_dump_json()
            )

        redis_client.sadd(
            OrderRepository.ORDER_SET,
            order_id
        )

        return order_id

    @staticmethod
    def get_order(order_id: int):

        key = f"order:{order_id}"

        order = redis_client.hgetall(key)

        if not order:
            return None

        items_key = f"order:{order_id}:items"

        items = [
            json.loads(item)
            for item in redis_client.lrange(
                items_key,
                0,
                -1
            )
        ]

        return {
            "order": order,
            "items": items,
        }

    @staticmethod
    def list_orders():

        orders = []

        for order_id in redis_client.smembers(
            OrderRepository.ORDER_SET
        ):

            order = OrderRepository.get_order(
                int(order_id)
            )

            if order:
                orders.append(order)

        return orders