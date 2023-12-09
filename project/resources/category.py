import uuid

from flask_smorest import Blueprint, abort
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError

from project.schemas import CategorySchema
from project.models import CategoryModel
from project.db import db

blp = Blueprint('category', __name__, description="Operations on category")


@blp.route("/category/<string:category_id>")
class Category(MethodView):

    @blp.response(200, CategorySchema)
    def get(self, category_id):
        category = CategoryModel.query.get_or_404(category_id)
        return category

    @blp.response(200, CategorySchema)
    def delete(self, category_id):
        try:
            category = categories.pop(category_id)
            return category
        except KeyError as e:
            abort(404, "Category not found")


@blp.route("/category")
class CategoryList(MethodView):

    @blp.response(200, CategorySchema(many=True))
    def get(self):
        return CategoryModel.query.all()

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
