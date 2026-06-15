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
        # More surgical landmask polygons
        self.land_polygons = [
            # Africa (simplified)
            Polygon([(-20, -35), (52, -35), (52, 12), (32, 30), (-10, 37), (-20, 15)]),
            # South America
            Polygon([(-82, -56), (-34, -10), (-45, 12), (-80, 12), (-82, -56)]),
            # North America
            Polygon([(-168, 72), (-50, 72), (-60, 15), (-130, 15), (-168, 72)]),
            # Eurasia (broken down to avoid blocking Suez/Gibraltar)
            Polygon([(40, 75), (170, 75), (170, 15), (100, 10), (60, 25), (40, 75)]), # Northern Eurasia
            Polygon([(-10, 75), (40, 75), (40, 36), (-10, 36), (-10, 75)]), # Europe
            Polygon([(60, 30), (130, 30), (130, 10), (70, 8), (60, 30)]), # Southern Asia
            # Australia
            Polygon([(113, -40), (154, -40), (154, -10), (113, -10), (113, -40)]),
            # Greenland
            Polygon([(-60, 85), (-10, 85), (-10, 60), (-60, 60), (-60, 85)])
        ]

    def is_land(self, lat, lon):
        p = Point(lon, lat)
        for poly in self.land_polygons:
            if poly.contains(p):
                return True
        return False

    def load_graph(self):
        # 1. Generate Grid Nodes (3-degree resolution for better precision)
        step = 3
        grid_nodes = {}
        for lat in range(-75, 85, step):
            for lon in range(-180, 180, step):
                if not self.is_land(lat, lon):
                    node_id = f"{lon},{lat}"
                    self.graph.add_node(node_id, lat=lat, lon=lon, type='waypoint')
                    grid_nodes[(lon, lat)] = node_id

        # 2. Add Critical Passage Points
        passages = [
            {"name": "Suez South", "lat": 29.8, "lon": 32.5},
            {"name": "Suez North", "lat": 31.3, "lon": 32.3},
            {"name": "Panama East", "lat": 9.3, "lon": -79.9},
            {"name": "Panama West", "lat": 8.9, "lon": -79.6},
            {"name": "Gibraltar", "lat": 35.9, "lon": -5.4},
            {"name": "Malacca", "lat": 2.5, "lon": 101.0},
            {"name": "Bab-el-Mandeb", "lat": 12.6, "lon": 43.3},
            {"name": "Hormuz", "lat": 26.6, "lon": 56.3},
            {"name": "English Channel", "lat": 50.0, "lon": -1.0},
            {"name": "Cape of Good Hope", "lat": -35.0, "lon": 18.5},
            {"name": "Cape Horn", "lat": -56.5, "lon": -67.3},
            {"name": "Bering Strait", "lat": 66.0, "lon": -169.0}
        ]
        for p in passages:
            node_id = f"passage_{p['name'].replace(' ', '_')}"
            self.graph.add_node(node_id, lat=p['lat'], lon=p['lon'], type='waypoint')
            # Connect passage to nearest grid nodes
            for (glon, glat), gn_id in grid_nodes.items():
                if abs(glon - p['lon']) <= step and abs(glat - p['lat']) <= step:
                    d = haversine(p['lon'], p['lat'], glon, glat)
                    self.graph.add_edge(node_id, gn_id, weight=d)

        # 3. Connect Grid with 8-way connectivity (O(N) neighbor lookup)
        for (lon, lat), n1_id in grid_nodes.items():
            for dlon in [-step, 0, step]:
                for dlat in [-step, 0, step]:
                    if dlon == 0 and dlat == 0: continue
                    
                    nlone = lon + dlon
                    nlat = lat + dlat
                    
                    # Wrap longitude for trans-Pacific routes
                    if nlone >= 180: nlone -= 360
                    if nlone < -180: nlone += 360
                    
                    n2_id = grid_nodes.get((nlone, nlat))
                    if n2_id:
                        dist = haversine(lon, lat, nlone, nlat)
                        self.graph.add_edge(n1_id, n2_id, weight=dist)

        # 4. Load Ports and connect to nearest grid node
        ports_path = os.path.join(self.data_path, 'ports', 'ports.json')
        with open(ports_path, 'r') as f:
            ports = json.load(f)
            for port in ports:
                port_id = f"port_{port['id']}"
                self.graph.add_node(port_id, name=port['name'], lat=port['lat'], lon=port['lon'], type='port')
                
                # Find nearest grid node (checking more broadly than before)
                nearest_node = None
                min_dist = float('inf')
                for node, data in self.graph.nodes(data=True):
                    if data.get('type') == 'waypoint':
                        d = haversine(port['lon'], port['lat'], data['lon'], data['lat'])
                        if d < min_dist:
                            min_dist = d
                            nearest_node = node
                
                if nearest_node:
                    self.graph.add_edge(port_id, nearest_node, weight=min_dist)

        # 5. Integrate Piracy Risk into Weights
        piracy_path = os.path.join(self.data_path, 'piracy', 'piracy_zones.geojson')
        with open(piracy_path, 'r') as f:
            piracy_data = json.load(f)
            zones = []
            for feature in piracy_data['features']:
                zones.append({
                    "poly": Polygon(feature['geometry']['coordinates'][0]),
                    "risk": 10.0 if feature['properties']['risk_level'] == 'High' else 3.0
                })

        for u, v, data in self.graph.edges(data=True):
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
