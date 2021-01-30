from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_migrate import Migrate, MigrateCommand, Manager
from marshmallow import ValidationError

# from flask_uploads import configure_uploads, patch_request_class
from blacklist import BLACKLIST


from db import db
# from ma import ma
# from oa import oauth

from resources.user import UserRegister, User, UserLogin, UserLogout
from resources.confirmation import Confirmation, ConfirmationByUser
# from resources.image import ImageUpload, Image, AvatarUpload, Avatar
# from resources.github_login import GithubLogin, GithubAuthorize
# from resources.order import Order
# from libs.image_helper import IMAGE_SET
from resources.log import Log
from resources.test import Test

load_dotenv(".env", verbose=True)

app = Flask(__name__)

app.config.from_object("default_config")
app.config.from_envvar("APPLICATION_SETTINGS")
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://juafomyb:MDacQZXLu7SeLA3OHTOQlDUkkj4Yw3Mc@isilo.db.elephantsql.com:5432/juafomyb';
# patch_request_class(app, 10 * 1024 * 1024)  # 10MB max size upload
# configure_uploads(app, IMAGE_SET)

api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):  # except ValidationError as err
    return jsonify(err.message)


# old approach jwt = JWT(app, authenticate, identify)  # /auth end point

jwt = JWTManager(app)


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {"is_admin": True}
    return {"is_admin": False}


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        "description": "The token has expired.",
        "error": "token_expired"
    }
    ), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        "description": "Signature verification failed",
        "error": "invalid_token"
    }
    ), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        "description": "Request doesn't contains an access token.",
        "error": "authorization_required"
    }
    ), 401


# this method will check if a token is blacklisted, and will be called automatically when blacklist is enabled
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        "description": "The token was revoked.",
        "error": "token_revoked"
    }
    ), 401


api.add_resource(UserRegister, '/user/register')
api.add_resource(User, '/user/<int:user_id>')
# api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserLogout, '/user/logout')
api.add_resource(UserLogin, '/user/login')
api.add_resource(Confirmation, '/user/confirmation/<string:confirmation_id>')
api.add_resource(ConfirmationByUser, '/user/confirmation/<int:user_id>')
# api.add_resource(ImageUpload, '/upload/image')
# api.add_resource(Image, '/image/<string:filename>')
# api.add_resource(AvatarUpload, '/upload/avatar')
# api.add_resource(Avatar, '/avatar/<int:user_id>')
# api.add_resource(GithubLogin, '/login/github')
# api.add_resource(GithubAuthorize, '/login/github/authorized', endpoint="github.authorize")
# api.add_resource(SetPassword, '/user/password')
# api.add_resource(Order, '/order')
api.add_resource(Log, '/logs')
api.add_resource(Test, '/tests')

if __name__ != '__main__':
    db.init_app(app)
    migrate = Migrate(app, db)


if __name__ == '__main__':
    db.init_app(app)
    # ma.init_app(app)
    # oauth.init_app(app)
    app.run(port=5000, debug=True)

