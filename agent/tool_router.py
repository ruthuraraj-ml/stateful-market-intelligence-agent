from models.competitor import ToolDecision

class ToolRouter:

    @staticmethod
    def decide(state) -> ToolDecision:
        # Step A: Data Gathering Check
        if not state.competitors:
            return ToolDecision(
                thought="No competitor profiles available in the active state.",
                selected_tool="CompetitorSearchTool",
                reasoning="Geographical mapping and competitor search must execute first."
            )

        # Step B: Check for UNPROCESSED stores (instead of checking for 'FAILED' statuses)
        unprocessed_stores = [
            c for c in state.competitors 
            if c.store_id not in state.enriched_store_ids
        ]

        if unprocessed_stores:
            return ToolDecision(
                thought=f"Found {len(unprocessed_stores)} stores lacking traffic profiles.",
                selected_tool="CompetitorEnrichmentTool",
                reasoning="Execute the empirical stream or inference fallbacks for pending stores."
            )

        # Step C: Analytics Execution Check
        if state.analytics is None:
            return ToolDecision(
                thought="Competitor records enriched, but business analytics are missing.",
                selected_tool="AnalyticsEngine",
                reasoning="Calculate peak distributions and cross-competitor traffic metrics."
            )

        # Step D: Critique Check
        if state.reflection is None:
            return ToolDecision(
                thought="Analytics generation complete. Awaiting structural validation check.",
                selected_tool="ReflectionEngine",
                reasoning="Evaluate data density and coverage metrics before compile."
            )

        # Step E: Termination Condition
        return ToolDecision(
            thought="All required market intelligence completely gathered and validated.",
            selected_tool="ReportGenerator",
            reasoning="State requirements satisfied. Compiling final investor intelligence report."
        )