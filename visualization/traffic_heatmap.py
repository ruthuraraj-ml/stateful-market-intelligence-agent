import pandas as pd
import plotly.express as px


class TrafficHeatmap:

    DAYS = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    @staticmethod
    def create(
        competitors
    ):

        rows = []

        for competitor in competitors:

            row = {
                "Store": competitor.name
            }

            for day in (
                TrafficHeatmap.DAYS
            ):

                metric = (
                    competitor
                    .weekly_metrics
                    .get(day)
                )

                if metric:

                    row[day] = (
                        metric.avg_traffic_pct
                    )

                else:

                    row[day] = 0

            rows.append(row)

        dataframe = pd.DataFrame(
            rows
        )

        heatmap_df = (
            dataframe
            .set_index("Store")
        )

        fig = px.imshow(
            heatmap_df,

            labels={
                "x": "Day",
                "y": "Store",
                "color": "Traffic %"
            },

            title=(
                "Weekly Traffic Heatmap"
            ),

            aspect="auto",

            text_auto=True
        )

        fig.update_layout(
            height=500
        )

        return fig