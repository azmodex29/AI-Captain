import os
import sys

# Add backend directory to sys.path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app import create_app, db
from app.models import User, Route, RouteHistory

def init_db():
    app = create_app('dev')
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("Database initialized successfully.")

if __name__ == '__main__':
    init_db()
