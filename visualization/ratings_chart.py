import pandas as pd
import plotly.express as px

class RatingsChart:

    @staticmethod
    def create(competitors):
        df = pd.DataFrame(
            [
                {
                    "Store": c.name,
                    "Rating": c.rating if c.rating is not None else 0.0
                }
                for c in competitors
            ]
        )
        
        if df.empty:
            return px.bar(title="Competitor Rating Comparison (No Data Available)")

        return px.bar(
            df,
            x="Store",
            y="Rating",
            title="Competitor Rating Comparison"
        )