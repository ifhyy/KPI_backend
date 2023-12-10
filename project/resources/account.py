from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import make_response
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError

from project.schemas import AccountSchema, AccountIncome
from project.models import AccountModel, UserModel
from project.db import db

blp = Blueprint('account', __name__, description='Operations on account')


@blp.route("/account/<int:account_id>")
class Account(MethodView):

    @jwt_required()
    @blp.response(200, AccountSchema)
    def get(self, account_id):
        account = AccountModel.query.get_or_404(account_id)
        return account

    @blp.errorhandler(404)
    def handle_not_found(self):
        return make_response({'message': 'Account not found'}, 404)


@blp.route("/account")
class AccountAdd(MethodView):

    @jwt_required()
    @blp.arguments(AccountIncome(partial=True))
    def put(self, data):
        account = UserModel.query.filter_by(id=get_jwt_identity()).first().account
        account.net_worth = account.net_worth + data['income']
        db.session.commit()
        return make_response({'message': 'Funds added to your account'})
