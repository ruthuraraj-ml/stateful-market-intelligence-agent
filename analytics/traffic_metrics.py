from models.competitor import CompetitorProfile

class TrafficAnalytics:

    @staticmethod
    def average_weekly_traffic(competitor: CompetitorProfile) -> float:
        if not competitor.weekly_metrics:
            return 0.0
        values = [day.avg_traffic_pct for day in competitor.weekly_metrics.values()]
        return round(sum(values) / len(values), 2)
    
    @staticmethod
    def highest_traffic_competitor(competitors: list[CompetitorProfile]) -> CompetitorProfile:
        return max(competitors, key=TrafficAnalytics.average_weekly_traffic)
    
    @staticmethod
    def highest_peak_competitor(competitors: list[CompetitorProfile]) -> CompetitorProfile:
        def get_max_peak(c: CompetitorProfile):
            if not c.weekly_metrics:
                return 0
            return max(day.peak_traffic_pct for day in c.weekly_metrics.values())
            
        return max(competitors, key=get_max_peak)