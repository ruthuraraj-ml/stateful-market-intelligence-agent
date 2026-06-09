import pandas as pd
from openpyxl import Workbook

class ExcelExporter:

    @staticmethod
    def export(filepath: str, dashboard_kpis, competitor_dataframe: pd.DataFrame):
        """
        Generates a multi-sheet formatted business workbook mapping high-level KPIs 
        and clean structural performance tables.
        """
        wb = Workbook()
        
        # --- Sheet 1: Executive KPI Summary Dashboard ---
        summary_sheet = wb.active
        summary_sheet.title = "Executive Summary"
        
        summary_sheet.append(["Metric", "Value"])
        summary_sheet.append(["Competitor Count", dashboard_kpis.competitor_count])
        summary_sheet.append(["Average Rating", dashboard_kpis.average_rating])
        summary_sheet.append(["Traffic Coverage (%)", dashboard_kpis.traffic_coverage])
        summary_sheet.append(["Empirical Coverage (%)", dashboard_kpis.empirical_coverage])
        summary_sheet.append(["Market Leader", dashboard_kpis.market_leader])
        summary_sheet.append(["Leader Index Score", dashboard_kpis.leader_score])
        summary_sheet.append(["Market Gap Margin", dashboard_kpis.market_gap])
        
        # --- Sheet 2: Structured Competitor Data Table ---
        competitor_sheet = wb.create_sheet(title="Competitors")
        
        # Ingest dataframe header names safely
        competitor_sheet.append(list(competitor_dataframe.columns))
        
        # Dump cell contents iteratively
        for row in competitor_dataframe.itertuples(index=False):
            competitor_sheet.append(list(row))
            
        # Save active file buffer to disk
        wb.save(filepath)