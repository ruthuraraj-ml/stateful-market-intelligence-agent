from models.leaderboard import CompetitorScore  
from models.competitor import CompetitorProfile

class CompetitiveScoringEngine:

    @staticmethod
    def _calculate_average_traffic(competitor: CompetitorProfile) -> float:
        if not competitor.weekly_metrics:
            return 0.0
        return sum(day.avg_traffic_pct for day in competitor.weekly_metrics.values()) / len(competitor.weekly_metrics)

    @staticmethod
    def calculate(competitors: list[CompetitorProfile]) -> list[CompetitorScore]:
        if not competitors:
            return []

        # 1. Establish Upper Bounds for Matrix Normalization
        max_rating = max([c.rating for c in competitors if c.rating is not None], default=1.0)
        max_reviews = max([c.review_count for c in competitors if c.review_count is not None], default=1.0)
        
        if max_rating == 0: max_rating = 1.0
        if max_reviews == 0: max_reviews = 1.0

        traffic_averages = {c.store_id: CompetitiveScoringEngine._calculate_average_traffic(c) for c in competitors}
        max_traffic = max(traffic_averages.values(), default=1.0)
        if max_traffic == 0: max_traffic = 1.0

        # 2. Accumulate Interim Scores as Dictionaries
        raw_scores = []
        for competitor in competitors:
            current_rating = competitor.rating or 0.0
            current_reviews = competitor.review_count or 0
            current_traffic = traffic_averages.get(competitor.store_id, 0.0)

            rating_score = round((current_rating / max_rating) * 100, 2)
            review_score = round((current_reviews / max_reviews) * 100, 2)
            traffic_score = round((current_traffic / max_traffic) * 100, 2)
            
            competitive_score = round((0.35 * rating_score) + (0.25 * review_score) + (0.40 * traffic_score), 2)

            raw_scores.append({
                "store_name": competitor.name,
                "rating_score": rating_score,
                "review_score": review_score,
                "traffic_score": traffic_score,
                "competitive_score": competitive_score
            })

        # 3. Sort Candidates by Competitive Index (Descending Order)
        raw_scores.sort(key=lambda x: x["competitive_score"], reverse=True)

        # 4. Instantiate Strongly-Typed Pydantic Models with numerical ranks
        final_scores = []
        for rank, entry in enumerate(raw_scores, 1):
            final_scores.append(
                CompetitorScore(
                    store_name=entry["store_name"],
                    rating_score=entry["rating_score"],
                    review_score=entry["review_score"],
                    traffic_score=entry["traffic_score"],
                    competitive_score=entry["competitive_score"],
                    market_position=rank  # ✅ Maps to your integer schema definition flawlessly
                )
            )

        return final_scores