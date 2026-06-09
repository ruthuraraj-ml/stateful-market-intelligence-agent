import streamlit as st
import pandas as pd
import io
import os
import json

# --- Ingestion, Adapter & Search Tools ---
from tools.competitor_search import CompetitorSearchTool
from tools.competitor_adapter import CompetitorAdapter
from tools.competitor_enrichment import CompetitorEnrichmentTool  

# --- Core Business Logic Analytics & Engines ---
from analytics.metrics import AnalyticsEngine
from analytics.competitive_scoring import CompetitiveScoringEngine
from analytics.dashboard_metrics import DashboardMetrics

from workflow.reflection import ReflectionEngine
from workflow.langgraph_workflow import competitor_agent_graph  

# --- Visualization Layout Engines ---
from visualization.competitor_table import CompetitorTableBuilder
from visualization.traffic_chart import TrafficChart
from visualization.ratings_chart import RatingsChart
from visualization.reviews_chart import ReviewsChart
from visualization.competitive_score_chart import CompetitiveScoreChart
from visualization.traffic_heatmap import TrafficHeatmap

# --- Reporting, LLM Context, & Export Engines ---
from reporting.executive_summary import ExecutiveSummaryGenerator
from reporting.recommendation_engine import RecommendationEngine
from export.pdf_exporter import PDFExporter
from export.excel_exporter import ExcelExporter

# --- Persistent Knowledge Memory Layer Engines ---
from memory.memory_writer import MemoryWriter
from memory.memory_retriever import MemoryRetriever
from memory.memory_qa_agent import MemoryQAAgent


# ==========================================
# 🎨 PAGE CONFIGURATION & HEADER
# ==========================================
st.set_page_config(
    page_title="Competitor Intelligence Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🏪 Competitor Intelligence Platform")
st.markdown(
    """
    Analyze nearby clothing store competitors, foot traffic patterns, 
    market positioning, and tactical business opportunities using live telemetry.
    """
)


# ==========================================
# 💾 STATE INITIALIZATION COMPONENT
# ==========================================
if "pipeline_data" not in st.session_state:
    st.session_state.pipeline_data = None
if "current_location" not in st.session_state:
    st.session_state.current_location = ""


# ==========================================
# 🛠️ INTERACTIVE CONFIGURATION SIDEBAR
# ==========================================
with st.sidebar:
    st.header("Analysis Configuration")
    
    location = st.text_input(
        "Target Location / Neighborhood",
        value="Koramangala Bangalore"
    )
    
    max_results = st.slider(
        "Maximum Competitors to Track",
        min_value=2,
        max_value=10,
        value=5
    )
    
    st.markdown("---")
    run_analysis = st.button("🚀 Generate Intelligence", use_container_width=True)


# ==========================================
# 🏁 PIPELINE COMPUTATION LOOP (LANGGRAPH POWERED)
# ==========================================
if run_analysis:
    with st.spinner("Invoking LangGraph StateGraph Orchestration Engine..."):
        try:
            # Execute the compiled graph with the initial state context inputs
            initial_state = {
                "location": location,
                "max_results": max_results,
                "competitors": [],
                "loop_count": 0
            }
            
            final_state = competitor_agent_graph.invoke(initial_state)
            
            # Extract computed data properties from LangGraph State mapping
            competitors = final_state["competitors"]
            leaderboard = final_state["leaderboard"]
            dashboard_kpis = final_state["dashboard_kpis"]
            reflection = final_state["reflection"]
            executive_summary = final_state["executive_summary"]
            competitor_df = final_state["competitor_df"]

            # 📋 PRE-COMPILE THE CORPORATE ARTIFACT FILE BYTES (Keep output layers out of the graph)
            pdf_filename = "competitor_report.pdf"
            excel_filename = "competitor_report.xlsx"
            
            PDFExporter.export(
                pdf_filename, 
                dashboard_kpis, 
                executive_summary, 
                competitor_df, 
                reflection,
                competitors,   
                leaderboard    
            )
            ExcelExporter.export(excel_filename, dashboard_kpis, competitor_df)
            
            with open(pdf_filename, "rb") as pdf_file:
                pdf_bytes = pdf_file.read()
                
            with open(excel_filename, "rb") as excel_file:
                excel_bytes = excel_file.read()

            # 🧠 UPGRADED V2 RICH DOCUMENT WRITER INGESTION
            try:
                memory_writer = MemoryWriter()
                memory_writer.save_analysis(
                    location=location,
                    dashboard_kpis=dashboard_kpis,
                    executive_summary=executive_summary,
                    reflection=reflection
                )
                st.sidebar.success("✅ Analysis Synced to Long-Term Memory.")
            except Exception as mem_write_err:
                st.sidebar.warning(f"Memory Sync Interrupted: {str(mem_write_err)}")

            # 🚀 COMMIT DATA INTO SESSION STATE FOR COMPONENT RETENTION
            st.session_state.pipeline_data = {
                "competitors": competitors,
                "leaderboard": leaderboard,
                "dashboard_kpis": dashboard_kpis,
                "reflection": reflection,
                "executive_summary": executive_summary,
                "competitor_df": competitor_df,
                "pdf_bytes": pdf_bytes,
                "excel_bytes": excel_bytes
            }
            st.session_state.current_location = location

        except Exception as e:
            st.error(f"LangGraph State Execution Matrix failed: {str(e)}")


