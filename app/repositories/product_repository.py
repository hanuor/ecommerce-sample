from typing import List, Optional

from app.core.redis import redis_client
from app.schemas.product import ProductCreate, ProductResponse


class ProductRepository:

    PRODUCT_COUNTER = "counter:products"
    PRODUCT_SET = "products"

    @staticmethod
    def create_product(product: ProductCreate) -> ProductResponse:
        """
        Creates a new product.
        """

        product_id = redis_client.incr(ProductRepository.PRODUCT_COUNTER)

        key = f"product:{product_id}"

        redis_client.hset(
            key,
            mapping={
                "id": product_id,
                "name": product.name,
                "price": product.price,
                "stock": product.stock,
            },
        )

        redis_client.sadd(ProductRepository.PRODUCT_SET, product_id)

        return ProductResponse(
            id=product_id,
            name=product.name,
            price=product.price,
            stock=product.stock,
        )

    @staticmethod
    def get_product(product_id: int) -> Optional[ProductResponse]:
        """
        Returns a single product.
        """

        key = f"product:{product_id}"

        product = redis_client.hgetall(key)

        if not product:
            return None

        return ProductResponse(
            id=int(product["id"]),
            name=product["name"],
            price=float(product["price"]),
            stock=int(product["stock"]),
        )

    @staticmethod
    def get_all_products() -> List[ProductResponse]:
        """
        Returns all products.
        """

        product_ids = redis_client.smembers(ProductRepository.PRODUCT_SET)

        products = []

        for product_id in product_ids:
            product = ProductRepository.get_product(int(product_id))

            if product:
                products.append(product)

        return products

    @staticmethod
    def update_stock(product_id: int, new_stock: int) -> bool:
        """
        Updates inventory.
        """

        key = f"product:{product_id}"

        if not redis_client.exists(key):
            return False

        redis_client.hset(key, "stock", new_stock)

        return True

    @staticmethod
    def decrement_stock(product_id: int, quantity: int) -> bool:
        """
        Atomically decrement stock.

        Returns False if insufficient inventory.
        """

        key = f"product:{product_id}"

        pipe = redis_client.pipeline()

        while True:
            try:
                pipe.watch(key)

                stock = pipe.hget(key, "stock")

                if stock is None:
                    pipe.unwatch()
                    return False

                stock = int(stock)

                if stock < quantity:
                    pipe.unwatch()
                    return False

                pipe.multi()

                pipe.hset(
                    key,
                    "stock",
                    stock - quantity,
                )

                pipe.execute()

                return True

            except Exception:
                continue

            finally:
                pipe.reset()