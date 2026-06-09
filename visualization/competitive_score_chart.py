import pandas as pd
import plotly.express as px

class CompetitiveScoreChart:

    @staticmethod
    def create(leaderboard):
        df = pd.DataFrame(
            [
                {
                    "Store": item.store_name,
                    "Competitive Score": round(item.competitive_score, 2)
                }
                for item in leaderboard
            ]
        )
        
        if df.empty:
            return px.bar(title="Competitive Intensity Ranking (No Data Available)")

        return px.bar(
            df,
            x="Store",
            y="Competitive Score",
            title="Competitive Intensity Ranking"
        )