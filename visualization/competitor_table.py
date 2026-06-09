import pandas as pd


class CompetitorTableBuilder:

    @staticmethod
    def build(
        competitors,
        leaderboard
    ):
        """
        Creates a dashboard-ready competitor overview table.

        Parameters
        ----------
        competitors : list[CompetitorProfile]

        leaderboard : list[CompetitorScore]

        Returns
        -------
        pandas.DataFrame
        """

        leaderboard_lookup = {
            item.store_name: item
            for item in leaderboard
        }

        rows = []

        for competitor in competitors:

            score = leaderboard_lookup.get(
                competitor.name
            )

            rows.append(
                {
                    "Rank": (
                        score.market_position
                        if score
                        else None
                    ),

                    "Store": competitor.name,

                    "Rating": (
                        round(
                            competitor.rating,
                            2
                        )
                        if competitor.rating
                        else None
                    ),

                    "Reviews": (
                        competitor.review_count
                    ),

                    "Traffic Source": (
                        competitor.traffic_source
                    ),

                    "Traffic Status": (
                        competitor.traffic_status
                    ),

                    "Traffic Confidence": (
                        round(
                            competitor.traffic_confidence,
                            2
                        )
                        if competitor.traffic_confidence
                        else 0.0
                    ),

                    "Competitive Score": (
                        round(
                            score.competitive_score,
                            2
                        )
                        if score
                        else 0.0
                    ),

                    "Busiest Days": (
                        ", ".join(
                            competitor.busiest_days
                        )
                        if competitor.busiest_days
                        else "-"
                    )
                }
            )

        dataframe = pd.DataFrame(
            rows
        )

        dataframe = dataframe.sort_values(
            by="Rank",
            ascending=True
        )

        return dataframe