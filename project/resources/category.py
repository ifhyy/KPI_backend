import uuid

from flask_smorest import Blueprint, abort
from flask.views import MethodView
from project.schemas import CategorySchema

categories = {}
blp = Blueprint('category', __name__, description="Operations on category")


@blp.route("/category/<string:category_id>")
class Category(MethodView):

    @blp.response(200, CategorySchema)
    def get(self, category_id):
        try:
            return categories[category_id]
        except KeyError:
            abort(404, "Category not found")

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
        return list(categories.values())

    @blp.arguments(CategorySchema)
    @blp.response(201, CategorySchema)
    def post(self, category_data):
        category_name = category_data.get('category')
        if category_name:
            cat_id = uuid.uuid4().hex
            category = {"id": cat_id, "category": category_name}
            categories[cat_id] = category
            return category, 201
