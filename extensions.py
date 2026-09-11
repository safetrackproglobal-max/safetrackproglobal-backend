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

# Create extensions without binding to app
db = SQLAlchemy()
socketio = SocketIO()
cors = CORS()
mail = Mail()
jwt = JWTManager()
limiter = Limiter(key_func=get_remote_address)

