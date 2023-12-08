from flask_smorest import Blueprint, abort
from flask.views import MethodView
from project.schemas import RecordSchema
from project.models import RecordModel

records = {}
blp = Blueprint('user', __name__, description="Operations on record")


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
        if record_id:
            try:
                record = records.pop(record_id)
                return record
            except KeyError as e:
                abort(404, "Record not found")
        abort(400, "Required argument 'record_id' wasn't passed")


@blp.route("/record")
class RecordList(MethodView):

    @blp.response(200, RecordSchema(many=True))
    def get(self):
        return list(records.values())

    @blp.arguments(RecordSchema)
    @blp.response(201, RecordSchema)
    def post(self, record_data):
        record_user_id = record_data.get('user_id')
        if not record_user_id:
            return abort(400, {"message": "required data \'user_id\' wasn't passed"})
        record_category_id = request.get_json().get("category_id", None)
        if not record_category_id:
            return jsonify({"message": "required data \'category_id\' wasn't passed"}), 400
        date_and_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        expenses = random.randint(1, 100)
        record_id = uuid.uuid4().hex
        record = {"id": record_id, "user_id": record_user_id, "category_id": record_category_id,
                  "date_and_time": date_and_time, "expenses": expenses}
        records[record_id] = record
        return record, 201
