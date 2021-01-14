import traceback
from collections import Counter
from flask import request
from flask_jwt_extended import fresh_jwt_required
from flask_restful import Resource
from marshmallow import ValidationError
from stripe import error

from libs.strings import gettext
from models.log import LogModel
from schemas.log import LogSchema

log_schema = LogSchema()


# multiple_order_schema = LogSchema(many=True)


class Log(Resource):

    @classmethod
    def get(cls):
        # return multiple_order_schema.dump(OrderModel.find_all()), 200
        # return log_schema.dump(LogModel.find_all(), many=True), 200
        return {"message": "Get succesfull."}, 200

    @classmethod
    @fresh_jwt_required
    def post(cls):
        """
        Expect a project_name, module_name, log_type, log_message, order_date, dataset_name,ins_count (default is 0),
        upd_count (default is 0), del_count (default is 0), merge_count (default is 0),
        it_inserted_user from the request body.
        Insert a entry log into database.
        """
        log_json = request.get_json()  # list of body

        # if ItemModel.find_by_name(name):
        #     return {'message': "An item with name '{}' already exists.".format(name)}, 400

        # item_json = request.get_json()  # price and store_id
        # log_json["name"] = name

        try:
            log = log_schema.load(log_json)
        except ValidationError as ex:
            traceback.print_exc()
            return {"message": gettext("log_inserted_validation_error").format(ex.messages)}, 500

        try:
            log.save_to_db()
        except:
            traceback.print_exc()
            return {"message": gettext("log_inserted_error")}, 500

        return {"message": gettext("log_inserted_successful")}, 201

    # @classmethod
    # def post(cls):
    #     """
    #     Expect a token and a list of item ids from the request body.
    #     Construct a order to talk with Strip API to make a charge.
    #     """
    #     data = request.get_json()  # token + list of item ids
    #     items = []
    #     item_id_quantities = Counter(data["item_ids"])
    #
    #     #   iterate from list of items and retrieve from the database
    #     for _id, count in item_id_quantities.most_common():
    #         item = ItemModel.find_by_id(_id)
    #         if not item:
    #             return {"message": gettext("order_by_id+not_found").format(_id)}, 404
    #
    #         items.append(ItemsInOrder(item_id=_id, quantity=count))
    #
    #     order = OrderModel(items=items, status="pending")
    #     order.save_to_db()  # this doesn't submit to Stripe
    #
    #     try:
    #         order.set_status("failed")
    #         order.charge_with_stripe(data["token"])
    #         order.set_status("complete")
    #         return order_schema.dump(order)
    #     except error.CardError as e:
    #         # Since it is a decline, stripe.error.CardError will be caught
    #         return e.json_body, e.http_status
    #     # vezi in document restul de errori
    #     except error.StripeError as e:
    #         # Display a very generic error to the user, and maybe send yourself
    #         # an email
    #         return e.json_body, e.http_status
    #     except Exception as e:
    #         print(e)
    #         return {"message": gettext("order_error")}, 500
