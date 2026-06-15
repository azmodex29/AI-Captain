import json
import networkx as nx
from math import radians, cos, sin, asin, sqrt
import os
from shapely.geometry import Point, Polygon

def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 3440 # Nautical miles
    return c * r

class GraphService:
    def __init__(self):
        self.graph = nx.Graph()
        self.data_path = os.path.join(os.path.dirname(__file__), '..', 'data')
        # Simplified landmask polygons for major continents
        self.land_polygons = [
            # Africa
            Polygon([(20,-35), (51,-35), (51,37), (-17,37), (-17,5), (20,-35)]),
            # Americas (North & South)
            Polygon([(-168,72), (-50,72), (-35,-55), (-82,-55), (-168,72)]),
            # Eurasia
            Polygon([(170,75), (170,1), (80,1), (80,-10), (10,35), (-10,35), (-10,75), (170,75)]),
            # Australia
            Polygon([(113,-10), (154,-10), (154,-40), (113,-40), (113,-10)])
        ]

    def is_land(self, lat, lon):
        p = Point(lon, lat)
        for poly in self.land_polygons:
            if poly.contains(p):
                return True
        return False

    def load_graph(self):
        # 1. Generate Grid Nodes (5-degree resolution)
        for lat in range(-60, 80, 5):
            for lon in range(-180, 185, 5):
                if not self.is_land(lat, lon):
                    node_id = f"{lon},{lat}"
                    self.graph.add_node(node_id, lat=lat, lon=lon, type='waypoint')

        # 2. Add Passage Points (Critical Straits)
        passages = [
            {"name": "Suez", "lat": 29.9, "lon": 32.5},
            {"name": "Panama", "lat": 9.35, "lon": -79.9},
            {"name": "Gibraltar", "lat": 35.9, "lon": -5.4},
            {"name": "Malacca", "lat": 2.5, "lon": 101.0},
            {"name": "Bab-el-Mandeb", "lat": 12.6, "lon": 43.3},
            {"name": "Hormuz", "lat": 26.6, "lon": 56.3},
            {"name": "English Channel", "lat": 50.0, "lon": -1.0}
        ]
        for p in passages:
            node_id = f"{p['lon']},{p['lat']}"
            self.graph.add_node(node_id, lat=p['lat'], lon=p['lon'], type='waypoint')

        # 3. Connect Grid with 8-way connectivity
        nodes = list(self.graph.nodes(data=True))
        for i, (n1_id, d1) in enumerate(nodes):
            for j in range(i + 1, len(nodes)):
                n2_id, d2 = nodes[j]
                # Connect if nodes are within ~7.5 degrees (covers diagonals in 5-deg grid)
                if abs(d1['lat'] - d2['lat']) <= 6 and abs(d1['lon'] - d2['lon']) <= 6:
                    dist = haversine(d1['lon'], d1['lat'], d2['lon'], d2['lat'])
                    self.graph.add_edge(n1_id, n2_id, weight=dist)

        # 4. Load Ports and connect to nearest grid node
        ports_path = os.path.join(self.data_path, 'ports', 'ports.json')
        with open(ports_path, 'r') as f:
            ports = json.load(f)
            for port in ports:
                port_id = f"port_{port['id']}"
                self.graph.add_node(port_id, name=port['name'], lat=port['lat'], lon=port['lon'], type='port')
                
                # Find nearest waypoint node
                nearest_wp = None
                min_dist = float('inf')
                for node, data in self.graph.nodes(data=True):
                    if data.get('type') == 'waypoint':
                        d = haversine(port['lon'], port['lat'], data['lon'], data['lat'])
                        if d < min_dist:
                            min_dist = d
                            nearest_wp = node
                
                if nearest_wp:
                    self.graph.add_edge(port_id, nearest_wp, weight=min_dist)

        # 5. Integrate Piracy Risk into Weights
        piracy_path = os.path.join(self.data_path, 'piracy', 'piracy_zones.geojson')
        with open(piracy_path, 'r') as f:
            piracy_data = json.load(f)
            zones = []
            for feature in piracy_data['features']:
                zones.append({
                    "poly": Polygon(feature['geometry']['coordinates'][0]),
                    "risk": 5.0 if feature['properties']['risk_level'] == 'High' else 2.0
                })

        for u, v, data in self.graph.edges(data=True):
            # Check if edge midpoint is in a piracy zone
            node_u = self.graph.nodes[u]
            node_v = self.graph.nodes[v]
            mid_lat = (node_u['lat'] + node_v['lat']) / 2
            mid_lon = (node_u['lon'] + node_v['lon']) / 2
            mid_p = Point(mid_lon, mid_lat)
            
            for zone in zones:
                if zone['poly'].contains(mid_p):
                    data['weight'] *= zone['risk']
                    break

        return self.graph
