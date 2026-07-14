from app.repositories.product_repository import ProductRepository
from app.repositories.coupon_repository import CouponRepository
from app.repositories.stats_repository import StatsRepository

from app.schemas.product import (
    ProductCreate,
    ProductResponse,
)

from app.schemas.admin import (
    CouponResponse,
    StatsResponse,
)


class AdminService:

    DEFAULT_DISCOUNT_PERCENTAGE = 10

    @staticmethod
    def create_product(
        product: ProductCreate,
    ) -> ProductResponse:
        """
        Creates a new product.
        """

        return ProductRepository.create_product(product)

    @staticmethod
    def list_products():
        """
        Returns all products.
        """

        return ProductRepository.get_all_products()

    @staticmethod
    def generate_discount() -> CouponResponse:
        """
        Generates a coupon manually.

        This endpoint is intended only for testing/admin use.
        During normal checkout, coupons are generated automatically
        after every Nth successful order.
        """

        coupon = CouponRepository.create_coupon(
            percentage=AdminService.DEFAULT_DISCOUNT_PERCENTAGE,
            generated_for_order=-1,
        )

        StatsRepository.increment_discount_codes_generated()

        return coupon

    @staticmethod
    def list_coupons():
        """
        Returns all coupons.
        """

        return CouponRepository.list_coupons()

    @staticmethod
    def get_stats() -> StatsResponse:
        """
        Returns store statistics.
        """

        return StatsRepository.get_stats()