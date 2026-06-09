from typing import TypedDict, List, Any, Dict
from langgraph.graph import StateGraph, END

# --- Import your existing engine components ---
from tools.competitor_search import CompetitorSearchTool
from tools.competitor_adapter import CompetitorAdapter
from tools.competitor_enrichment import CompetitorEnrichmentTool  
from analytics.metrics import AnalyticsEngine
from analytics.competitive_scoring import CompetitiveScoringEngine
from analytics.dashboard_metrics import DashboardMetrics
from workflow.reflection import ReflectionEngine  
from reporting.executive_summary import ExecutiveSummaryGenerator
from reporting.recommendation_engine import RecommendationEngine
from visualization.competitor_table import CompetitorTableBuilder

# 1. Define the Shared State
class AgentState(TypedDict):
    location: str
    max_results: int
    competitors: List[Any]
    leaderboard: List[Any]
    analytics: Any
    dashboard_kpis: Any
    reflection: Any
    recommendations: Any
    executive_summary: Any
    competitor_df: Any
    loop_count: int  # Prevent infinite routing loops

# 2. Define Node Functions
def search_node(state: AgentState) -> Dict[str, Any]:
    search_tool = CompetitorSearchTool()
    raw_results = search_tool.search_competitors(state["location"], state["max_results"])
    
    competitors = [
        CompetitorAdapter.from_apify(result)
        for result in raw_results
    ]
    return {"competitors": competitors, "loop_count": state.get("loop_count", 0) + 1}

def enrichment_node(state: AgentState) -> Dict[str, Any]:
    enrichment_tool = CompetitorEnrichmentTool()
    enriched_competitors = [
        enrichment_tool.enrich(c)
        for c in state["competitors"]
    ]
    return {"competitors": enriched_competitors}

def analytics_node(state: AgentState) -> Dict[str, Any]:
    analytics = AnalyticsEngine.generate(state["competitors"])
    leaderboard = CompetitiveScoringEngine.calculate(state["competitors"])
    dashboard_kpis = DashboardMetrics.generate(analytics, state["competitors"], leaderboard)
    competitor_df = CompetitorTableBuilder.build(state["competitors"], leaderboard)
    
    return {
        "analytics": analytics,
        "leaderboard": leaderboard,
        "dashboard_kpis": dashboard_kpis,
        "competitor_df": competitor_df
    }

def reflection_node(state: AgentState) -> Dict[str, Any]:
    reflection = ReflectionEngine.evaluate(state["competitors"])
    return {"reflection": reflection}

def summary_node(state: AgentState) -> Dict[str, Any]:
    recommendations = RecommendationEngine.generate(state["dashboard_kpis"], state["reflection"])
    generator = ExecutiveSummaryGenerator()
    executive_summary = generator.generate(
        location=state["location"],
        dashboard_kpis=state["dashboard_kpis"],
        leaderboard=state["leaderboard"],
        reflection=state["reflection"],
        recommendations=recommendations
    )
    return {
        "recommendations": recommendations,
        "executive_summary": executive_summary
    }

# 3. Define Conditional Edge Routing Logic
def route_after_reflection(state: AgentState) -> str:
    status = str(getattr(state["reflection"], "status", "INSUFFICIENT")).upper()
    
    # If data is insufficient and we haven't looped more than twice, retry search
    if status == "INSUFFICIENT" and state.get("loop_count", 0) < 2:
        return "search"
    
    # Otherwise proceed to complete the summary block
    return "summary"

# 4. Compile the Graph
workflow = StateGraph(AgentState)

# Add Nodes
workflow.add_node("search", search_node)
workflow.add_node("enrichment", enrichment_node)
workflow.add_node("analytics", analytics_node)
workflow.add_node("reflection", reflection_node)
workflow.add_node("summary", summary_node)

# Map Edges
workflow.set_entry_point("search")
workflow.add_edge("search", "enrichment")
workflow.add_edge("enrichment", "analytics")
workflow.add_edge("analytics", "reflection")

# Add Conditional Loop Routing
workflow.add_conditional_edges(
    "reflection",
    route_after_reflection,
    {
        "search": "search",
        "summary": "summary"
    }
)

workflow.add_edge("summary", END)

# This compiled object is what your Streamlit app will execute
competitor_agent_graph = workflow.compile()