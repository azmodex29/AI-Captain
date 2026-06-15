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
    # We force IPv4 by resolving the hostname and passing it as hostaddr.
    if uri and "supabase.co" in uri and "hostaddr=" not in uri:
        import socket
        from urllib.parse import urlparse
        try:
            parsed = urlparse(uri)
            hostname = parsed.hostname
            if hostname:
                # Explicitly resolve to an IPv4 address
                addr_info = socket.getaddrinfo(hostname, None, socket.AF_INET)
                if addr_info:
                    ipv4 = addr_info[0][4][0]
                    separator = "&" if "?" in uri else "?"
                    uri = f"{uri}{separator}hostaddr={ipv4}"
                    print(f"INFO: Resolved {hostname} to IPv4 {ipv4} for hostaddr")
        except Exception as e:
            print(f"ERROR: Failed to resolve IPv4 for {hostname}: {e}")
            pass
    
    # Safe logging of the URI (masking password)
    try:
        from urllib.parse import urlparse
        p = urlparse(uri)
        masked_uri = f"{p.scheme}://{p.username}:****@{p.hostname}:{p.port}{p.path}"
        if p.query:
            masked_uri += f"?{p.query}"
        print(f"INFO: Using Database URI: {masked_uri}")
    except:
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
