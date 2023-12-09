import random
import uuid
import datetime

from flask_smorest import Blueprint, abort
from flask.views import MethodView
from project.schemas import RecordSchema, RecordQuerySchema

records = {}
blp = Blueprint('record', __name__, description="Operations on record")


@blp.route("/record/<string:record_id>")
class Record(MethodView):

    @blp.response(200, RecordSchema)
    def get(self, record_id):
        try:
            return records[record_id]
        except KeyError:
            abort(404, "Record not found")

    @blp.response(200, RecordSchema)
    def delete(self, record_id):
        try:
            record = records.pop(record_id)
            return record
        except KeyError:
            abort(404, "Record not found")


@blp.route("/record")
class RecordList(MethodView):

    @blp.arguments(RecordQuerySchema, location='query', as_kwargs=True)
    @blp.response(200, RecordSchema(many=True))
    def get(self, **kwargs):
        category_id = kwargs.get("category_id")
        user_id = kwargs.get("user_id")

        results = {}
        for key, value in records.items():
            if user_id and category_id:
                if value['user_id'] == user_id and value['category_id'] == category_id:
                    results[key] = value
            elif category_id:
                if value['category_id'] == category_id:
                    results[key] = value
            elif user_id:
                if value['user_id'] == user_id:
                    results[key] = value

        if results:
            return list(results), 200
        abort(404, "Records not found")

    @blp.arguments(RecordSchema)
    @blp.response(201, RecordSchema)
    def post(self, record_data):
        record_user_id = record_data.get('user_id')
        record_category_id = record_data.get('category_id')
        record_sum = record_data.get("sum")
        date_and_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        expenses = record_sum
        record_id = uuid.uuid4().hex
        record = {"id": record_id, "user_id": record_user_id, "category_id": record_category_id,
                  "date_and_time": date_and_time, "expenses": expenses}
        records[record_id] = record
        return record, 201
