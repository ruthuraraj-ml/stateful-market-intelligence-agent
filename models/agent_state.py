from pydantic import BaseModel, Field
from typing import Optional, Set
from models.competitor import CompetitorProfile, ToolDecision

# Placeholder schemas for your downstream modules to prevent compilation errors
class AnalyticsResult(BaseModel):
    metrics_generated: bool = True
    summary: dict = Field(default_factory=dict)

class ReflectionResult(BaseModel):
    is_sufficient: bool = True
    coverage_score: float = 1.0

class AgentState(BaseModel):
    user_query: str
    location: str
    competitors: list[CompetitorProfile] = Field(default_factory=list)
    analytics: Optional[AnalyticsResult] = None
    reflection: Optional[ReflectionResult] = None
    decisions: list[ToolDecision] = Field(default_factory=list)
    final_report: str = ""
    cycle: int = 0
    # 🛡️ Track processed items to prevent infinite routing loops
    enriched_store_ids: list[str] = Field(default_factory=list)