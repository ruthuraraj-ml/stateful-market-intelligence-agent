from pydantic import BaseModel, Field


class InsightResult(BaseModel):

    key_insights: list[str] = Field(
        default_factory=list
    )

    recommendations: list[str] = Field(
        default_factory=list
    )