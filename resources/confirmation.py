import traceback
from time import time

from flask import make_response, render_template
from flask_restful import Resource
from mysql.connector.utils import _get_unicode_read_direction

from libs.mailgun import MailGunException
from models.confirmation import ConfirmationModel
from models.user import UserModel
from resources.user import USER_NOT_FOUND
from schemas.confirmation import ConfirmationSchema
from libs.strings import gettext

confirmation_schema = ConfirmationSchema()


class Confirmation(Resource):
    @classmethod
    def get(cls, confirmation_id: int):
        """Return confirmation HTML page"""
        confirmation = ConfirmationModel.find_by_id(confirmation_id)
        if not confirmation:
            return {"message": gettext("confirmation_not_found")}, 404

        if confirmation.expired:
            return {"message": gettext("confirmation_expired")}, 400

        if confirmation.confirmed:
            return {"message": gettext("confirmation_already_confirmed")}, 400

        confirmation.confirmed = True
        confirmation.save_to_db()
        headers = {"Content-Type": "text/html"}
        # return {"message": USER_CONFIRMED}, 200
        return make_response(
            render_template("confirmation_page.html", email=confirmation.user.email),
            200,
            headers
        )


class ConfirmationByUser(Resource):
    @classmethod
    def get(cls, user_id: int):
        """Returns confirmation for a given user. Use for testing."""
        user = UserModel.find_by_id(user_id)

        if not user:
            return {"message": USER_NOT_FOUND}

        confirmations = [each for each in user.confirmation.order_by(ConfirmationModel.expire_at.desc(),)]

        return (
            {
                "current_time": int(time()),
                "confirmation": [
                    confirmation_schema.dump(confirmations, many=True)
                ],
            },
            200
        )

    @classmethod
    def post(cls, user_id: int):
        """Resend the confirmation."""
        user = UserModel.find_by_id(user_id)

        if not user:
            return {"message": USER_NOT_FOUND}

        try:
            confirmation = user.most_recent_confirmation
            if confirmation:
                if confirmation.confirmed:
                    return {"message": gettext("confirmation_already_confirmed")}
                confirmation.force_to_expire()

            new_confirmation = ConfirmationModel(user_id)
            new_confirmation.save_to_db()
            user.send_confirmation_email()
            return {"message": gettext("confirmation_resend_successful")}, 201
        except MailGunException as ex:
            return {"message": str(ex)}, 500
        except:
            traceback.print_exc()
            return {"message": gettext("confirmation_resend_fail")}