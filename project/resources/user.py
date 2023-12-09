import uuid

from flask import make_response
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from project.schemas import UserSchema
from project.models import UserModel

users = {}
blp = Blueprint('user', __name__, description="Operations on user")


@blp.route("/user/<string:user_id>")
class User(MethodView):

    @blp.response(200, UserSchema)
    def get(self, user_id):
        try:
            return users[user_id]
        except KeyError:
            abort(404, "User not found")

    @blp.response(200, UserSchema)
    def delete(self, user_id):
        try:
            user = users.pop(user_id)
            return user
        except KeyError as e:
            abort(404, "User not found")

    @blp.errorhandler(404)
    def handle_not_found(self):
        return make_response({'message': 'User not found'}, 404)


@blp.route("/user")
class UserList(MethodView):

    @blp.response(200, UserSchema(many=True))
    def get(self):
        return list(users.values())

    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        username = user_data.get('username')
        user_id = uuid.uuid4().hex
        user = {"id": user_id, "username": username}
        users[user_id] = user
        return user, 201
