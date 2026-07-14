from app.core.redis import redis_client
from app.schemas.admin import StatsResponse


class StatsRepository:

    STATS_KEY = "stats"

    @staticmethod
    def increment_orders() -> None:
        redis_client.hincrby(
            StatsRepository.STATS_KEY,
            "total_orders",
            1,
        )

    @staticmethod
    def increment_items(quantity: int) -> None:
        redis_client.hincrby(
            StatsRepository.STATS_KEY,
            "total_items_purchased",
            quantity,
        )

    @staticmethod
    def increment_revenue(amount: float) -> None:
        redis_client.hincrbyfloat(
            StatsRepository.STATS_KEY,
            "total_revenue",
            amount,
        )

    @staticmethod
    def increment_discount_given(amount: float) -> None:
        redis_client.hincrbyfloat(
            StatsRepository.STATS_KEY,
            "total_discount_given",
            amount,
        )

    @staticmethod
    def increment_discount_codes_generated() -> None:
        redis_client.hincrby(
            StatsRepository.STATS_KEY,
            "discount_codes_generated",
            1,
        )

    @staticmethod
    def get_stats() -> StatsResponse:

        stats = redis_client.hgetall(
            StatsRepository.STATS_KEY
        )

        return StatsResponse(
            total_orders=int(
                stats.get("total_orders", 0)
            ),
            total_items_purchased=int(
                stats.get("total_items_purchased", 0)
            ),
            total_revenue=float(
                stats.get("total_revenue", 0)
            ),
            total_discount_codes=int(
                stats.get("discount_codes_generated", 0)
            ),
            total_discount_given=float(
                stats.get("total_discount_given", 0)
            ),
        )