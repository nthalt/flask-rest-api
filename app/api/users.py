from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User
from app import db

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'id': fields.Integer(readonly=True),
    'username': fields.String(required=True),
    'email': fields.String(required=True),
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'role': fields.String(required=True),
    'is_active': fields.Boolean(required=True)
})

@api.route('/')
class UserList(Resource):
    @api.marshal_list_with(user_model)
    @jwt_required()
    def get(self):
        return User.query.all()

@api.route('/<int:id>')
class UserResource(Resource):
    @api.marshal_with(user_model)
    @jwt_required()
    def get(self, id):
        return User.query.get_or_404(id)

    @api.expect(user_model)
    @api.marshal_with(user_model)
    @jwt_required()
    def put(self, id):
        user = User.query.get_or_404(id)
        data = api.payload
        user.username = data['username']
        user.email = data['email']
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.is_active = data['is_active']
        db.session.commit()
        return user

    @jwt_required()
    def delete(self, id):
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return '', 204