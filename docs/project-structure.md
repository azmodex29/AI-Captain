# Project Structure

```text
AI-Captain/
├── backend/                # Flask Backend
│   ├── app/
│   │   ├── api/            # API Endpoints (Blueprints)
│   │   ├── services/       # Business Logic (Routing, Risk, Weather)
│   │   ├── repositories/   # DB Access Layer
│   │   ├── models/         # SQLAlchemy Models
│   │   ├── schemas/        # Pydantic Schemas
│   │   ├── core/           # Config, Security, Constants
│   │   ├── utils/          # Helpers (GIS, Math)
│   │   └── data/           # Static Datasets (Ports, Piracy Zones)
│   ├── migrations/         # Alembic Migrations
│   ├── tests/              # Pytest Suite
│   ├── .env.example
│   ├── config.py
│   ├── manage.py
│   └── requirements.txt
├── frontend/               # React Frontend
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── hooks/
│   │   ├── store/
│   │   └── utils/
│   ├── public/
│   └── package.json
├── docs/                   # Documentation
├── scripts/                # Setup and Utility Scripts
└── README.md
```
