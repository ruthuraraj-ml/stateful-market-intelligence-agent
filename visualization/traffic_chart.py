import pandas as pd
import plotly.express as px

class TrafficChart:

    @staticmethod
    def create(competitors):
        rows = []

        for competitor in competitors:
            if not competitor.weekly_metrics:
                continue

            avg_traffic = round(
                sum(day.avg_traffic_pct for day in competitor.weekly_metrics.values())
                / len(competitor.weekly_metrics),
                2
            )

            rows.append(
                {
                    "Store": competitor.name,
                    "Average Traffic": avg_traffic,
                    "Traffic Source": getattr(competitor, "traffic_source", "UNKNOWN")
                }
            )

        df = pd.DataFrame(rows)
        
        if df.empty:
            return px.bar(title="Average Weekly Traffic Comparison (No Data Available)")

        fig = px.bar(
            df,
            x="Store",
            y="Average Traffic",
            color="Traffic Source",
            title="Average Weekly Traffic Comparison"
        )
        return fig