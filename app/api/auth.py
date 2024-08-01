from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
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

@api.route('/register')
class Register(Resource):
    @api.expect(register_model)
    def post(self):
        data = request.json
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
        user = User.query.filter_by(username=data['username']).first()
        if user and user.check_password(data['password']):
            access_token = create_access_token(identity=user.id)
            return {'access_token': access_token}, 200
        return {'message': 'Invalid credentials'}, 401

# Implement password reset endpoints here