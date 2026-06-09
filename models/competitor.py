from typing import Optional
from pydantic import BaseModel, Field

class TrafficMetrics(BaseModel):
    """
    Represents normalized traffic percentages for a specific day.
    """
    avg_traffic_pct: int
    peak_traffic_pct: int

class CompetitorProfile(BaseModel):
    """
    Represents a nearby competitor clothing store.
    """
    store_id: str
    name: str
    address: str
    rating: Optional[float] = None
    review_count: Optional[int] = None
    distance_meters: float
    peak_hours: list[str] = Field(default_factory=list)
    footfall_score: Optional[float] = None
    footfall_level: Optional[str] = None
    confidence_score: float = 0.0
    source: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    business_status: Optional[str] = None
    website: Optional[str] = None
    phone: Optional[str] = None
    opening_hours: list[dict] = Field(default_factory=list)
    categories: list[str] = Field(default_factory=list)
    rank: Optional[int] = None
    place_id: Optional[str] = None
    popular_times: dict = Field(default_factory=dict)
    weekly_metrics: dict[str, TrafficMetrics] = Field(default_factory=dict)
    busiest_days: list[str] = Field(default_factory=list)
    traffic_source: Optional[str] = None      # "BESTTIME_EMPIRICAL" or "ANALYTICAL_INFERENCE"
    traffic_status: str = "FAILED"            # "EMPIRICAL", "INFERRED", or "FAILED"
    traffic_confidence: Optional[float] = 0.0


class ToolDecision(BaseModel):
    """
    Observability model for ReAct tool routing.
    Captured to cleanly display the agent's internal thoughts in the UI.
    """
    thought: str
    selected_tool: str
    reasoning: str