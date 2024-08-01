from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import create_access_token
import re
from app.models import User
from app import db

api = Namespace('auth', description='Authentication operations')

register_model = api.model('Register', {
    'username': fields.String(required=True),
    'password': fields.String(required=True),
    'email': fields.String(required=True),
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True)
})

login_model = api.model('Login', {
    'username': fields.String(required=True),
    'password': fields.String(required=True)
})

def is_valid_email(email):
    # Define a regex for validating an email
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email) is not None

@api.route('/register')
class Register(Resource):
    @api.expect(register_model)
    def post(self):
        data = request.json
        
        # Check for missing fields
        required_fields = ['username', 'password', 'email', 'first_name', 'last_name']
        for field in required_fields:
            if field not in data or not data[field]:
                return {'message': f'{field} is required and cannot be empty'}, 400
        
        # Check for unique username and email
        if User.query.filter_by(username=data['username']).first():
            return {'message': 'Username already exists'}, 400
        if User.query.filter_by(email=data['email']).first():
            return {'message': 'Email already exists'}, 400
        
        # Validate email format
        if not is_valid_email(data['email']):
            return {'message': 'Invalid email address'}, 400
        
        # Create and save the user
        user = User(
            username=data['username'],
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name']
        )
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        return {'message': 'User created successfully'}, 201

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        data = request.json
        
        # Check for missing or empty fields
        if 'username' not in data or not data['username']:
            return {'message': 'Username is required and cannot be empty'}, 400
        if 'password' not in data or not data['password']:
            return {'message': 'Password is required and cannot be empty'}, 400

        user = User.query.filter_by(username=data['username']).first()
        if user and user.check_password(data['password']):
            access_token = create_access_token(identity=user.id)
            return {'access_token': access_token}, 200
        return {'message': 'Invalid credentials'}, 401

# Implement password reset endpoints here