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
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email) is not None

def is_valid_password(password):
    if len(password) < 8:
        return False
    if not re.search(r'[0-9]', password):
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[@$!%*?&#]', password):
        return False
    return True

def is_valid_username(username):
    regex = r'^[a-zA-Z0-9_.-]+$'
    return re.match(regex, username) is not None

@api.route('/register')
class Register(Resource):
    @api.expect(register_model)
    def post(self):
        data = request.json

        # Trim leading and trailing whitespace
        for key in data:
            data[key] = data[key].strip()

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

        # Validate password strength
        if not is_valid_password(data['password']):
            return {'message': 'Password must be at least 8 characters long, contain numbers, uppercase and lowercase letters, and special characters'}, 400

        # Validate username format
        if not is_valid_username(data['username']):
            return {'message': 'Username can only contain letters, numbers, underscores, hyphens, and periods'}, 400

        # Create and save the user
        user = User(
            username=data['username'],
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name']
        )
        user.set_password(data['password'])
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'message': 'An error occurred while creating the user'}, 500

        return {'message': 'User created successfully'}, 201

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        data = request.json

        # Trim leading and trailing whitespace
        data['username'] = data['username'].strip()
        data['password'] = data['password'].strip()

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