import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from app.core.config import config_by_name
from app.core.errors import register_error_handlers

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='dev'):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Logging setup
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info(f"Starting AI Captain in {config_name} mode")

    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    register_error_handlers(app)

    # Import models to ensure they are registered with SQLAlchemy
    from app.models.user import User
    from app.models.route import Route
    from app.models.history import RouteHistory

    # Create tables
    with app.app_context():
        db.create_all()

    # Register Blueprints
    from app.api.routes import bp as routes_bp
    app.register_blueprint(routes_bp, url_prefix='/api')

    from app.api.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    @app.route('/health')
    def health_check():
        return {'status': 'healthy'}, 200

    return app
