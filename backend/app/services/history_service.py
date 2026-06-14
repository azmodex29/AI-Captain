from app import db
from app.models.route import Route
from app.models.history import RouteHistory

class HistoryService:
    @staticmethod
    def save_route_to_history(user_id, route_data):
        """Saves a calculated route and links it to a user's history."""
        # Check if route already exists (simplification)
        # In a real app, we might check by source/dest or geometry
        
        new_route = Route(
            source_port=route_data['source_port'],
            destination_port=route_data['destination_port'],
            distance=route_data['distance'],
            eta=route_data['eta'],
            risk_score=route_data['risk_score'],
            geometry=route_data['geometry']
        )
        db.session.add(new_route)
        db.session.flush() # Get the new_route.id

        history_entry = RouteHistory(
            user_id=user_id,
            route_id=new_route.id
        )
        db.session.add(history_entry)
        db.session.commit()
        
        return new_route

    @staticmethod
    def get_user_history(user_id):
        """Retrieves history of routes for a specific user."""
        history = RouteHistory.query.filter_by(user_id=user_id).all()
        routes = []
        for entry in history:
            route = Route.query.get(entry.route_id)
            if route:
                routes.append({
                    "id": route.id,
                    "source_port": route.source_port,
                    "destination_port": route.destination_port,
                    "distance": route.distance,
                    "eta": route.eta,
                    "risk_score": route.risk_score,
                    "created_at": route.created_at.isoformat()
                })
        return routes
