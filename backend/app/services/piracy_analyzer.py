import os
from app.services.geo_analysis_service import GeoAnalysisService

class PiracyAnalyzer:
    def __init__(self):
        self.geo_service = GeoAnalysisService()
        self.piracy_zones_path = os.path.join(
            os.path.dirname(__file__), '..', 'data', 'piracy', 'piracy_zones.geojson'
        )
        self.zones = self.geo_service.load_geojson_polygons(self.piracy_zones_path)

    def calculate_piracy_risk(self, route_linestring):
        """
        Calculates piracy risk score (0-100) based on route intersection 
        with piracy zones.
        """
        total_risk_score = 0
        intersected_zones = []

        route_length = route_linestring.length
        if route_length == 0:
            return 0, []

        for zone in self.zones:
            if self.geo_service.intersects(route_linestring, zone['geometry']):
                # Calculate what percentage of the route is within the zone
                intersection_len = self.geo_service.intersection_length(
                    route_linestring, zone['geometry']
                )
                
                percentage_in_zone = (intersection_len / route_length) * 100
                
                # Risk weight based on zone level
                weight = 1.0 if zone['risk_level'] == 'High' else 0.5
                
                # Contribution to score (max 100)
                # We cap it so that even a short trip entirely in a high risk zone is 100
                zone_risk = min(percentage_in_zone * 2 * weight, 100)
                total_risk_score += zone_risk
                
                intersected_zones.append({
                    "name": zone['name'],
                    "risk_level": zone['risk_level'],
                    "percentage_of_route": round(percentage_in_zone, 2)
                })

        return min(round(total_risk_score), 100), intersected_zones
