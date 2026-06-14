from flask import Blueprint, jsonify, request
import json
import os
from app.services.graph_service import GraphService
from app.services.route_engine import RouteEngine
from app.services.geo_analysis_service import GeoAnalysisService
from app.services.piracy_analyzer import PiracyAnalyzer
from app.services.weather_analyzer import WeatherAnalyzer
from app.services.risk_fusion_engine import RiskFusionEngine
from app.services.advisor_service import AdvisorService
from app.services.history_service import HistoryService
from app.core.security import token_required

bp = Blueprint('routes', __name__)

# Initialize services
graph_service = GraphService()
graph = graph_service.load_graph()
route_engine = RouteEngine(graph)
piracy_analyzer = PiracyAnalyzer()
weather_analyzer = WeatherAnalyzer()
risk_fusion_engine = RiskFusionEngine()
advisor_service = AdvisorService()
history_service = HistoryService()

@bp.route('/ports', methods=['GET'])
def get_ports():
    ports_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'ports', 'ports.json')
    with open(ports_path, 'r') as f:
        ports = json.load(f)
    return jsonify(ports), 200

@bp.route('/routes', methods=['POST'])
@token_required
def create_route(current_user):
    data = request.get_json()
    source_id = data.get('source_id')
    dest_id = data.get('destination_id')

    if not source_id or not dest_id:
        return jsonify({"message": "Source and destination IDs are required"}), 400

    # 1. Routing
    start_node = f"port_{source_id}"
    end_node = f"port_{dest_id}"
    
    route_result = route_engine.find_route(start_node, end_node)
    if not route_result:
        return jsonify({"message": "No route found"}), 404

    geometry = route_engine.get_route_geometry(route_result['path'])
    linestring = GeoAnalysisService.create_linestring(geometry['coordinates'])

    # 2. Piracy Analysis
    piracy_score, intersected_zones = piracy_analyzer.calculate_piracy_risk(linestring)

    # 3. Weather Analysis
    weather_score, weather_details = weather_analyzer.calculate_weather_risk(geometry['coordinates'])

    # 4. Risk Fusion
    overall_risk = risk_fusion_engine.calculate_overall_risk(piracy_score, weather_score)

    # 5. Recommendations
    analysis_results = {
        "distance": round(route_result['distance'], 2),
        "eta": route_result['eta'],
        "piracy_risk": piracy_score,
        "weather_risk": weather_score,
        "overall_risk": overall_risk
    }
    recommendation = advisor_service.generate_recommendation(analysis_results)

    # 6. Prepare Response
    full_response = {
        "id": None, # Will be set after saving
        "source_port": start_node,
        "destination_port": end_node,
        "distance": analysis_results['distance'],
        "eta": analysis_results['eta'],
        "risk_score": overall_risk,
        "geometry": geometry,
        "analysis": {
            "piracy": {
                "score": piracy_score,
                "zones": intersected_zones
            },
            "weather": {
                "score": weather_score,
                "details": weather_details
            }
        },
        "recommendation": recommendation
    }

    # 7. Save to History
    saved_route = history_service.save_route_to_history(current_user.id, full_response)
    full_response['id'] = saved_route.id

    return jsonify(full_response), 201

@bp.route('/routes', methods=['GET'])
@token_required
def get_user_history(current_user):
    history = history_service.get_user_history(current_user.id)
    return jsonify(history), 200

@bp.route('/routes/<route_id>', methods=['GET'])
@token_required
def get_route_details(current_user, route_id):
    from app.models.route import Route
    route = Route.query.get(route_id)
    if not route:
        return jsonify({"message": "Route not found"}), 404
        
    # Check if this route belongs to the user via history
    from app.models.history import RouteHistory
    history = RouteHistory.query.filter_by(user_id=current_user.id, route_id=route_id).first()
    if not history:
        return jsonify({"message": "Unauthorized"}), 403

    return jsonify({
        "id": route.id,
        "source_port": route.source_port,
        "destination_port": route.destination_port,
        "distance": route.distance,
        "eta": route.eta,
        "risk_score": route.risk_score,
        "geometry": route.geometry,
        "created_at": route.created_at.isoformat()
    }), 200
