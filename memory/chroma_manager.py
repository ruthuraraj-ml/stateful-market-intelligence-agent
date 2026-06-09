from chromadb import PersistentClient


class ChromaManager:

    def __init__(self):

        self.client = PersistentClient(
            path="memory_db"
        )

        self.collection = (
            self.client.get_or_create_collection(
                name="competitor_analysis_memory"
            )
        )