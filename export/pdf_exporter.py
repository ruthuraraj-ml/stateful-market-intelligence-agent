import io
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Import all chart modules from the platform ecosystem
from visualization.traffic_chart import TrafficChart
from visualization.competitive_score_chart import CompetitiveScoreChart
from visualization.ratings_chart import RatingsChart
from visualization.reviews_chart import ReviewsChart
from visualization.traffic_heatmap import TrafficHeatmap

class PDFExporter:

    @staticmethod
    def export(filepath: str, dashboard_kpis, executive_summary, competitor_dataframe: pd.DataFrame, reflection, competitors, leaderboard):
        """
        Compiles calculated analytical models, text narratives, all 5 Plotly graphs,
        and the structured competitor data matrix into a presentation-grade report.
        """
        # Initialize canvas template setup
        doc = SimpleDocTemplate(
            filepath,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40
        )
        
        styles = getSampleStyleSheet()
        elements = []
        
        # Corporate Identity Styling Parameters
        title_style = ParagraphStyle(
            'DocTitle', parent=styles['Title'], fontSize=24, leading=28,
            textColor=colors.HexColor("#1A365D"), alignment=0, spaceAfter=15
        )
        h1_style = ParagraphStyle(
            'SectionH1', parent=styles['Heading1'], fontSize=15, leading=19,
            textColor=colors.HexColor("#1A365D"), spaceBefore=14, spaceAfter=8, keepWithNext=True
        )
        h2_style = ParagraphStyle(
            'SectionH2', parent=styles['Heading2'], fontSize=12, leading=16,
            textColor=colors.HexColor("#2B6CB0"), spaceBefore=10, spaceAfter=6, keepWithNext=True
        )
        body_style = ParagraphStyle(
            'DocBody', parent=styles['BodyText'], fontSize=10, leading=14,
            textColor=colors.HexColor("#2D3748"), spaceAfter=10
        )
        bullet_style = ParagraphStyle(
            'DocBullet', parent=styles['Normal'], fontSize=9.5, leading=14,
            textColor=colors.HexColor("#2D3748"), leftIndent=15, spaceAfter=4
        )
        table_header_style = ParagraphStyle(
            'TableHeader', parent=styles['Normal'], fontSize=9, leading=11,
            textColor=colors.white, alignment=1
        )
        table_body_style = ParagraphStyle(
            'TableBody', parent=styles['Normal'], fontSize=8, leading=11,
            textColor=colors.HexColor("#2D3748"), alignment=0
        )

        # --- 1. Document Title ---
        elements.append(Paragraph("Competitor Intelligence & Market Positioning Report", title_style))
        elements.append(Spacer(1, 10))
        
        # --- 2. Executive Summary Narrative & Strategic Briefings ---
        elements.append(Paragraph("1. Executive Summary & Market Context", h1_style))
        clean_text = executive_summary.summary.replace("\n", "<br/>")
        elements.append(Paragraph(clean_text, body_style))
        elements.append(Spacer(1, 5))
        
        # Inject Opportunities Breakdown
        if getattr(executive_summary, "opportunities", None):
            elements.append(Paragraph("Market Opportunities", h2_style))
            for opp in executive_summary.opportunities:
                elements.append(Paragraph(f"<b>🚀 Opportunity:</b> {opp}", bullet_style))
            elements.append(Spacer(1, 5))
            
        # Inject Risks Breakdown
        if getattr(executive_summary, "risks", None):
            elements.append(Paragraph("Threat Vectors & Vulnerabilities", h2_style))
            for risk in executive_summary.risks:
                elements.append(Paragraph(f"<b>⚠️ Risk Matrix:</b> {risk}", bullet_style))
            elements.append(Spacer(1, 5))
            
        # Inject Recommendations Breakdown
        if getattr(executive_summary, "recommendations", None):
            elements.append(Paragraph("Strategic Action Directives", h2_style))
            for rec in executive_summary.recommendations:
                elements.append(Paragraph(f"<b>🎯 Action Plan:</b> {rec}", bullet_style))
                
        elements.append(PageBreak()) # Force visual assets onto a fresh sheet
        
        # --- 3. Operational Analytics Graph Visualizations ---
        elements.append(Paragraph("2. Market Intelligence Visualizations", h1_style))
        
        try:
            # 🚀 GENERATE ALL 5 HIGH-FIDELITY LIVE GRAPH IMAGES IN-MEMORY
            fig_score = CompetitiveScoreChart.create(leaderboard)
            fig_traffic = TrafficChart.create(competitors)
            fig_ratings = RatingsChart.create(competitors)
            fig_reviews = ReviewsChart.create(competitors)
            fig_heatmap = TrafficHeatmap.create(competitors)
            
            # Pack Plotly visualization structures into clean PNG byte buffers
            img_bytes_score = fig_score.to_image(format="png", width=550, height=250)
            img_bytes_traffic = fig_traffic.to_image(format="png", width=550, height=250)
            img_bytes_ratings = fig_ratings.to_image(format="png", width=550, height=250)
            img_bytes_reviews = fig_reviews.to_image(format="png", width=550, height=250)
            img_bytes_heatmap = fig_heatmap.to_image(format="png", width=550, height=250)
            
            # Map buffers into flowable elements
            elements.append(Paragraph("Competitive Score Index Placement Matrix", h2_style))
            elements.append(Image(io.BytesIO(img_bytes_score), width=460, height=210))
            elements.append(Spacer(1, 15))
            
            elements.append(Paragraph("Weekly Traffic Profile Waves", h2_style))
            elements.append(Image(io.BytesIO(img_bytes_traffic), width=460, height=210))
            elements.append(PageBreak())
            
            elements.append(Paragraph("Market Profile Sentiment Distributions", h2_style))
            elements.append(Image(io.BytesIO(img_bytes_ratings), width=460, height=210))
            elements.append(Spacer(1, 15))
            
            elements.append(Paragraph("Relative Consumer Engagement Volume Matrix", h2_style))
            elements.append(Image(io.BytesIO(img_bytes_reviews), width=460, height=210))
            elements.append(PageBreak())
            
            elements.append(Paragraph("Hourly Footfall Density Telemetry Heatmap", h2_style))
            elements.append(Image(io.BytesIO(img_bytes_heatmap), width=460, height=210))
            elements.append(Spacer(1, 15))
            
        except Exception as chart_err:
            elements.append(Paragraph(f"<i>Visual Charts Missing: {str(chart_err)}</i>", body_style))
            elements.append(Spacer(1, 10))
        
        # --- 4. Strategic KPI Summary Grid Matrix ---
        elements.append(Paragraph("3. Executive Dashboard Performance Matrix", h1_style))
        kpi_table_data = [
            [Paragraph("<b>Performance Intelligence Key Metric</b>", body_style), Paragraph("<b>Analytics Value</b>", body_style)],
            [Paragraph("Competitor Density Count", body_style), Paragraph(str(dashboard_kpis.competitor_count), body_style)],
            [Paragraph("Market Average Rating Profile", body_style), Paragraph(f"{dashboard_kpis.average_rating} Stars", body_style)],
            [Paragraph("Traffic Telemetry Tracked Coverage", body_style), Paragraph(f"{dashboard_kpis.traffic_coverage}%", body_style)],
            [Paragraph("Empirical Core Data Coverage", body_style), Paragraph(f"{dashboard_kpis.empirical_coverage}%", body_style)],
            [Paragraph("Current Market Space Leader", body_style), Paragraph(str(dashboard_kpis.market_leader), body_style)],
            [Paragraph("Leader Benchmark Score", body_style), Paragraph(f"{dashboard_kpis.leader_score} / 100", body_style)],
            [Paragraph("Strategic Advantage Market Gap Margin", body_style), Paragraph(f"{dashboard_kpis.market_gap} pts", body_style)],
        ]
        
        kpi_table = Table(kpi_table_data, colWidths=[260, 260])
        kpi_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (1,0), colors.HexColor("#EDF2F7")),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ]))
        elements.append(kpi_table)
        elements.append(Spacer(1, 15))
        
        # --- 5. Granular Competitor Data Grid Matrix (The Missing Feature) ---
        elements.append(Paragraph("4. Granular Competitor Data Grid Matrix", h1_style))
        
        matrix_table_data = []
        # Header Row Injection
        header_cells = [Paragraph(f"<b>{col}</b>", table_header_style) for col in competitor_dataframe.columns]
        matrix_table_data.append(header_cells)
        
        # Content Rows Injection
        for _, row in competitor_dataframe.iterrows():
            matrix_table_data.append([Paragraph(str(val), table_body_style) for val in row])
            
        num_cols = len(competitor_dataframe.columns)
        total_width = 520
        col_width = total_width / max(num_cols, 1)
        
        matrix_table = Table(matrix_table_data, colWidths=[col_width] * num_cols)
        matrix_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1A365D")),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F7FAFC")]),
        ]))
        elements.append(matrix_table)
        elements.append(Spacer(1, 15))
        
        # --- 6. Data Quality Compliance Reflection ---
        elements.append(Paragraph("5. Data Quality Assurance Assessment", h1_style))
        status_text = f"<b>Data Stream Integrity Status:</b> {reflection.status}<br/><b>Validation Reason Context:</b> {reflection.reason}"
        elements.append(Paragraph(status_text, body_style))
        
        # Process and compile all flowable page builders sequentially
        doc.build(elements)