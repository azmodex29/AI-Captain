from datetime import datetime
from app import db
import uuid

class Route(db.Model):
    __tablename__ = 'routes'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    source_port = db.Column(db.String(100), nullable=False)
    destination_port = db.Column(db.String(100), nullable=False)
    distance = db.Column(db.Float, nullable=False)
    eta = db.Column(db.Float, nullable=False)
    risk_score = db.Column(db.Integer, default=0)
    geometry = db.Column(db.JSON, nullable=False) # Store GeoJSON geometry
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    history_entries = db.relationship('RouteHistory', backref='route', lazy=True)
