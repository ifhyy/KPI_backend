from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Str(dump_only=True)
    username = fields.Str(required=True)


class CategorySchema(Schema):
    id = fields.Str(dump_only=True)
    category = fields.Str(required=True)


class RecordSchema(Schema):
    id = fields.Str(dump_only=True)
    user = fields.Str(required=True)
    category = fields.Str(required=True)
    sum = fields.Float(required=True)


class RecordQuerySchema(Schema):
    user_id = fields.Str(required=True)
    category_id = fields.Str()
    

