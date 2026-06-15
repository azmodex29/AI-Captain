import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key')
    
    # Handle Render/Heroku 'postgres://' prefix which SQLAlchemy 1.4+ does not support
    uri = os.environ.get('DATABASE_URL', 'sqlite:///dev.db')
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    
    # Render doesn't support IPv6, and Supabase sometimes defaults to it.
    # We force IPv4 by appending ?ipv6=false to Supabase URIs if not already present.
    if uri and "supabase.co" in uri and "ipv6=false" not in uri:
        separator = "&" if "?" in uri else "?"
        uri = f"{uri}{separator}ipv6=false"
    
    SQLALCHEMY_DATABASE_URI = uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    # Production specific settings
    pass

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config_by_name = {
    'dev': DevelopmentConfig,
    'prod': ProductionConfig,
    'test': TestingConfig
}
