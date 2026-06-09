# test_memory_agent.py
import sys
import os
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from memory.memory_writer import MemoryWriter
from memory.memory_qa_agent import MemoryQAAgent

# Mock layout definitions to mimic standard runtime parameters
class QuickMock:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

def run_v2_validation():
    print("⏳ Stage 1: Seeding vector space database with multi-location snapshots...")
    writer = MemoryWriter()
    
    # 1. Seed Koramangala Analytics Data Snapshot
    writer.save_analysis(
        location="Koramangala Bangalore",
        dashboard_kpis=QuickMock(market_leader="Style Union - Koramangala", market_gap=25.21, traffic_coverage=80.0),
        executive_summary=QuickMock(summary="Koramangala exhibits high competitive saturation dominated primarily by Style Union."),
        reflection=QuickMock(status="SUFFICIENT")
    )
    
    # 2. Seed Indiranagar Analytics Data Snapshot
    writer.save_analysis(
        location="Indiranagar Bangalore",
        dashboard_kpis=QuickMock(market_leader="Zudio - Indiranagar", market_gap=44.15, traffic_coverage=95.0),
        executive_summary=QuickMock(summary="Indiranagar shows massive footfall concentration but holds an expansive market gap margin."),
        reflection=QuickMock(status="SUFFICIENT")
    )
    
    print("✅ Seed steps fully synchronized.")
    print("⏳ Stage 2: Initializing Chat Agent and running analytical retrieval comparison queries...")
    
    agent = MemoryQAAgent()
    
    # Run test question comparing locations
    test_query = "Compare the market gaps between Koramangala and Indiranagar. Which location presents a larger margin?"
    print(f"\n🔍 Query to Memory Agent: '{test_query}'\n")
    
    answer = agent.ask(test_query)
    
    print("--- Memory Agent Business Reasoning Output ---")
    print(answer)
    print("----------------------------------------------")

if __name__ == "__main__":
    run_v2_validation()