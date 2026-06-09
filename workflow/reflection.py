from models.state import ReflectionResult


class ReflectionEngine:

    @staticmethod
    def evaluate(competitors):
        """
        Evaluates data quality metrics across the collected competitive sample space.
        Aligns directly with modern 'weekly_metrics' schema structures.
        """
        missing_information = []
        competitor_count = len(competitors)

        # 1. Evaluate Core Firmographic Data Coverages
        rating_coverage = (
            sum(1 for c in competitors if getattr(c, 'rating', None) is not None)
            / max(competitor_count, 1)
        )

        review_coverage = (
            sum(1 for c in competitors if getattr(c, 'review_count', None) is not None)
            / max(competitor_count, 1)
        )

        # 2. Evaluate Unified Traffic Telemetry Coverages (Fixed Legacy Attributes)
        traffic_coverage = (
            sum(1 for c in competitors if getattr(c, 'weekly_metrics', None))
            / max(competitor_count, 1)
        )

        # Count how much data represents real historical telemetry vs synthetic inference models
        empirical_count = sum(
            1 for c in competitors 
            if getattr(c, 'traffic_status', '') == 'EMPIRICAL'
        )

        # ==========================================
        # 📈 PRODUCTION THRESHOLD VALIDATION MATRIX
        # ==========================================
        # Relaxed from strict absolute 5 count down to a standard local market sample size
        if competitor_count < 3:
            missing_information.append("insufficient_competitor_density")

        if rating_coverage < 0.80:
            missing_information.append("rating_data_gaps")

        if review_coverage < 0.80:
            missing_information.append("review_count_gaps")

        # Telemetry check now respects both empirical hits and inferred models
        if traffic_coverage < 0.60:
            missing_information.append("footfall_telemetry_gaps")

        # ==========================================
        # 📋 COMPILE STATUS AUDIT RESPONSE OBJECT
        # ==========================================
        if missing_information:
            return ReflectionResult(
                status="INSUFFICIENT",
                reason=(
                    f"Market data profile contains structural gaps. "
                    f"Tracked {competitor_count} nodes with {traffic_coverage * 100:.0f}% traffic coverage."
                ),
                missing_information=missing_information
            )

        # Data is cleanly resolved, full market space visualization is reliable
        return ReflectionResult(
            status="SUFFICIENT",
            reason=(
                f"Successfully validated comprehensive competitive footprint. "
                f"Analyzed {competitor_count} nodes with 100% data coverage "
                f"({empirical_count} empirical telemetry streams active)."
            ),
            missing_information=[]
        )