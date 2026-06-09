from models.competitor import TrafficMetrics

class TrafficInferenceEngine:

    @staticmethod
    def infer(review_count: int) -> dict[str, TrafficMetrics]:
        if review_count < 200:
            scale = 0.40
        elif review_count < 1000:
            scale = 0.60
        elif review_count < 5000:
            scale = 0.80
        else:
            scale = 1.00

        weekday_avg = int(35 * scale)
        weekday_peak = int(70 * scale)
        weekend_avg = int(50 * scale)
        weekend_peak = int(90 * scale)

        # Strictly Title-Cased keys populated into formal Pydantic schemas
        return {
            "Monday": TrafficMetrics(avg_traffic_pct=weekday_avg, peak_traffic_pct=weekday_peak),
            "Tuesday": TrafficMetrics(avg_traffic_pct=weekday_avg, peak_traffic_pct=weekday_peak),
            "Wednesday": TrafficMetrics(avg_traffic_pct=weekday_avg, peak_traffic_pct=weekday_peak),
            "Thursday": TrafficMetrics(avg_traffic_pct=weekday_avg, peak_traffic_pct=weekday_peak),
            "Friday": TrafficMetrics(avg_traffic_pct=weekday_avg + 10, peak_traffic_pct=weekday_peak + 10),
            "Saturday": TrafficMetrics(avg_traffic_pct=weekend_avg, peak_traffic_pct=weekend_peak),
            "Sunday": TrafficMetrics(avg_traffic_pct=weekend_avg, peak_traffic_pct=weekend_peak)
        }