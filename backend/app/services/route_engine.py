import networkx as nx
from app.services.graph_service import haversine

class RouteEngine:
    def __init__(self, graph):
        self.graph = graph
        self.average_speed = 15 # average speed in knots

    def heuristic(self, u, v):
        """Heuristic for A*: haversine distance between nodes."""
        node_u = self.graph.nodes[u]
        node_v = self.graph.nodes[v]
        return haversine(node_u['lon'], node_u['lat'], node_v['lon'], node_v['lat'])

    def find_route(self, start_node, end_node):
        """
        Calculates the shortest path using A*.
        Returns path nodes and total distance.
        """
        try:
            path = nx.astar_path(
                self.graph, 
                start_node, 
                end_node, 
                heuristic=self.heuristic, 
                weight='weight'
            )
            
            distance = nx.path_weight(self.graph, path, weight='weight')
            
            return {
                "path": path,
                "distance": distance,
                "eta": self.estimate_eta(distance)
            }
        except nx.NetworkXNoPath:
            return None

    def estimate_eta(self, distance):
        """Estimate ETA in days."""
        hours = distance / self.average_speed
        return round(hours / 24, 2)

    def get_route_geometry(self, path):
        """Converts path nodes into GeoJSON LineString coordinates."""
        coordinates = []
        for node in path:
            data = self.graph.nodes[node]
            coordinates.append([data['lon'], data['lat']])
        
        return {
            "type": "LineString",
            "coordinates": coordinates
        }

    def find_alternative_routes(self, start_node, end_node, num_alternatives=2):
        """
        Generates alternative routes by temporarily removing edges 
        from the shortest path.
        """
        alternatives = []
        original_result = self.find_route(start_node, end_node)
        if not original_result:
            return []

        alternatives.append(original_result)
        
        # Simple strategy: remove one edge at a time from the original path
        # and re-run A*. This is a variation of Yen's algorithm.
        original_path = original_result['path']
        
        for i in range(len(original_path) - 1):
            if len(alternatives) > num_alternatives:
                break
                
            u, v = original_path[i], original_path[i+1]
            
            # Temporarily remove edge
            if self.graph.has_edge(u, v):
                edge_data = self.graph.get_edge_data(u, v)
                self.graph.remove_edge(u, v)
                
                alt_result = self.find_route(start_node, end_node)
                if alt_result and alt_result['path'] not in [a['path'] for a in alternatives]:
                    alternatives.append(alt_result)
                
                # Restore edge
                self.graph.add_edge(u, v, **edge_data)
                
        return alternatives
