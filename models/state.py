from typing import Literal

from pydantic import BaseModel, Field

from models.competitor import CompetitorProfile


class ReflectionResult(BaseModel):
    status: Literal["SUFFICIENT", "INSUFFICIENT"]

    reason: str

    missing_information: list[str] = Field(default_factory=list)


class AgentState(BaseModel):
    location: str

    user_query: str

    competitors: list[CompetitorProfile] = Field(default_factory=list)

    analytics: dict = Field(default_factory=dict)

    insights: list[str] = Field(default_factory=list)

    report: str = ""

    reflection_result: ReflectionResult | None = None

    conversation_history: list[dict] = Field(default_factory=list)

    logs: list[str] = Field(default_factory=list)

    cycle: int = 0