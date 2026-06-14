# AI Captain

AI Captain is a maritime decision-support platform that calculates optimal sea routes while considering risks like piracy and weather.

## Features
- **Maritime Routing:** Shortest path calculation using A* on a global maritime network.
- **Piracy Analysis:** Detection of route intersections with known piracy zones.
- **Weather Analysis:** Real-time marine weather forecasting using Open-Meteo.
- **Risk Assessment:** Combined risk scoring and human-readable advice.
- **Route History:** Save and revisit past route calculations.

## Tech Stack
- **Frontend:** React, Vite, Leaflet, Tailwind CSS, Lucide React.
- **Backend:** Flask, SQLAlchemy, NetworkX, Shapely.
- **Database:** PostgreSQL (Supabase).

## Getting Started

### Backend Setup
1. Navigate to `backend/`
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `venv\Scripts\activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Initialize the database: `python ../scripts/init_db.py`
6. Run the server: `python manage.py`

### Frontend Setup
1. Navigate to `frontend/`
2. Install dependencies: `npm install`
3. Run the development server: `npm run dev`

## Deployment
- **Frontend:** Vercel
- **Backend:** Render
- **Database:** Supabase
