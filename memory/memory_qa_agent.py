# memory/memory_qa_agent.py
from langchain_google_genai import ChatGoogleGenerativeAI
from config.settings import settings
from memory.memory_rag import MemoryRAG

class MemoryQAAgent:
    def __init__(self):
        """
        Initializes the context reasoning engine using the Google Gemini 
        Flash framework model.
        """
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-3.1-flash-lite",
            google_api_key=settings.GEMINI_API_KEY,
            temperature=0.2
        )
        self.rag = MemoryRAG()

    def ask(self, question: str) -> str:
        """
        Ingests real-time analytics questions, retrieves relevant data matches 
        from memory, and prompts Gemini to compile a business analysis response.
        """
        context = self.rag.retrieve_context(question, top_k=5)
        
        if not context.strip():
            return "❌ No historical retail intelligence analyses are found in the persistent vector storage memory database."

        prompt = f"""
You are a senior competitor market intelligence consultant.

Analyze the historical data provided below and answer the user's question.

CRITICAL INSTRUCTIONS:
1. Base your answer ONLY on the supplied historical analysis records inside the MEMORY block.
2. Do not assume, extrapolate, or look for external real-world values outside the records.
3. If the answer cannot be confidently deduced using only the records, state explicitly: "I cannot find the answer within the current historical analysis records."
4. Provide a clear, metrics-driven business answer with proper formatting.

--- START PERSISTENT MEMORY RECORDS ---
{context}
--- END PERSISTENT MEMORY RECORDS ---

USER QUESTION: 
{question}

EXECUTIVE BUSINESS RESPONSE:
"""
        response = self.llm.invoke(prompt)
        return response.content