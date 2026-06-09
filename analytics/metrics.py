from models.analytics import AnalyticsResult
from statistics import median


class AnalyticsEngine:

    @staticmethod
    def generate(
        competitors
    ) -> AnalyticsResult:

        ratings = [
            c.rating
            for c in competitors
            if c.rating is not None
        ]

        reviews = [
            c.review_count
            for c in competitors
            if c.review_count is not None
        ]

        top_rated = max(
            competitors,
            key=lambda c: c.rating or 0
        )

        most_reviewed = max(
            competitors,
            key=lambda c: c.review_count or 0
        )

        ranks = [
            c.rank
            for c in competitors
            if c.rank is not None
        ]

        return AnalyticsResult(
            competitor_count=len(
                competitors
            ),

            average_rating=round(
                sum(ratings) / len(ratings),
                2
            ),

            average_reviews=round(
                sum(reviews) / len(reviews),
                2
            ),

            median_reviews=round(
                median(reviews),
                2
            ),

            top_rated_competitor=(
                top_rated.name
            ),

            highest_reviewed_competitor=(
                most_reviewed.name
            ),

            average_rank=round(
                sum(ranks) / len(ranks),
                2
            )
        )