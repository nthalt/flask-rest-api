from flask_restx import Namespace, Resource, fields
from flask import request, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import re
from app.models import User
from app import db
from app.utils import send_reset_email

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

forgot_password_model = api.model('ForgotPassword', {
    'email': fields.String(required=True)
})

reset_password_model = api.model('ResetPassword', {
    'token': fields.String(required=True),
    'new_password': fields.String(required=True)
})

def is_valid_email(email):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email) is not None

def is_valid_password(password):
    if len(password) < 8:
        return False
    # if not re.search(r'[0-9]', password):
    #     return False
    # if not re.search(r'[A-Z]', password):
    #     return False
    # if not re.search(r'[a-z]', password):
    #     return False
    # if not re.search(r'[@$!%*?&#]', password):
    #     return False
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

@api.route('/forgot-password')
class ForgotPassword(Resource):
    @api.expect(forgot_password_model)
    def post(self):
        data = request.json
        user = User.query.filter_by(email=data['email']).first()
        if not user:
            return {'message': 'If a user with this email exists, a password reset link has been sent.'}, 200
        
        token = user.generate_reset_token()
        send_reset_email(user.email, token)
        return {'message': 'If a user with this email exists, a password reset link has been sent.'}, 200

@api.route('/reset-password')
class ResetPassword(Resource):
    @api.expect(reset_password_model)
    def post(self):
        data = request.json
        user = User.query.filter_by(password_reset_token=data['token']).first()
        if not user or not user.verify_reset_token(data['token']):
            return {'message': 'Invalid or expired token'}, 400
        
        if not is_valid_password(data['new_password']):
            return {'message': 'Password must be at least 8 characters long'}, 400
        
        user.set_password(data['new_password'])
        user.clear_reset_token()
        db.session.commit()
        return {'message': 'Password has been reset successfully'}, 200

@api.route('/change-password')
class ChangePassword(Resource):
    @jwt_required()
    @api.expect(api.model('ChangePassword', {
        'current_password': fields.String(required=True),
        'new_password': fields.String(required=True)
    }))
    def post(self):
        current_user = User.query.get(get_jwt_identity())
        data = request.json
        
        if not current_user.check_password(data['current_password']):
            return {'message': 'Current password is incorrect'}, 400
        
        if not is_valid_password(data['new_password']):
            return {'message': 'New password must be at least 8 characters long'}, 400
        
        current_user.set_password(data['new_password'])
        db.session.commit()
        return {'message': 'Password changed successfully'}, 200
        
# Implement password reset endpoints here