import secrets
from typing import List, Optional

from app.core.redis import redis_client
from app.schemas.admin import CouponResponse


class CouponRepository:

    COUPON_SET = "coupons"

    @staticmethod
    def create_coupon(
        percentage: int,
        generated_for_order: int,
    ) -> CouponResponse:
        """
        Creates a new coupon.
        """

        code = secrets.token_hex(4).upper()

        key = f"coupon:{code}"

        redis_client.hset(
            key,
            mapping={
                "code": code,
                "percentage": percentage,
                "used": "false",
                "generated_for_order": generated_for_order,
                "used_by": "",
            },
        )

        redis_client.sadd(
            CouponRepository.COUPON_SET,
            code,
        )

        return CouponResponse(
            code=code,
            percentage=percentage,
            used=False,
        )

    @staticmethod
    def get_coupon(
        code: str,
    ) -> Optional[CouponResponse]:

        key = f"coupon:{code}"

        coupon = redis_client.hgetall(key)

        if not coupon:
            return None

        return CouponResponse(
            code=coupon["code"],
            percentage=int(coupon["percentage"]),
            used=coupon["used"] == "true",
        )

    @staticmethod
    def list_coupons() -> List[CouponResponse]:

        coupons = []

        for code in redis_client.smembers(
            CouponRepository.COUPON_SET
        ):

            coupon = CouponRepository.get_coupon(code)

            if coupon:
                coupons.append(coupon)

        return coupons

    @staticmethod
    def mark_coupon_used(
        code: str,
        user_id: int,
    ) -> bool:

        key = f"coupon:{code}"

        if not redis_client.exists(key):
            return False

        redis_client.hset(
            key,
            mapping={
                "used": "true",
                "used_by": user_id,
            },
        )

        return True