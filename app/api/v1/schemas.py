from marshmallow import fields
from app.ext import ma


class UsersSchema(ma.Schema):
    userId = fields.Integer(dump_only=True)
    public_id = fields.String(dump_only=True)
    name = fields.String(required=True)
    password = fields.String(required=True)
    admin = fields.Boolean(dump_only=True)

    # Relaciones
    tokens = fields.List(fields.Nested(lambda: BlacklistTokenSchema(exclude=("users",))), dump_only=True)

    # Ordenar el Output
    class Meta:
        fields = ("userId", "public_id", "name", "password", "admin", "tokens")
        ordered = True


class BlacklistTokenSchema(ma.Schema):
    token_id = fields.Integer(required=True, dump_only=True)
    jti = fields.String(required=True, dump_only=True)
    token_type = fields.String(required=True, dump_only=True)
    user_identity = fields.String(required=True, dump_only=True)
    expires = fields.DateTime(required=True, dump_only=True)

    # Relaciones
    users = fields.Nested(UsersSchema(exclude=("tokens",)), dump_only=True)

    # Ordenar el Output
    class Meta:
        fields = ("token_id", "jti", "token_type", "user_identity", "expires", "users")
        ordered = True