# ==========================================
# 📑 THREE-TAB SYSTEM VIEW INTERFACE (V2)
# ==========================================
tab_current, tab_memory, tab_assistant = st.tabs([
    "📊 Current Location Analysis", 
    "🧠 Persistent Database Explorer",
    "🤖 Historical Memory Assistant"
])

# --- TAB 1: CURRENT RUN GRAPHICAL OVERVIEW ---
with tab_current:
    if st.session_state.pipeline_data is not None:
        data = st.session_state.pipeline_data
        competitors = data["competitors"]
        leaderboard = data["leaderboard"]
        dashboard_kpis = data["dashboard_kpis"]
        reflection = data["reflection"]
        executive_summary = data["executive_summary"]
        competitor_df = data["competitor_df"]
        
        # 🛠️ Developer Diagnostics
        with st.expander("🛠️ Developer Diagnostics"):
            for c in competitors:
                st.write({
                    "store": c.name,
                    "status": getattr(c, 'traffic_status', 'N/A'),
                    "source": getattr(c, 'traffic_source', 'N/A'),
                    "confidence": getattr(c, 'traffic_confidence', 0.0),
                    "days_mapped": len(c.weekly_metrics) if hasattr(c, 'weekly_metrics') and c.weekly_metrics else 0,
                    "busiest_days": getattr(c, 'busiest_days', [])
                })

        # Score Metric Badges Grid
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Competitors", dashboard_kpis.competitor_count)
        with col2:
            st.metric("Avg Rating", f"{dashboard_kpis.average_rating} ⭐")
        with col3:
            st.metric("Traffic Coverage", f"{dashboard_kpis.traffic_coverage}%")
        with col4:
            st.metric("Empirical Coverage", f"{dashboard_kpis.empirical_coverage}%")
        with col5:
            st.metric("Market Gap", f"{dashboard_kpis.market_gap} pts")
        
        st.markdown("---")

        st.subheader("🏪 Competitor Performance Matrix Overview")
        st.dataframe(competitor_df, use_container_width=True, hide_index=True)
        st.markdown("---")

        # Market Space Analytical Chart Visualizations
        st.subheader("📉 Market Space Analytical Chart Visualizations")
        chart_row1_col1, chart_row1_col2 = st.columns(2)
        with chart_row1_col1:
            st.plotly_chart(CompetitiveScoreChart.create(leaderboard), use_container_width=True)
        with chart_row1_col2:
            st.plotly_chart(TrafficChart.create(competitors), use_container_width=True)

        chart_row2_col1, chart_row2_col2 = st.columns(2)
        with chart_row2_col1:
            st.plotly_chart(RatingsChart.create(competitors), use_container_width=True)
        with chart_row2_col2:
            st.plotly_chart(ReviewsChart.create(competitors), use_container_width=True)

        # 🔥 RESTORED TRAFFIC HEATMAP
        st.markdown("---")
        st.subheader("🔥 Weekly Traffic Density Footfall Heatmap")
        st.plotly_chart(TrafficHeatmap.create(competitors), use_container_width=True)
        st.markdown("---")

        # Consultant Executive Briefing Narrative
        st.subheader("📋 Consultant Executive Briefing Narrative")
        st.markdown(getattr(executive_summary, "summary", ""))
        
        if getattr(executive_summary, "opportunities", None):
            st.markdown("### 🚀 Opportunities")
            for item in executive_summary.opportunities:
                st.success(item)
                
        if getattr(executive_summary, "risks", None):
            st.markdown("### ⚠️ Risks")
            for item in executive_summary.risks:
                st.warning(item)
                
        if getattr(executive_summary, "recommendations", None):
            st.markdown("### 🎯 Recommendations")
            for item in executive_summary.recommendations:
                st.info(item)
                
        st.markdown("---")

        # 🔍 RESTORED DATA REFLECTION ASSESSMENT
        st.subheader("🔍 Data Stream Integrity Assessment")
        status_flag = str(getattr(reflection, "status", "INSUFFICIENT")).upper()
        status_color = "green" if status_flag == "SUFFICIENT" else "orange"
        st.markdown(f"**Validation Status:** :{status_color}[{status_flag}]")
        st.info(f"**Verification Reason Context:** {getattr(reflection, 'reason', '')}")
        st.markdown("---")

        # Download Managers
        st.subheader("⬇️ Download Corporate Artifact Reports")
        dc1, dc2 = st.columns(2)
        dc1.download_button(
            label="⬇️ Download Presentation Grade PDF Report",
            data=data["pdf_bytes"],
            file_name="Competitor_Intelligence_Report.pdf",
            mime="application/pdf",
            use_container_width=True
        )
        dc2.download_button(
            label="⬇️ Download Structured Data Excel Sheet",
            data=data["excel_bytes"],
            file_name="Competitor_Performance_Data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
        
        st.markdown("---")
        # 🤖 RESTORED OBSERVABILITY LOG TRACE
        st.subheader("🤖 Agent Execution Observability Trace")
        agent_trace_logs = [
            {"tool": "CompetitorSearchTool", "reason": "Scanned target coordinate workspace matrices to extract local competitive hubs."},
            {"tool": "CompetitorEnrichmentTool", "reason": "Executed live telemetry lookups & synthesized data streams via TrafficInferenceEngine fallback."},
            {"tool": "AnalyticsEngine", "reason": "Compiled profile distributions, parsed out averages, and extracted market gap deltas."},
            {"tool": "ReflectionEngine", "reason": "Evaluated data coverage depth metrics against data density constraints."},
            {"tool": "ExecutiveSummaryGenerator", "reason": "Synthesized parsed analytical profiles into strategic presentation narrative objects."},
            {"tool": "MemoryWriter", "reason": "Successfully captured real-time telemetry records into long-term ChromaDB vector store."}
        ]
        for step in agent_trace_logs:
            st.markdown(f"⚙️ **Invoked System Module:** `{step['tool']}`")
            st.caption(f"*Reasoning Logic Context:* {step['reason']}")
            
    else:
        st.info("💡 Input a location on the left sidebar panel and trigger 'Generate Intelligence' to calculate parameters.")


# --- TAB 2: RAW VECTOR DB SEARCH AND INSPECTION ---
with tab_memory:
    st.subheader("🧠 ChromaDB Context Index Lookup")
    st.markdown("Extract specific vector entries directly from the long-term database collections mapping.")
    
    db_query = st.text_input("🔍 Input Raw Search Query Key:", placeholder="e.g., Koramangala, Style Union, Zudio", key="raw_db_explorer_input")
    
    if db_query:
        with st.spinner("Scanning persistent storage indices..."):
            try:
                retriever = MemoryRetriever()
                raw_matches = retriever.search(db_query, top_k=3)
                
                if raw_matches and 'documents' in raw_matches and len(raw_matches['documents'][0]) > 0:
                    for i, text_block in enumerate(raw_matches['documents'][0]):
                        meta = raw_matches['metadatas'][0][i] if 'metadatas' in raw_matches else {}
                        dist = raw_matches['distances'][0][i] if 'distances' in raw_matches else None
                        
                        with st.expander(f"📄 Match Matrix #{i+1} | Location Context: {meta.get('location', 'Unknown')} (Distance Delta: {round(dist,4) if dist is not None else 'N/A'})"):
                            try:
                                parsed_json = json.loads(text_block)
                                st.json(parsed_json)
                            except Exception:
                                st.text(text_block)
                else:
                    st.info("No matching data entries found for this tracking string.")
            except Exception as err:
                st.error(f"Search engine index failure: {str(err)}")


# --- TAB 3: THE INTUITIVE V2 GEMINI RAG QA AGENT ---
with tab_assistant:
    st.subheader("🤖 Gemini Multi-Location Intelligence Assistant")
    # ... (rest of your markdown code stays the same) ...
    
    user_prompt = st.text_input("💬 Ask Long-Term Memory Interface:", placeholder="e.g., Summarize the differences across all analyzed markets...", key="gemini_rag_qa_input")
    
    if user_prompt:
        with st.spinner("🧠 Querying database context vectors and executing Gemini analytical reasoning..."):
            try:
                qa_agent = MemoryQAAgent()
                agent_payload = qa_agent.ask(user_prompt)
                
                # 🛠️ FIX: Safely extract the raw string from the agent payload list
                if isinstance(agent_payload, list) and len(agent_payload) > 0:
                    agent_answer = agent_payload[0].get('text', str(agent_payload))
                elif isinstance(agent_payload, dict):
                    agent_answer = agent_payload.get('text', str(agent_payload))
                else:
                    agent_answer = str(agent_payload)
                
                st.markdown("### 📋 Executive Summary Consultant Evaluation")
                st.info(agent_answer)
                
            except Exception as agent_err:
                st.error(f"RAG Engine failed to process reasoning chain: {str(agent_err)}")