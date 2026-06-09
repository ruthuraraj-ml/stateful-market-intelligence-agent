from memory.chroma_manager import (
    ChromaManager
)


class MemoryRetriever:

    def __init__(self):

        self.manager = (
            ChromaManager()
        )

    def search(
        self,
        query,
        top_k=5
    ):

        results = (
            self.manager.collection.query(
                query_texts=[query],
                n_results=top_k
            )
        )

        return results