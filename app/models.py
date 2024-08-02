from app import db
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Enum
import secrets

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(Enum('Admin', 'User', name='user_roles'), default='User')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    password_reset_token = db.Column(db.String(100), unique=True, nullable=True)
    password_reset_expiration = db.Column(db.DateTime, nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_reset_token(self):
        self.password_reset_token = secrets.token_urlsafe(32)
        self.password_reset_expiration = datetime.utcnow() + timedelta(hours=1)
        db.session.commit()
        return self.password_reset_token

    def verify_reset_token(self, token):
        if self.password_reset_token != token:
            return False
        if datetime.utcnow() > self.password_reset_expiration:
            return False
        return True

    def clear_reset_token(self):
        self.password_reset_token = None
        self.password_reset_expiration = None
        db.session.commit()