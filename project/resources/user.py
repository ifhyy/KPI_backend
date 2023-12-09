from flask import make_response
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError

from project.schemas import UserSchema
from project.models import UserModel
from project.db import db

blp = Blueprint('user', __name__, description="Operations on user")


@blp.route("/user/<int:user_id>")
class User(MethodView):

    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    @blp.response(200, UserSchema)
    def delete(self, user_id):
        raise NotImplemented

    @blp.errorhandler(404)
    def handle_not_found(self):
        return make_response({'message': 'User not found'}, 404)


@blp.route("/user")
class UserList(MethodView):

    @blp.response(200, UserSchema(many=True))
    def get(self):
        return UserModel.query.all()

    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        user = UserModel(**user_data)
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            abort(400, message="User with this name already exists")
        return user, 201
