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
    # We force IPv4 by resolving the hostname and replacing it in the URI.
    if uri and "supabase.co" in uri:
        import socket
        from urllib.parse import urlparse
        try:
            parsed = urlparse(uri)
            hostname = parsed.hostname
            if hostname and not hostname.replace('.', '').isdigit(): # Only if it's not already an IP
                # Explicitly resolve to an IPv4 address
                addr_info = socket.getaddrinfo(hostname, None, socket.AF_INET)
                if addr_info:
                    ipv4 = addr_info[0][4][0]
                    # Replace hostname with IP in the netloc (handles user:pass@host:port)
                    new_netloc = parsed.netloc.replace(hostname, ipv4)
                    new_parsed = parsed._replace(netloc=new_netloc)
                    uri = new_parsed.geturl()
                    
                    # Ensure sslmode=require is present as we're using an IP
                    if "sslmode" not in uri:
                        separator = "&" if "?" in uri else "?"
                        uri = f"{uri}{separator}sslmode=require"
                    
                    print(f"INFO: Resolved {hostname} -> {ipv4}. Final URI host replaced.")
        except Exception as e:
            print(f"ERROR: IPv4 resolution failed for {hostname}: {e}")
            pass
    
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
