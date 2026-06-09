from models.competitor import CompetitorProfile, TrafficMetrics
from tools.footfall_enrichment import FootfallEnrichmentTool
from analytics.traffic_inference import TrafficInferenceEngine

class CompetitorEnrichmentTool:

    def __init__(self):
        self.footfall_tool = FootfallEnrichmentTool()

    def enrich(self, competitor: CompetitorProfile) -> CompetitorProfile:
        # Business logic strictly interacts with Pydantic properties
        raw_data = self.footfall_tool.get_footfall_analytics(competitor.name, competitor.address)

        if raw_data.get("status") == "SUCCESS":
            raw_metrics = raw_data.get("weekly_metrics", {})
            
            # Normalize and cast external JSON map into our TrafficMetrics model map
            competitor.weekly_metrics = {
                day.capitalize(): TrafficMetrics(
                    avg_traffic_pct=metrics.get("avg_traffic_pct", 0),
                    peak_traffic_pct=metrics.get("peak_traffic_pct", 0)
                )
                for day, metrics in raw_metrics.items()
            }
            competitor.busiest_days = [day.capitalize() for day in raw_data.get("busiest_days", [])]
            competitor.traffic_source = "BESTTIME_EMPIRICAL"
            competitor.traffic_status = "EMPIRICAL"
            competitor.traffic_confidence = 0.95
        else:
            # Fallback cleanly to local Analytical Inference
            competitor.weekly_metrics = TrafficInferenceEngine.infer(competitor.review_count)
            competitor.busiest_days = ["Saturday", "Sunday"]
            competitor.traffic_source = "ANALYTICAL_INFERENCE"
            competitor.traffic_status = "INFERRED"
            competitor.traffic_confidence = 0.60

        return competitor