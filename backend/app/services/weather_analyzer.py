import requests
import logging

class WeatherAnalyzer:
    def __init__(self):
        self.base_url = "https://marine-api.open-meteo.com/v1/marine"

    def fetch_weather_for_point(self, lat, lon):
        """Fetches marine weather for a single coordinate."""
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": ["wind_speed_10m", "wave_height", "wind_gusts_10m"],
            "timezone": "auto"
        }
        try:
            response = requests.get(self.base_url, params=params, timeout=5)
            if response.status_code == 200:
                return response.json().get('current', {})
            return None
        except Exception as e:
            logging.error(f"Error fetching weather: {e}")
            return None

    def calculate_weather_risk(self, coordinates):
        """
        Calculates weather risk score (0-100) by sampling points along the route.
        """
        if not coordinates:
            return 0, {}

        # Sample at most 5 points to avoid excessive API calls
        sample_size = min(5, len(coordinates))
        step = max(1, len(coordinates) // sample_size)
        sample_points = coordinates[::step]

        total_wind_speed = 0
        total_wave_height = 0
        valid_samples = 0

        for lon, lat in sample_points:
            weather = self.fetch_weather_for_point(lat, lon)
            if weather:
                # Use getattr-like safety or or operator to handle None from .get()
                wind = weather.get('wind_speed_10m')
                wave = weather.get('wave_height')
                
                total_wind_speed += wind if wind is not None else 0
                total_wave_height += wave if wave is not None else 0
                valid_samples += 1

        if valid_samples == 0:
            return 0, {"message": "Weather data unavailable"}

        avg_wind = total_wind_speed / valid_samples
        avg_wave = total_wave_height / valid_samples

        # Simple risk scoring logic:
        # High wind (> 30 knots) or high waves (> 4 meters) increase risk
        wind_risk = min((avg_wind / 40) * 100, 100)
        wave_risk = min((avg_wave / 6) * 100, 100)

        total_risk = (wind_risk * 0.4) + (wave_risk * 0.6)

        return round(total_risk), {
            "avg_wind_speed": round(avg_wind, 2),
            "avg_wave_height": round(avg_wave, 2),
            "samples_analyzed": valid_samples
        }
