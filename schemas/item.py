from ma import ma
from models.item import ItemModel


class ItemSchema(ma.Schema):
    class Meta:
        model = ItemModel
        load_only = ("store",)
        dump_only = ("id", )
        include_fk = True

    # id  = fields.Int()
    # username = fields.Str(required=True)
    # password = fields.Str(required=True)
