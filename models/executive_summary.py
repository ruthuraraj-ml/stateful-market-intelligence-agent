from pydantic import BaseModel, Field


class ExecutiveSummary(BaseModel):

    summary: str

    opportunities: list[str] = (
        Field(default_factory=list)
    )

    risks: list[str] = (
        Field(default_factory=list)
    )

    recommendations: list[str] = (
        Field(default_factory=list)
    )