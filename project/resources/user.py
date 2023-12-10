from flask import make_response, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from sqlalchemy.exc import IntegrityError

from project.schemas import UserSchema
from project.models import UserModel, AccountModel
from project.db import db

blp = Blueprint('user', __name__, description="Operations on user")


@blp.route("/user/<int:user_id>")
class User(MethodView):

    @jwt_required()
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    @jwt_required()
    @blp.response(200, UserSchema)
    def delete(self, user_id):
        raise NotImplemented

    @blp.errorhandler(404)
    def handle_not_found(self):
        return make_response({'message': 'User not found'}, 404)


@blp.route("/user")
class UserList(MethodView):

    @jwt_required()
    @blp.response(200, UserSchema(many=True))
    def get(self):
        return UserModel.query.all()


@blp.route("/register")
class Registration(MethodView):

    @blp.arguments(UserSchema)
    def post(self, user_data):
        username = user_data['username']
        password = user_data['password']
        password_hash = pbkdf2_sha256.hash(password)

        user = UserModel(username=username, password=password_hash)
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            abort(400, message="User with this name already exists")
        account = AccountModel(owner_id=user.id)
        db.session.add(account)
        db.session.commit()
        return make_response(jsonify({"message": f'{username} user registered'}))


@blp.route("/login")
class Login(MethodView):

    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter_by(username=user_data['username']).first()
        if user and pbkdf2_sha256.verify(user_data['password'], user.password):
            access_token = create_access_token(identity=user.id)
            response_data = {'access_token': access_token}
            return make_response(jsonify(response_data), 200)
        else:
            abort(401, message="Invalid credentials")

