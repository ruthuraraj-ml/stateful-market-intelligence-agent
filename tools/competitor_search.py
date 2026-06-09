from apify_client import ApifyClient
from config.settings import settings


class CompetitorSearchTool:

    def __init__(self):
        self.client = ApifyClient(
            settings.APIFY_API_TOKEN
        )

    def search_competitors(
        self,
        location: str,
        max_results: int = 20
    ):
        """
        Find nearby clothing stores along with rich footfall, peak hours, 
        ratings, and operational metrics.
        """

        actor_input = {
            "searchStringsArray": [
                f"clothing stores in {location}"
            ],
            "maxCrawledPlacesPerSearch": max_results,
            "includePopularTimes": True,
            "skipClosedPlaces": True
        }

        run = self.client.actor(
            "compass/crawler-google-places"
        ).call(
            run_input=actor_input
        )

        # Using our verified Pydantic property mapping
        dataset_id = run.default_dataset_id

        results = list(
            self.client.dataset(
                dataset_id
            ).iterate_items()
        )

        return results