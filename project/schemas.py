from marshmallow import Schema, fields, validates_schema, ValidationError


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.Str(required=True)


class CategorySchema(Schema):
    id = fields.Integer(dump_only=True)
    category = fields.Str(required=True)


class RecordSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(required=True)
    category_id = fields.Integer(required=True)
    sum = fields.Float(required=True)


class RecordQuerySchema(Schema):
    user_id = fields.Integer()
    category_id = fields.Integer()

    @validates_schema
    def validate_params(self, data, **kwargs):
        user_id = data.get('user_id')
        category_id = data.get('category_id')

        if not user_id and not category_id:
            raise ValidationError("At least one of 'user_id' or 'category_id' must be provided.")
    

