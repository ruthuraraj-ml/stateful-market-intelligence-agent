from pydantic import BaseModel

class CompetitorScore(BaseModel):
    """
    Holds the dynamic, derived analytical positioning score 
    for a single competitor store.
    """
    store_name: str
    rating_score: float
    review_score: float
    traffic_score: float
    competitive_score: float
    market_position: int