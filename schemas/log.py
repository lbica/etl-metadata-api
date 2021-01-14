from datetime import datetime


from marshmallow import fields, Schema, EXCLUDE, post_load

from ma import ma


from models.log import LogModel


class LogSchema(Schema):

    class Meta:
        model = LogModel
        load_only = ("log_message", "log_type", "project_name", "module_name", "order_date", "dataset_name", "ins_count",
                     "upd_count", "del_count", "merge_count", "it_ins_user", )
        dump_only = ("id", )
        unknown = EXCLUDE
        # load_instance = True

    project_name = fields.Str(load_only=True)
    module_name = fields.Str(load_only=True)
    order_date = fields.Date(format="%Y%m%d")
    ins_count = fields.Int(load_only=True)
    upd_count = fields.Int(load_only=True)
    del_count = fields.Int(load_only=True)
    merge_count = fields.Int(load_only=True)
    it_ins_user = fields.Str(load_only=True)

    # order_datef = fields.Function(lambda obj: datetime.strptime(obj.order_date, '%Y%m%d'))

    @post_load
    def create_log(self, data, **kwargs):
        instance = LogModel(**data)
        return instance






