from models.insights import (
    InsightResult
)


class InsightGenerator:

    @staticmethod
    def generate(
        competitors,
        analytics
    ) -> InsightResult:

        insights = []

        recommendations = []

        # Top Rated

        insights.append(
            f"{analytics.top_rated_competitor} "
            f"is the highest-rated competitor "
            f"with an average rating "
            f"of {analytics.average_rating}."
        )

        # Most Reviewed

        insights.append(
            f"{analytics.highest_reviewed_competitor} "
            f"has the largest review footprint "
            f"in the market."
        )

        # Traffic Leaders

        traffic_scores = {}

        for competitor in competitors:

            if not competitor.weekly_metrics:
                continue

            avg_traffic = sum(
                day.avg_traffic_pct
                for day in competitor.weekly_metrics.values()
            ) / len(
                competitor.weekly_metrics
            )

            traffic_scores[
                competitor.name
            ] = round(
                avg_traffic,
                2
            )

        if traffic_scores:

            leader = max(
                traffic_scores,
                key=traffic_scores.get
            )

            insights.append(
                f"{leader} exhibits the "
                f"highest average weekly "
                f"traffic levels."
            )

        # Recommendations

        recommendations.append(
            "Schedule promotional "
            "campaigns during "
            "competitor low-traffic "
            "windows."
        )

        recommendations.append(
            "Monitor highly reviewed "
            "competitors for pricing "
            "and assortment changes."
        )

        return InsightResult(
            key_insights=insights,
            recommendations=recommendations
        )