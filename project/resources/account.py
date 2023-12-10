from flask_jwt_extended import jwt_required
from flask import make_response
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError

from project.schemas import AccountSchema, AccountIncome
from project.models import AccountModel
from project.db import db

blp = Blueprint('account', __name__, description='Operations on account')


@blp.route("/account/<int:account_id>")
class Account(MethodView):

    @blp.response(200, AccountSchema)
    def get(self, account_id):
        account = AccountModel.query.get_or_404(account_id)
        return account

    @jwt_required()
    @blp.arguments(AccountIncome(partial=True))
    def put(self, data, account_id):
        account = AccountModel.query.get_or_404(account_id)
        account.net_worth = account.net_worth + data['income']
        db.session.commit()
        return make_response({'message': 'Funds added to your account'})

    @blp.errorhandler(404)
    def handle_not_found(self):
        return make_response({'message': 'Account not found'}, 404)


@blp.route("/account")
class Accounts(MethodView):

    @blp.arguments(AccountSchema)
    @blp.response(201, AccountSchema)
    def post(self, account_data):
        account = AccountModel(**account_data)
        try:
            db.session.add(account)
            db.session.commit()
        except IntegrityError:
            abort(400, message="This user already has an account")
        return account, 201
