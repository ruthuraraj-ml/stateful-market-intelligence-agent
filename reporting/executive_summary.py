import json
from langchain_google_genai import ChatGoogleGenerativeAI
from models.executive_summary import ExecutiveSummary
from config.settings import settings


class ExecutiveSummaryGenerator:

    def __init__(self):
        """
        Initializes the executive summary engine using the optimized
        Gemini flash framework context.
        """
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-3.1-flash-lite",
            google_api_key=settings.GEMINI_API_KEY,
            temperature=0.2
        )

    def generate(
        self,
        location,
        dashboard_kpis,
        leaderboard,
        reflection,
        recommendations
    ):
        """
        Compiles the real-time calculated business metrics into a professional
        retail intelligence narrative payload.
        ```
        """
        prompt = f"""
You are a retail market intelligence consultant.

Use ONLY the supplied analytics.

Return ONLY valid JSON matching the exact schema below. Do not wrap code block structures inside the text description fields.

Schema:
{{
    "summary": "...",
    "opportunities": [
        "...",
        "..."
    ],
    "risks": [
        "...",
        "..."
    ],
    "recommendations": [
        "...",
        "..."
    ]
}}

Location:
{location}

Competitors:
{dashboard_kpis.competitor_count}

Average Rating:
{dashboard_kpis.average_rating}

Traffic Coverage:
{dashboard_kpis.traffic_coverage}

Empirical Coverage:
{dashboard_kpis.empirical_coverage}

Market Leader:
{dashboard_kpis.market_leader}

Leader Score:
{dashboard_kpis.leader_score}

Market Gap:
{dashboard_kpis.market_gap}

Reflection Status:
{reflection.status}

Recommendations:
{recommendations}
"""
        response = self.llm.invoke(prompt)
        content_payload = response.content
        
        if isinstance(content_payload, list):
            clean_summary = ""
            for block in content_payload:
                if isinstance(block, dict) and "text" in block:
                    clean_summary += block["text"]
                elif isinstance(block, str):
                    clean_summary += block
        else:
            clean_summary = str(content_payload)

        # 🚀 FIX: Strip Markdown Code Fences (```json ... ```)
        text_clean = clean_summary.strip()
        if text_clean.startswith("```"):
            if text_clean.startswith("```json"):
                text_clean = text_clean[7:]
            else:
                text_clean = text_clean[3:]
            if text_clean.endswith("```"):
                text_clean = text_clean[:-3]
        text_clean = text_clean.strip()

        try:
            parsed = json.loads(text_clean)
            return ExecutiveSummary(
                summary=parsed.get("summary", ""),
                opportunities=parsed.get("opportunities", []),
                risks=parsed.get("risks", []),
                recommendations=parsed.get("recommendations", [])
            )
        except Exception:
            # Fallback if JSON generation corrupted structural keys completely
            return ExecutiveSummary(
                summary=clean_summary,
                opportunities=[],
                risks=[],
                recommendations=[]
            )