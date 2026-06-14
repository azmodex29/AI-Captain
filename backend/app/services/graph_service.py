import json
import networkx as nx
from math import radians, cos, sin, asin, sqrt
import os

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 3440 # Radius of earth in nautical miles. Use 6371 for kilometers
    return c * r

class GraphService:
    def __init__(self):
        self.graph = nx.Graph()
        self.data_path = os.path.join(os.path.dirname(__file__), '..', 'data')

    def load_graph(self):
        # 1. Load Ports
        ports_path = os.path.join(self.data_path, 'ports', 'ports.json')
        with open(ports_path, 'r') as f:
            ports = json.load(f)
            for port in ports:
                self.graph.add_node(
                    f"port_{port['id']}", 
                    name=port['name'], 
                    lat=port['lat'], 
                    lon=port['lon'],
                    type='port'
                )

        # 2. Load Network (Waypoints and Lanes)
        network_path = os.path.join(self.data_path, 'network', 'maritime_network.geojson')
        with open(network_path, 'r') as f:
            network = json.load(f)
            
            # First pass: add waypoints
            for feature in network['features']:
                if feature['properties']['type'] == 'waypoint':
                    geom = feature['geometry']
                    self.graph.add_node(
                        feature['properties']['name'],
                        lat=geom['coordinates'][1],
                        lon=geom['coordinates'][0],
                        type='waypoint'
                    )

            # Second pass: add lanes (edges)
            for feature in network['features']:
                if feature['properties']['type'] == 'lane':
                    coords = feature['geometry']['coordinates']
                    # This is a simplification: connecting ports to waypoints or directly
                    # For now, we assume lanes connect specific points in our graph
                    # In a real system, we'd find the nearest nodes
                    for i in range(len(coords) - 1):
                        p1 = coords[i]
                        p2 = coords[i+1]
                        dist = haversine(p1[0], p1[1], p2[0], p2[1])
                        # We use coordinates as node IDs for intermediate lane points if they don't exist
                        n1_id = f"{p1[0]},{p1[1]}"
                        n2_id = f"{p2[0]},{p2[1]}"
                        
                        if not self.graph.has_node(n1_id):
                            self.graph.add_node(n1_id, lat=p1[1], lon=p1[0], type='waypoint')
                        if not self.graph.has_node(n2_id):
                            self.graph.add_node(n2_id, lat=p2[1], lon=p2[0], type='waypoint')
                            
                        self.graph.add_edge(n1_id, n2_id, weight=dist)

        # 3. Connect Ports to nearest nodes in the graph
        for node, data in list(self.graph.nodes(data=True)):
            if data.get('type') == 'port':
                # Find nearest non-port node
                min_dist = float('inf')
                nearest_wp = None
                for wp_node, wp_data in self.graph.nodes(data=True):
                    if wp_data.get('type') != 'port' and wp_node != node:
                        d = haversine(data['lon'], data['lat'], wp_data['lon'], wp_data['lat'])
                        if d < min_dist:
                            min_dist = d
                            nearest_wp = wp_node
                
                if nearest_wp and min_dist < 50: # Only connect if reasonably close (50nm)
                    self.graph.add_edge(node, nearest_wp, weight=min_dist)

        return self.graph

    def get_nearest_node(self, lat, lon):
        min_dist = float('inf')
        nearest_node = None
        for node, data in self.graph.nodes(data=True):
            dist = haversine(lon, lat, data['lon'], data['lat'])
            if dist < min_dist:
                min_dist = dist
                nearest_node = node
        return nearest_node
