import uuid
import json
from memory.chroma_manager import ChromaManager

class MemoryWriter:
    def __init__(self):
        self.manager = ChromaManager()

    def save_analysis(self, location, dashboard_kpis, executive_summary, reflection):
        # 1. Structural Text snapshot layout formulation (Step 10 Upgrade)
        document_text = f"""
==========================================
RETAIL INTELLIGENCE ANALYSIS SNAPSHOT
==========================================
Location Neighborhood: {location}
Total Tracked Competitors: {dashboard_kpis.competitor_count}
Market Average Rating Profile: {dashboard_kpis.average_rating} Stars
Traffic Telemetry Tracked Coverage: {dashboard_kpis.traffic_coverage}%
Empirical Core Data Coverage: {dashboard_kpis.empirical_coverage}%
Current Market Space Leader: {dashboard_kpis.market_leader}
Leader Benchmark Score: {dashboard_kpis.leader_score} / 100
Strategic Advantage Market Gap Margin: {dashboard_kpis.market_gap} pts
Data Stream Integrity Status: {reflection.status}

EXECUTIVE BUSINESS SUMMARY:
{executive_summary.summary}
"""

        # 2. Extract and append standalone metadata filters for advanced queries
        metadata_payload = {
            "location": str(location),
            "market_leader": str(dashboard_kpis.market_leader),
            "market_gap": float(dashboard_kpis.market_gap),
            "reflection_status": str(reflection.status)
        }

        # 3. Add directly to persistent storage collections
        self.manager.collection.add(
            ids=[str(uuid.uuid4())],
            documents=[document_text.strip()],
            metadatas=[metadata_payload]
        )