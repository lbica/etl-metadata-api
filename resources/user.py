import traceback

from flask_jwt_extended import create_access_token, create_refresh_token, get_raw_jwt, get_jwt_identity, jwt_required, \
    jwt_refresh_token_required, fresh_jwt_required
from flask_restful import Resource
from flask import request, make_response, render_template
from werkzeug.security import safe_str_cmp

from models.confirmation import ConfirmationModel
from schemas.user import UserSchema
from models.user import UserModel
from libs.mailgun import MailGunException
from libs.test_flask_lib import function_accessing_global
from libs.strings import gettext

BLANK_ERROR = "'{}' can't be blank."
USER_ALREADY_EXISTS = "A user created with that username already exists."
EMAIL_ALREADY_EXISTS = "A user created with that email already exists."

USER_NOT_FOUND = "User not found."
USER_DELETED = "User deleted."
INVALID_CREDENTIALS = "Invalid credentials."
USER_LOGGED_OUT = "User <id={user_id}> successfully logged out."
NOT_CONFIRMED_ERROR = "You have not confirmed the registration, please check your email <{}>."
USER_CONFIRMED = "User confirmed."
FAILED_TO_CREATE = "Internal server error. Failed to create user."
SUCCESS_REGISTER_USER = "Account created successfully, an email with an activation link has been sent to your email " \
                        "address, please check."


user_schema = UserSchema()


class UserRegister(Resource):

    # parser = reqparse.RequestParser()
    # parser.add_argument('username',
    #     type=str,
    #     required=True,
    #     help="This field cannot be blank."
    # )
    # parser.add_argument('password',
    #     type=str,
    #     required=True,
    #     help="This field cannot be blank."
    # )

    @classmethod
    def post(cls):

        try:
            user = user_schema.load(request.get_json())
        except Exception as ex:
            traceback.print_exc(ex)

        if UserModel.find_by_username(user.username):
            return {"message": USER_ALREADY_EXISTS}, 400

        if UserModel.find_by_email(user.email):
            return {"message": EMAIL_ALREADY_EXISTS}, 400

        try:
            user.save_to_db()
            confirmation = ConfirmationModel(user.id)
            confirmation.save_to_db()
            user.send_confirmation_email()
            return {"message": SUCCESS_REGISTER_USER}, 201
        except MailGunException as ex:
            user.delete_from_db()  # rollback
            return {"message": str(ex)}, 500
        except:
            traceback.print_exc()
            user.delete_from_db()  # rollback
            return {"message": FAILED_TO_CREATE}, 500


class User(Resource):
    """
    This Resource can be useful when testing our Flask app. We may not want to expose it to public users, but for the
    sake of demonstration in this course, it can be useful when
    we manipulating data regarding the users.
    """

    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user_id:
            return {"message": USER_NOT_FOUND}, 404

        return user_schema.dump(user), 200

    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user_id:
            return {"message": USER_NOT_FOUND}, 404

        user.delete_from_db()

        return {"message": USER_DELETED}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):

        user_json = request.get_json()
        user_data = user_schema.load(user_json, partial=("email",))

        user = UserModel.find_by_username(user_data.username)

        g.token = "Test"
        function_accessing_global()

        # this is what 'authenticate()' function did in security.py
        if user and user.password and safe_str_cmp(user.password, user_data.password):
            confirmation = user.most_recent_confirmation
            if confirmation and confirmation.confirmed:
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(identity=user.id)
                return {"access_token": access_token, "refresh_token": refresh_token}, 200
            return {"message": NOT_CONFIRMED_ERROR.format(user.username)}, 400

        return {"message": INVALID_CREDENTIALS}, 401


class UserLogout(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        jti = get_raw_jwt()["jti"]  # jti is "JWT ID", a unique identifier for a JWT
        user_id = get_jwt_identity()
        # BLACKLIST.add(jti);

        return {"message": USER_LOGGED_OUT.format(user_id)}, 200


class TokenRefresh(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        jti = get_raw_jwt()["jti"]  # jti is "JWT ID", a unique identifier for a JWT
        user_id = get_jwt_identity()
        # BLACKLIST.add(jti);

        return {"message": USER_LOGGED_OUT.format(user_id)}, 200


class SetPassword(Resource):
    @classmethod
    @fresh_jwt_required
    def post(cls):
        user_json = request.get_json()
        user_data = user_schema.load(user_json)  # username and new password
        user = UserModel.find_by_username(user_data.username)

        if not user:
            return {"message": gettext("user_not_found")}, 400

        user.password = user_data.password
        user.save_to_db()

        return {"message": gettext("user_password_updated")}, 201