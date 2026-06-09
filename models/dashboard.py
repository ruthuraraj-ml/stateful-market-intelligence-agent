from pydantic import BaseModel


class DashboardKPIs(BaseModel):

    competitor_count: int

    average_rating: float

    traffic_coverage: float

    empirical_coverage: float

    market_leader: str

    leader_score: float

    market_gap: float