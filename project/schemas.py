from marshmallow import schema, fields


class UserSchema(schema):
    id = fields.Str(dump_only=True)
    username = fields.Str(required=True)


class CategorySchema(schema):
    id = fields.Str(dump_only=True)
    category = fields.Str(required=True)


class RecordSchema(schema):
    id = fields.Str(dump_only=True)
    user = fields.Str(required=True)
    category = fields.Str(required=True)
    sum = fields.Float(required=True)
    

