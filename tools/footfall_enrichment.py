import os
import json
import requests
from config.settings import settings

class FootfallEnrichmentTool:
    def __init__(self):
        self.api_key = settings.BESTTIME_API_KEY
        self.base_url = "https://besttime.app/api/v1/forecasts"
        # Create a local cache folder to store successful API responses
        self.cache_dir = "cache_data/footfall"
        os.makedirs(self.cache_dir, exist_ok=True)

    def _get_cache_filename(self, name: str) -> str:
        """Generates a clean file path based on the venue name."""
        safe_name = "".join([c if c.isalnum() else "_" for c in name]).lower()
        return os.path.join(self.cache_dir, f"{safe_name}.json")

    def get_footfall_analytics(self, name: str, address: str) -> dict:
        """
        Resilient foot traffic query with local fallback caching to preserve credits.
        """
        cache_path = self._get_cache_filename(name)

        # 🎯 CREDIT PROTECTION CHECK: Do we already have this data locally?
        if os.path.exists(cache_path):
            print(f"📦 [CACHE HIT] Reading local footfall profile for '{name}' (0 credits consumed)")
            with open(cache_path, "r") as f:
                return json.load(f)

        if not self.api_key:
            return {"error": "BestTime API Key is missing from settings configuration."}

        params = {
            "api_key_private": self.api_key,
            "venue_name": name,
            "venue_address": address
        }

        try:
            print(f"📡 [LIVE API CALL] Querying BestTime for '{name}' (Costs 2 credits)...")
            response = requests.post(self.base_url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("status") == "OK":
                    analysis_list = data.get("analysis", [])
                    processed_days = {}
                    busiest_days = []
                    
                    for day_data in analysis_list:
                        day_info = day_data.get("day_info", {})
                        day_name = day_info.get("day_text", "unknown").lower()
                        
                        avg_traffic = day_info.get("day_mean", 0)
                        peak_traffic = day_info.get("day_max", 0)
                        
                        processed_days[day_name] = {
                            "avg_traffic_pct": avg_traffic,
                            "peak_traffic_pct": peak_traffic
                        }
                        
                        if avg_traffic >= 60 or peak_traffic >= 90:
                            busiest_days.append(day_name.capitalize())
                    
                    result_payload = {
                        "status": "SUCCESS",
                        "source": "BestTime.app Empirical Data Stream",
                        "busiest_days": busiest_days if busiest_days else ["Weekend Windows"],
                        "weekly_metrics": processed_days
                    }

                    # 💾 SAVE TO CACHE: Save this successful data so we never pay for it again!
                    with open(cache_path, "w") as f:
                        json.dump(result_payload, f, indent=2)

                    return result_payload
                else:
                    return {"status": "UNINDEXED", "message": data.get("message")}
            else:
                return {"status": "ERROR", "message": f"HTTP Error {response.status_code}"}
                
        except Exception as e:
            return {"status": "ERROR", "message": f"Connection error: {str(e)}"}