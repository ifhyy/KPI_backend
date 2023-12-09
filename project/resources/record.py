from flask import make_response
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from project.schemas import RecordSchema, RecordQuerySchema, RecordResponseSchema
from project.models import RecordModel, AccountModel
from project.db import db

blp = Blueprint('record', __name__, description="Operations on record")


@blp.route("/record/<string:record_id>")
class Record(MethodView):

    @blp.response(200, RecordSchema)
    def get(self, record_id):
        record = RecordModel.query.get_or_404(record_id)
        return record

    @blp.response(200, RecordSchema)
    def delete(self, record_id):
        raise NotImplemented

    @blp.errorhandler(404)
    def handle_not_found(self):
        return make_response({'message': 'Record not found'}, 404)


@blp.route("/record")
class RecordList(MethodView):

    @blp.arguments(RecordQuerySchema, location='query', as_kwargs=True)
    @blp.response(200, RecordSchema(many=True))
    def get(self, **kwargs):
        category_id = kwargs.get("category_id")
        user_id = kwargs.get("user_id")

        query = RecordModel.query

        if user_id:
            query = query.filter(RecordModel.user_id == user_id)

        if category_id:
            query = query.filter(RecordModel.category_id == category_id)

        return query.all()

    @blp.arguments(RecordSchema)
    @blp.response(201, RecordSchema)
    def post(self, record_data):
        record = RecordModel(**record_data)
        user_id = record_data['user_id']
        sum = record_data['sum']
        account = AccountModel.query.filter_by(owner_id=user_id).first()
        try:
            account.net_worth -= sum
            db.session.add(record)
            db.session.commit()
        except Exception:
            abort(400, "Error occured")
        return record, 201
