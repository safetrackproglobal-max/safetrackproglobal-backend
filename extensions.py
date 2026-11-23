# extensions.py
"""
Centralized Flask extensions - breaks circular imports
All extensions are created here without binding to app
"""
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_cors import CORS
from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_jwt_extended import JWTManager
from flask import request


def client_ip():
    """Real client IP behind Railway's proxy: the right-most X-Forwarded-For entry is the one the proxy added.
    get_remote_address alone returns the proxy's address, which made every user share one rate-limit bucket."""
    try:
        xff = [p.strip() for p in (request.headers.get('X-Forwarded-For') or '').split(',') if p.strip()]
        return (xff[-1] if xff else get_remote_address() or 'unknown')[:64]
    except Exception:
        return get_remote_address()

# Create extensions without binding to app
db = SQLAlchemy()
socketio = SocketIO()
cors = CORS()
mail = Mail()
jwt = JWTManager()
limiter = Limiter(key_func=client_ip)

