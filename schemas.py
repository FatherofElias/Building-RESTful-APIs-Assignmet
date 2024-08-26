# For Task 2 defining the schema for MEMBERS

from marshmallow import Schema, fields

class MemberSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    age = fields.Int(required=True)