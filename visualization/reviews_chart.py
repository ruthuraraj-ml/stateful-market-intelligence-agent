import pandas as pd
import plotly.express as px

class ReviewsChart:

    @staticmethod
    def create(competitors):
        df = pd.DataFrame(
            [
                {
                    "Store": c.name,
                    "Reviews": c.review_count if c.review_count is not None else 0
                }
                for c in competitors
            ]
        )
        
        if df.empty:
            return px.bar(title="Review Volume Comparison (No Data Available)")

        return px.bar(
            df,
            x="Store",
            y="Reviews",
            title="Review Volume Comparison"
        )