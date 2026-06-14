# System Architecture

## Overview
AI Captain is a maritime decision-support platform designed to calculate optimal sea routes while considering risks like piracy and weather.

## Components
- **Frontend**: React + Vite + Leaflet (Map Visualization)
- **Backend**: Flask (API & Routing Logic)
- **Database**: Supabase (PostgreSQL)
- **GIS Engine**: NetworkX (Graph Routing), Shapely (Spatial Analysis)
- **External APIs**: Open-Meteo (Weather Data)

## Data Flow
1. User selects Source and Destination ports on the React Frontend.
2. Frontend sends request to Flask Backend.
3. Backend fetches Port coordinates and Maritime Network data.
4. Route Engine calculates the shortest path using A* on a NetworkX graph.
5. GeoAnalysis Service checks for intersections with Piracy Zones (GeoJSON).
6. Weather Analysis Service fetches forecasts for route waypoints.
7. Risk Fusion Engine computes an overall risk score.
8. Advisor Service generates human-readable recommendations.
9. Results are returned to the Frontend and stored in Supabase.

## Deployment Diagram
- **Frontend**: Vercel
- **Backend**: Render
- **Database**: Supabase
- **Data/Assets**: GitHub Repository
