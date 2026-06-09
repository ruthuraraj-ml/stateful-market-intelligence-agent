from memory.memory_retriever import MemoryRetriever

class MemoryRAG:
    def __init__(self):
        """
        Initializes the Retrieval-Augmented Generation context aggregator
        by attaching your functional MemoryRetriever index tracker.
        """
        self.retriever = MemoryRetriever()

    def retrieve_context(self, query: str, top_k: int = 5) -> str:
        """
        Queries the database collection index and processes string payloads 
        into a unified context feed for LLM processing.
        """
        results = self.retriever.search(query, top_k)
        
        # Guard against uninitialized collections or empty results matrix formats
        if not results or "documents" not in results or not results["documents"]:
            return ""
            
        documents = results["documents"][0]
        
        # Flatten distinct historical matrix snapshots with clean structural breaks
        context = "\n\n--- Historical Record Snapshot ---\n".join(documents)
        return context