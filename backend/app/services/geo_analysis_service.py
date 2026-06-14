from shapely.geometry import LineString, Polygon, Point, mapping
from shapely.ops import nearest_points
import json

class GeoAnalysisService:
    @staticmethod
    def create_linestring(coordinates):
        """Converts list of [lon, lat] coordinates to a Shapely LineString."""
        return LineString(coordinates)

    @staticmethod
    def create_polygon(coordinates):
        """Converts list of [lon, lat] coordinates (nested) to a Shapely Polygon."""
        return Polygon(coordinates[0])

    @staticmethod
    def intersects(geometry1, geometry2):
        """Checks if two geometries intersect."""
        return geometry1.intersects(geometry2)

    @staticmethod
    def intersection_length(linestring, polygon):
        """Calculates the length of the part of the linestring that is inside the polygon."""
        intersection = linestring.intersection(polygon)
        if intersection.is_empty:
            return 0.0
        return intersection.length

    @staticmethod
    def distance_to_polygon(point, polygon):
        """Calculates the minimum distance from a point to a polygon."""
        p1, p2 = nearest_points(point, polygon)
        return p1.distance(p2)

    @staticmethod
    def load_geojson_polygons(file_path):
        """Loads polygons from a GeoJSON file."""
        polygons = []
        with open(file_path, 'r') as f:
            data = json.load(f)
            for feature in data['features']:
                if feature['geometry']['type'] == 'Polygon':
                    poly = Polygon(feature['geometry']['coordinates'][0])
                    polygons.append({
                        "name": feature['properties'].get('name', 'Unknown'),
                        "risk_level": feature['properties'].get('risk_level', 'Unknown'),
                        "geometry": poly
                    })
        return polygons
