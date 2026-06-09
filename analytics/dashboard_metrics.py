from models.dashboard import DashboardKPIs

class DashboardMetrics:

    @staticmethod
    def generate(analytics, competitors, leaderboard):
        # Calculate overall traffic coverage
        traffic_enabled = sum(1 for c in competitors if c.weekly_metrics)
        traffic_coverage = round(
            (traffic_enabled / max(len(competitors), 1)) * 100, 2
        )

        # Calculate high-fidelity empirical source coverage
        empirical_count = sum(
            1 for c in competitors if getattr(c, "traffic_status", "") == "EMPIRICAL"
        )
        empirical_coverage = round(
            (empirical_count / max(len(competitors), 1)) * 100, 2
        )

        leader = leaderboard[0] if leaderboard else None
        leader_score = leader.competitive_score if leader else 0.0

        # Calculate competitive margin gap defensively between Rank 1 and Rank 2
        runner_up_score = (
            leaderboard[1].competitive_score
            if len(leaderboard) > 1
            else leader_score
        )
        market_gap = round(leader_score - runner_up_score, 2)

        return DashboardKPIs(
            competitor_count=analytics.competitor_count,
            average_rating=analytics.average_rating,
            traffic_coverage=traffic_coverage,
            empirical_coverage=empirical_coverage,  
            market_leader=leader.store_name if leader else "None",
            leader_score=round(leader_score, 2),
            market_gap=market_gap                  
        )