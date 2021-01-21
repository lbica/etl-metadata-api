from marshmallow import pre_dump, fields, post_load

from ma import ma
from models.user import UserModel


class UserSchema(ma.Schema):
    class Meta:
        model = UserModel
        # load_only = ("password",)
        # dump_only = ("id", "activated",)

    username = fields.Str(load_only=True)
    password = fields.Str(load_only=True)
    email = fields.Str(load_only=True)

    # @pre_dump
    # def __pre_dump(self, user: UserModel):
    #     user.confirmation = [user.most_recent_confirmation]
    #     return user

    @post_load
    def create_user(self, data, **kwargs):
        instance = UserModel(**data)
        return instance
