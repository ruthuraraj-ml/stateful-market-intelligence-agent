class RecommendationEngine:

    @staticmethod
    def generate(
        dashboard_kpis,
        reflection
    ):

        recommendations = []

        if (
            dashboard_kpis.market_gap
            > 15
        ):
            recommendations.append(
                "A dominant market leader exists. "
                "Differentiation strategies "
                "should be prioritized."
            )

        if (
            dashboard_kpis.empirical_coverage
            >= 80
        ):
            recommendations.append(
                "Traffic intelligence coverage "
                "is highly reliable."
            )

        if (
            reflection.status
            == "SUFFICIENT"
        ):
            recommendations.append(
                "Current dataset is sufficient "
                "for competitive analysis."
            )

        return recommendations