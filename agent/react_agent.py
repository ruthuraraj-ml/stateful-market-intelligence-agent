from agent.tool_router import ToolRouter

from reporting.insight_generator import (
    InsightGenerator
)

from reporting.report_generator import (
    ReportGenerator
)

class ReActAgent:

    def __init__(self, search_tool, enrichment_tool, analytics_engine, reflection_engine):
        self.search_tool = search_tool
        self.enrichment_tool = enrichment_tool
        self.analytics_engine = analytics_engine
        self.reflection_engine = reflection_engine

    def run(self, state):
        while True:
            decision = ToolRouter.decide(state)
            state.decisions.append(decision)

            print(f"\n🧠 [THOUGHT] {decision.thought}")
            print(f"🎬 [ACTION]  Invoking -> {decision.selected_tool}")

            if decision.selected_tool == "CompetitorSearchTool":
                # Simulated or real adapter extraction
                raw_results = self.search_tool.search_competitors(state.location)
                
                # Using your Adapter Pattern
                from tools.competitor_adapter import CompetitorAdapter
                state.competitors = [CompetitorAdapter.from_apify(r) for r in raw_results]

            elif decision.selected_tool == "CompetitorEnrichmentTool":
                # Mutate profiles through the dual-layer pipeline
                state.competitors = [self.enrichment_tool.enrich(c) for c in state.competitors]
                
                # 💾 RECORD EXECUTION: Save progress to the state model
                state.enriched_store_ids = [c.store_id for c in state.competitors]

            elif decision.selected_tool == "AnalyticsEngine":
                state.analytics = self.analytics_engine.generate(state.competitors)

            elif decision.selected_tool == "ReflectionEngine":
                state.reflection = self.reflection_engine.evaluate(state.competitors)

            elif decision.selected_tool == "ReportGenerator":
                print("\n🏁 [TERMINATION] Compiling final report assets...")
                
                insights = (
                    InsightGenerator.generate(
                    state.competitors,
                    state.analytics
                    )
                )

                state.final_report = (
                    ReportGenerator.generate(
                        state.competitors,
                        state.analytics,
                        state.reflection,
                        insights
                    )
                )

                break

            state.cycle += 1
            if state.cycle > 10:
                print("⚠️ [EMERGENCY BRAKE] Maximum ReAct execution cycles exceeded.")
                break

        return state