from marshmallow import Schema, fields, validates_schema, ValidationError
from project.db import db
from project.models import UserModel, CategoryModel, AccountModel


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)


class CategorySchema(Schema):
    id = fields.Integer(dump_only=True)
    category = fields.Str(required=True)


class RecordSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(required=True)
    category_id = fields.Integer(required=True)
    sum = fields.Float(required=True)

    @validates_schema
    def validate(self, data, **kwargs):
        self.validate_user(data)
        self.validate_category_id(data)
        self.validate_sum(data)
        return data

    def validate_user(self, data, **kwargs):
        user_id = data['user_id']
        user = UserModel.query.filter_by(id=user_id).first()
        if not user:
            raise ValidationError("User with given id not found")

        account = user.account
        if not account:
            raise ValidationError("User doesn't have account yet. You should create it first")

    def validate_category_id(self, data, **kwargs):
        category_id = data['category_id']
        exists = db.session.query(CategoryModel.id).filter_by(id=category_id).first() is not None
        if not exists:
            raise ValidationError("Category with given id not found")

    def validate_sum(self, data, **kwargs):
        user_id = data['user_id']
        sum = data['sum']
        if (AccountModel.query.filter_by(owner_id=user_id).first().net_worth - sum) < 0:
            raise ValidationError("User has not enough money on account, operation cancelled")


class RecordQuerySchema(Schema):
    user_id = fields.Integer()
    category_id = fields.Integer()

    @validates_schema
    def validate_params(self, data, **kwargs):
        user_id = data.get('user_id')
        category_id = data.get('category_id')

        if not user_id and not category_id:
            raise ValidationError("At least one of 'user_id' or 'category_id' must be provided.")
    

class AccountSchema(Schema):
    id = fields.Integer(dump_only=True)
    owner_id = fields.Integer(required=True)
    net_worth = fields.Float()


class AccountIncome(Schema):
    income = fields.Float(required=True)

    @validates_schema
    def validate_income(self, data, **kwargs):
        income = data.get("income")
        if income < 0:
            raise ValidationError("Income can't be negative")
