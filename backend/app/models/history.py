from datetime import datetime
from app import db
import uuid

class RouteHistory(db.Model):
    __tablename__ = 'route_history'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    route_id = db.Column(db.String(36), db.ForeignKey('routes.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
