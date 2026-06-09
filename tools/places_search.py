import requests
from uuid import uuid4

from models.competitor import CompetitorProfile


NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
OVERPASS_URL = "https://overpass-api.de/api/interpreter"


class PlaceSearchTool:

    @staticmethod
    def get_coordinates(location: str):
        """
        Convert location name to coordinates.
        """

        params = {
            "q": location,
            "format": "json",
            "limit": 1
        }

        headers = {
            "User-Agent": "CompetitorIntelligenceAgent"
        }

        response = requests.get(
            NOMINATIM_URL,
            params=params,
            headers=headers,
            timeout=30
        )

        response.raise_for_status()

        results = response.json()

        if not results:
            raise ValueError(
                f"Could not find location: {location}"
            )

        return (
            float(results[0]["lat"]),
            float(results[0]["lon"])
        )

    @staticmethod
    def search_clothing_stores(
        location: str,
        radius_meters: int = 1000
    ):
        """
        Find nearby clothing stores.
        """

        lat, lon = PlaceSearchTool.get_coordinates(
            location
        )

        query = f"""
        [out:json];

        (
          node
            ["shop"="clothes"]
            (around:{radius_meters},{lat},{lon});

          way
            ["shop"="clothes"]
            (around:{radius_meters},{lat},{lon});

          relation
            ["shop"="clothes"]
            (around:{radius_meters},{lat},{lon});
        );

        out center;
        """

        response = requests.post(
            OVERPASS_URL,
            data=query,
            timeout=60
        )

        response.raise_for_status()

        data = response.json()

        competitors = []

        for item in data.get("elements", []):

            tags = item.get("tags", {})

            name = tags.get("name")

            if not name:
                continue

            latitude = item.get(
                "lat",
                item.get("center", {}).get("lat")
            )

            longitude = item.get(
                "lon",
                item.get("center", {}).get("lon")
            )

            competitor = CompetitorProfile(
                store_id=str(uuid4()),
                name=name,
                address=tags.get(
                    "addr:street",
                    "Address unavailable"
                ),
                distance_meters=0,
                peak_hours=[],
                source="OpenStreetMap",
                confidence_score=0.80,
                latitude=latitude,
                longitude=longitude,
                business_status="ACTIVE"
            )

            competitors.append(competitor)

        return competitors