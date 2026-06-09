from pydantic import BaseModel



class AnalyticsResult(BaseModel):

    competitor_count: int

    average_rating: float

    average_reviews: float

    median_reviews: float

    top_rated_competitor: str

    highest_reviewed_competitor: str

    average_rank: float