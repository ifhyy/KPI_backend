from flask import make_response
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError

from project.schemas import CategorySchema
from project.models import CategoryModel
from project.db import db

blp = Blueprint('category', __name__, description="Operations on category")


@blp.route("/category/<string:category_id>")
class Category(MethodView):

    @jwt_required()
    @blp.response(200, CategorySchema)
    def get(self, category_id):
        category = CategoryModel.query.get_or_404(category_id)
        return category

    @jwt_required()
    @blp.response(200, CategorySchema)
    def delete(self, category_id):
        raise NotImplemented

    @blp.errorhandler(404)
    def handle_not_found(self):
        return make_response({'message': 'Category not found'}, 404)


@blp.route("/category")
class CategoryList(MethodView):

    @jwt_required()
    @blp.response(200, CategorySchema(many=True))
    def get(self):
        return CategoryModel.query.all()

    @jwt_required()
    @blp.arguments(CategorySchema)
    @blp.response(201, CategorySchema)
    def post(self, category_data):
        category = CategoryModel(**category_data)
        try:
            db.session.add(category)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Category with this name already exists")
        return category, 201
