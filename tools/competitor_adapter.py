from models.competitor import CompetitorProfile


class CompetitorAdapter:

    @staticmethod
    def from_apify(place: dict) -> CompetitorProfile:
        """
        Convert raw Apify result into CompetitorProfile.
        """

        return CompetitorProfile(
            store_id=place.get("placeId", ""),

            name=place.get("title", "Unknown Store"),

            address=place.get("address", "Unknown Address"),

            rating=place.get("totalScore"),

            review_count=place.get("reviewsCount"),

            distance_meters=0.0,

            peak_hours=[],

            footfall_score=None,

            footfall_level=None,

            confidence_score=0.90,

            source="Apify Google Maps",

            latitude=place.get(
                "location",
                {}
            ).get("lat"),

            longitude=place.get(
                "location",
                {}
            ).get("lng"),

            business_status=(
                "CLOSED"
                if place.get("permanentlyClosed")
                else "ACTIVE"
            ),

            website=place.get("website"),

            phone=place.get("phone"),

            opening_hours=place.get(
                "openingHours",
                []
            ),

            categories=place.get(
                "categories",
                []
            ),

            rank=place.get("rank"),

            place_id=place.get("placeId"),

            popular_times=place.get(
                "popularTimesHistogram",
                {}
            )
        )