from flask import Blueprint
from flask_restx import Api
from .auth import api as auth_ns
from .users import api as users_ns

api_bp = Blueprint('api', __name__)
api = Api(api_bp,
    title='User Management API',
    version='1.0',
    description='A simple user management API with Role-based access control',
    doc='/swagger/'
)

api.add_namespace(auth_ns)
api.add_namespace(users_ns)