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
    'is_active': fields.Boolean(required=True),
    'created_at': fields.DateTime(readonly=True),
    'updated_at': fields.DateTime(readonly=True)
})

@api.route('/')
class UserList(Resource):
    @api.marshal_list_with(user_model)
    @jwt_required()
    @api.doc(security='Bearer Auth')
    def get(self):
        current_user = User.query.get(get_jwt_identity())
        if current_user.role != 'Admin':
            return {'message': 'Admin access required'}, 403
        return User.query.all()

@api.route('/<int:id>')
class UserResource(Resource):
    @api.marshal_with(user_model)
    @jwt_required()
    @api.doc(security='Bearer Auth')
    def get(self, id):
        current_user = User.query.get(get_jwt_identity())
        if current_user.role != 'Admin' and current_user.id != id:
            return {'message': 'Unauthorized'}, 403
        return User.query.get_or_404(id)

    @api.expect(user_model)
    @api.marshal_with(user_model)
    @jwt_required()
    @api.doc(security='Bearer Auth')
    def put(self, id):
        current_user = User.query.get(get_jwt_identity())
        user = User.query.get_or_404(id)
        
        if current_user.role != 'Admin' and current_user.id != id:
            return {'message': 'Unauthorized'}, 403

        data = api.payload
        user.username = data['username']
        user.email = data['email']
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.is_active = data['is_active']

        if current_user.role == 'Admin' and 'role' in data:
            user.role = data['role']

        db.session.commit()
        return user

    @jwt_required()
    @api.doc(security='Bearer Auth')
    def delete(self, id):
        current_user = User.query.get(get_jwt_identity())
        user = User.query.get_or_404(id)
        
        if current_user.role != 'Admin':
            return {'message': 'Admin access required'}, 403

        if user.role == 'Admin':
            return {'message': 'Cannot delete admin users'}, 403

        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted'}, 200

@api.route('/promote/<int:id>')
class PromoteUser(Resource):
    @jwt_required()
    @api.doc(security='Bearer Auth')
    def post(self, id):
        current_user = User.query.get(get_jwt_identity())
        if current_user.role != 'Admin':
            return {'message': 'Admin access required'}, 403

        user = User.query.get_or_404(id)
        user.role = 'Admin'
        db.session.commit()
        return {'message': 'User promoted to Admin'}, 200