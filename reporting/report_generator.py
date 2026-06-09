class ReportGenerator:

    @staticmethod
    def generate(
        competitors,
        analytics,
        reflection,
        insights
    ):

        report = []

        report.append(
            "# Competitor Intelligence Report\n"
        )

        report.append(
            "## Market Overview\n"
        )

        report.append(
            f"Competitors Analyzed: "
            f"{analytics.competitor_count}\n"
        )

        report.append(
            f"Average Rating: "
            f"{analytics.average_rating}\n"
        )

        report.append(
            f"Median Reviews: "
            f"{analytics.median_reviews}\n"
        )

        report.append(
            "\n## Key Insights\n"
        )

        for insight in (
            insights.key_insights
        ):

            report.append(
                f"- {insight}"
            )

        report.append(
            "\n## Recommendations\n"
        )

        for recommendation in (
            insights.recommendations
        ):

            report.append(
                f"- {recommendation}"
            )

        report.append(
            "\n## Reflection Summary\n"
        )

        report.append(
            f"Status: "
            f"{reflection.status}"
        )

        report.append(
            f"\nReason: "
            f"{reflection.reason}"
        )

        return "\n".join(report)