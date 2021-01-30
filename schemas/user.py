from marshmallow import pre_dump, fields, post_load

from ma import ma
from models.user import UserModel
from schemas.confirmation import ConfirmationSchema


class UserSchema(ma.Schema):

    confirmation = ma.Nested(ConfirmationSchema, many=True)

    class Meta:
        model = UserModel
        load_only = ("password",)
        dump_only = ("id", "confirmation",)
        fields = ("username", "password", "email", "confirmation")

    # username = fields.Str(load_only=True)
    # password = fields.Str(load_only=True)
    # email = fields.Str(load_only=True)

    @pre_dump
    def _pre_dump(self, user: UserModel, **kwargs):
        user.confirmation = [user.most_recent_confirmation]
        return user

    @post_load
    def _post_load(self, data, **kwargs):
        user = UserModel(**data)
        # user.confirmation = [user.most_recent_confirmation]
        return user
