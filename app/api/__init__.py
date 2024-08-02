from flask import Blueprint
from flask_restx import Api
from .auth import api as auth_ns
from .users import api as users_ns
from flask_jwt_extended import JWTManager

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    },
}

api_bp = Blueprint('api', __name__)
api = Api(api_bp,
    title='User Management API',
    version='1.0',
    description='A simple user management API with Role-based access control',
    doc='/',
    authorizations=authorizations,
    security='Bearer Auth'
)

api.add_namespace(auth_ns)
api.add_namespace(users_ns)